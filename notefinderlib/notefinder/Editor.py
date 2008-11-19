#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#       Copyright (C) 2008 GFORGX <gforgx@gmail.com>
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
#       * Neither the name of the  nor the names of its
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

from notefinderlib.libnotetaking import *
from notefinderlib.creoleparser import text2html

from PyQt4 import Qt

from notefinderlib.notefinder.EditorWidget import Ui_Form

class EditorWidget(Qt.QWidget):
    def __init__(self, app):
        Qt.QWidget.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.app = app

        self.connect(self.ui.addTagButton, Qt.SIGNAL('clicked()'), self.addTag)
        self.connect(self.ui.tagEdit.lineEdit(), Qt.SIGNAL('returnPressed()'), self.addTag)
        self.connect(self.ui.tagsList, Qt.SIGNAL('itemDoubleClicked(QListWidgetItem *)'), self.editTag)
        self.connect(self.ui.delTagButton, Qt.SIGNAL('clicked()'), self.deleteTag)
        
        self.connect(self.ui.textEdit, Qt.SIGNAL('textChanged()'), self.update)
        
        self.connect(self.ui.textBrowser, Qt.SIGNAL('anchorClicked(const QUrl)'), self.openUrl)
        
        self.connect(self.ui.findButton, Qt.SIGNAL('clicked()'), self.find)
        self.connect(self.ui.searchEdit, Qt.SIGNAL('returnPressed()'), self.find)

        self.refresh()

    def refresh(self):
        """ Cleaning interface up """
        self.ui.tagEdit.clear()

        for tag in self.app.notebook.getTags():
            self.ui.tagEdit.addItem(unicode(tag, 'utf'))

        self.ui.tagEdit.setEditText('')

    def addTag(self):
        """ Adding entered tag to list """
        line = str(self.ui.tagEdit.currentText().toUtf8())

        if not line == '' and not line in self.tags():
            notes = self.app.notebook.getNotesByTag(line)

            item = Qt.QListWidgetItem(Qt.QIcon(':/tag.png'), unicode(line, 'utf'), self.ui.tagsList)
            item.setToolTip(self.trUtf8('Notes (%i): %s' % (len(notes), ', '.join(notes))))
    
            self.ui.tagEdit.lineEdit().clear()

    def deleteTag(self):
        """ Removing current item from list """
        self.ui.tagsList.takeItem(self.ui.tagsList.currentRow())

    def editTag(self):
        """ Opens item editor """
        self.ui.tagsList.openPersistentEditor(self.ui.tagsList.currentRow())

    def tags(self):
        """ Gets currently added tags list """
        return [str(self.ui.tagsList.item(i).text().toUtf8()) for i in xrange(self.ui.tagsList.count())]

    def openUrl(self, url):
        """ Opens clicked URL (internal or external """
        if str(url.scheme().toUtf8()) != "":
            Qt.QDesktopServices().openUrl(url)
        else:
            if Note(str(url.path().toUtf8()), self.app.notebook).exists():
                self.app.openNote(str(url.path().toUtf8()))
            else:
                self.app.new(str(url.path().toUtf8()))

    def find(self, text=None):
        """ Finds text in text browser/editor """
        if text is None:
            text = self.ui.searchEdit.text()

        self.ui.textBrowser.find(text)
        self.ui.textEdit.find(text)

    def update(self):
        """ Updates HTML Preview """
        text = str(self.ui.textEdit.toPlainText().toUtf8())

        if self.app.notebook.markup == 'HTML': 
            html = text
        else: 
            html = text2html(unicode(text, 'utf'))

        self.ui.textBrowser.setHtml(self.trUtf8(html))
        if self.app.settings["AutoSave"]:
            self.app.saveNote()