#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#       Copyright (C) 2007-2008 Simonenko Sergey <gforgx@lavabit.com>
#
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#
#       * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following disclaimer
#       in the documentation and/or other materials provided with the
#       distribution.
#       * Neither the name of the project NoteFinder and author's name nor the names of 
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#      "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Standard library imports
import os
import re

# Configuration handler
from notefinderlib.libnotetaking.config import Config

# Backend imports
from notefinderlib.libnotetaking.backends.dokuwiki import DokuWiki
from notefinderlib.libnotetaking.backends.files import Files
from notefinderlib.libnotetaking.backends.filesystem import FileSystem
from notefinderlib.libnotetaking.backends.ical import iCal
from notefinderlib.libnotetaking.backends.ipod import iPod
from notefinderlib.libnotetaking.backends.mail import Mail
from notefinderlib.libnotetaking.backends.opera import Opera
from notefinderlib.libnotetaking.backends.rss import RSS
from notefinderlib.libnotetaking.backends.wixi import Wixi
from notefinderlib.libnotetaking.backends.zim import Zim

# Backends dictionary
backends = {
    'FileSystem':FileSystem,
    'Files':Files,
    'iCal':iCal,
    'iPod':iPod,
    'DokuWiki':DokuWiki,
    'RSS':RSS,
    'Mail':Mail,
    'Opera':Opera,
    'Zim':Zim,
    'Wixi':Wixi
    }

# Encryption library
from notefinderlib.p3 import *

# Initializing configuration handler
config = Config()

class Notebook(object):
    def __init__(self, name):
        self.name = name

        # Selects backend from the dictionary
        try:
            self.backend = backends[config.getBackend(self.name)](config, self.name)
        except KeyError:
            raise Exception("Notebook doesn't exist")

        self.markup = config.get('Markup', self.name)

        self.Wiki = (self.markup == 'Wiki')

    def add(self, note, text, key=None):
        if not key is None:
            text = p3_encrypt(text, key)
        self.backend.write(note, text)

    def tag(self, note, tags):
        self.backend.tag(note, tags)

    def delete(self, note):
        return self.backend.deleteNote(note)

    def rename(self, note, new):
        self.add(new, self.get(note))
        self.tag(new, self.noteTags(note))
        self.delete(note)

    def copy(self, note, notebooks, move=False):
        for i in notebooks:
            Notebook(i).add(note, self.get(note))

        if move:
            self.delete(note)

    def get(self, note, key=None):
        if not key is None:
            return p3_decrypt(self.backend.getText(note), key)
        else:
            return str(self.backend.getText(note))

    def noteDate(self, note):
        return self.backend.getNoteDate(note)

    def noteTags(self, note):
        return self.backend.getNoteTags(note)

    def url(self, note):
        return self.notebook.backend.getURL(note)

    def backlinks(self, note):
        return [i for i in self.notes() if re.compile(r'^.*\[\[%s(\|.*)?\]\].*$' % (note), re.DOTALL).match(self.get(i))]

    def related(self, note):
        notes = []

        for tag in self.noteTags(note):
            for note in self.byTag(tag):
                if not note in notes:
                    notes.append(note)

        return notes

    def notes(self):
        return self.backend.getNotes()

    def dates(self):
        return self.backend.getDates()

    def tags(self):
        return self.backend.getTags()

    def has(self, note):
        return self.backend.noteExists(note)

    def byDate(self, date):
        return self.backend.getNotesByDate(date)
    
    def byTag(self, tag):
        return self.backend.getNotesByTag(tag)
    
    def byText(self, t):
        return [i for i in self.notes() if re.compile('^.*%s.*$' % (t), re.DOTALL|re.IGNORECASE).match(self.get(i))]

    def search(self, items):
        results = []

        # Processing search items
        for item in items:

            try:
                # Trying to split item into parameter, keyword pair
                parameter, keyword = item.split(':')

                # Checking date
                if parameter == 'date': notes = self.byDate(keyword)

                # Checking year
                elif parameter == 'year':
                    notes = []
                    for date in self.dates():
                        if date.split('-')[0] == keyword: notes.extend(self.byDate(date))

                # Checking month
                elif parameter == 'month':
                    notes = []
                    for date in self.dates():
                        if date.split('-')[1] == keyword: notes.extend(self.byDate(date))

                # Checking day
                elif parameter == 'day':
                    notes = []
                    for date in self.dates():
                        if date.split('-')[2] == keyword:  notes.extend(self.byDate(date))

                # Checking tag
                elif parameter == 'tag': notes = self.byTag(keyword)

                # Checking text
                elif parameter == 'text': notes = self.byText(keyword)

                # Checking title
                elif parameter == 'title':
                    notes = [i for i in [keyword] if self.has(keyword)]

                else:  notes = []

            except ValueError:

                notes = self.byDate(item) + self.byTag(item) + self.byText(item)
                if self.has(item):
                    if not item in notes: notes.append(item)

            results.append(notes)

        isection = lambda list: set(list[0]) if len(list) == 1 else set(list[0]).intersection(isection(list[1::]))

        return list(isection(results))
    
    def addTag(self, tag):
        self.backend.createTag(tag)
    
    def deleteTag(self, tag):
        self.backend.removeTag(tag)
