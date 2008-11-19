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

import sys
from datetime import datetime
from time import localtime
import pickle
from inspect import isclass
try:
    from pkg_resources import iter_entry_points
    PLUGINS = True
except ImportError:
    PLUGINS = False

from PyQt4 import Qt

from notefinderlib.libnotetaking import *
from notefinderlib.creoleparser import text2html

from notefinderlib.notefinder.About import Ui_AboutDialog
from notefinderlib.notefinder.AddTag import Ui_AddTagDialog
from notefinderlib.notefinder.CopyEntry import Ui_CopyDialog
from notefinderlib.notefinder.Credits import Ui_CreditsDialog
from notefinderlib.notefinder.Delete import Ui_DeleteDialog
from notefinderlib.notefinder.DeleteNotebook import Ui_DeleteNotebookDialog
from notefinderlib.notefinder.DeleteTag import Ui_DeleteTagDialog
from notefinderlib.notefinder.Editor import EditorWidget
from notefinderlib.notefinder.License import Ui_LicenseDialog
from notefinderlib.notefinder.Main import Ui_MainWindow
from notefinderlib.notefinder.Message import Ui_MessageDialog
from notefinderlib.notefinder.Notebook import Ui_NotebookDialog
from notefinderlib.notefinder.plugin import Plugin
from notefinderlib.notefinder.Rename import Ui_RenameDialog
from notefinderlib.notefinder.Settings import Ui_SettingsDialog
from notefinderlib.notefinder.notefinder_rc import *

__version__ = '0.2.5'

class Application(Qt.QObject):
    def __init__(self):
        Qt.QObject.__init__(self)
        self.application = Qt.QApplication(sys.argv)

        # l10n
        translator = Qt.QTranslator()
        translator.load('notefinder_' + Qt.QLocale.system().name() + '.qm', ':/')
        self.application.installTranslator(translator)

        # Loading saved searches
        self.searchesFile = os.path.expanduser("~/.config/notefinder/searches.dat")

        try: self.searches = pickle.load(open(self.searchesFile))
        except: self.searches = []

        # Backend icons
        self.backendIcons = {
            'DokuWiki' : ':/dokuwiki.png',
            'iPod' : ':/ipod.png',
            'Zim' : ':/zim.png',
            'iCal' : ':/ical.png',
            'Files' : ':/icon.png',
            'FileSystem' : ':/icon.png',
            'Wixi' : ':/wixi.png',
            'RSS' : ':/rss.png',
            'Mail': ':/mail_post_to.png'
        }

        # Settings
        self.settings = {
            'AutoSave' : True,
            'BackendIcons' : True,
            'Dates' : False,
            'SearchCompletion' : True,
            'SearchOnTheFly' : True,
            'ShowMetaPanel' : True,
            'Toolbars' : True,
            'TrayIcon' : True,
            'Tooltips' : True,
        }

        self.connect(self, Qt.SIGNAL('notesModified()'), self.refresh)

        # Main window stuff
        self.mainWindow = Qt.QMainWindow()
        self.mainWindow.ui = Ui_MainWindow()
        self.mainWindow.ui.setupUi(self.mainWindow)
        
        # Setting current date
        date = localtime()[:3]
        self.mainWindow.ui.dateEdit.setDate(Qt.QDate(date[0], date[1], date[2]))

        self.mainWindow.ui.closeButton = Qt.QToolButton(self.mainWindow)
        self.mainWindow.ui.closeButton.setIcon(Qt.QIcon(':/tab_remove.png'))
        self.mainWindow.ui.closeButton.setToolButtonStyle(Qt.Qt.ToolButtonIconOnly)
        self.mainWindow.ui.closeButton.setShortcut('Ctrl+W')
        self.mainWindow.ui.tabWidget.setCornerWidget(self.mainWindow.ui.closeButton)
        self.mainWindow.closeEvent = self.closeEvent

        # Сontext menus
        self.mainWindow.ui.notesList.setContextMenuPolicy(Qt.Qt.ActionsContextMenu)
        self.mainWindow.ui.notesList.addAction(self.mainWindow.ui.actionE_Mail)
        self.mainWindow.ui.notesList.addAction(self.mainWindow.ui.actionBacklinks)
        self.mainWindow.ui.notesList.addAction(self.mainWindow.ui.actionFindRelated)
        self.mainWindow.ui.notesList.addAction(self.mainWindow.ui.actionCreateIndex)
        self.mainWindow.ui.notesList.addAction(self.mainWindow.ui.actionMerge)
        self.mainWindow.ui.notesList.addAction(self.mainWindow.ui.actionRename)
        self.mainWindow.ui.notesList.addAction(self.mainWindow.ui.actionCopyEntry)
        self.mainWindow.ui.notesList.addAction(self.mainWindow.ui.actionOpenExternally)
        self.mainWindow.ui.notesList.addAction(self.mainWindow.ui.actionDelete)

        self.mainWindow.ui.metaList.setContextMenuPolicy(Qt.Qt.ActionsContextMenu)
        self.mainWindow.ui.metaList.addAction(self.mainWindow.ui.actionDeleteNotebook)
        self.mainWindow.ui.metaList.addAction(self.mainWindow.ui.actionDeleteTag)
        self.mainWindow.ui.metaList.addAction(self.mainWindow.ui.actionDeleteSelectedSearch)

        self.connect(self.mainWindow.ui.actionAboutQt, Qt.SIGNAL('triggered()'), self.application.aboutQt)
        self.connect(self.mainWindow.ui.metaList, Qt.SIGNAL('itemSelectionChanged()'), self.refreshMenu)
        self.connect(self.mainWindow.ui.closeButton, Qt.SIGNAL("clicked()"), self.closeTab)
        self.connect(self.mainWindow.ui.actionExit, Qt.SIGNAL('triggered()'), self.application.quit)
        
        self.connect(self.mainWindow.ui.dateEdit, Qt.SIGNAL('editingFinished()'), self.openDate)
        self.connect(self.mainWindow.ui.metaList, Qt.SIGNAL('itemClicked(QListWidgetItem *)'), self.openMeta)
        self.connect(self.mainWindow.ui.searchEdit, QtCore.SIGNAL("returnPressed()"), self.search)
        
        self.connect(self.mainWindow.ui.actionNew, Qt.SIGNAL('triggered()'), self.new)
        self.connect(self.mainWindow.ui.actionCreateIndex,  Qt.SIGNAL('triggered()'), self.buildListIndex)
        self.connect(self.mainWindow.ui.actionMerge, Qt.SIGNAL('triggered()'), self.merge)
        self.connect(self.mainWindow.ui.notesList, Qt.SIGNAL('itemDoubleClicked(QListWidgetItem *)'), self.openFromList) 
        self.connect(self.mainWindow.ui.actionSave, Qt.SIGNAL('triggered()'), self.saveNote)

        self.connect(self.mainWindow.ui.actionE_Mail, Qt.SIGNAL('triggered()'), self.email)
        self.connect(self.mainWindow.ui.actionOpenExternally, Qt.SIGNAL('triggered()'), self.openExternally)
        self.connect(self.mainWindow.ui.actionFindRelated, Qt.SIGNAL('triggered()'), self.findRelated)
        self.connect(self.mainWindow.ui.actionBacklinks, Qt.SIGNAL('triggered()'), self.backlinks)

        self.connect(self.mainWindow.ui.actionAll, Qt.SIGNAL('triggered()'), self.showAll)
        self.connect(self.mainWindow.ui.actionToday, Qt.SIGNAL('triggered()'), self.today)
        
        self.connect(self.mainWindow.ui.saveSearchButton, Qt.SIGNAL('clicked()'), self.saveSearch)
        self.connect(self.mainWindow.ui.actionDeleteSelectedSearch, Qt.SIGNAL('triggered()'), self.deleteSearch)

        self.connect(self.mainWindow.ui.actionBold, Qt.SIGNAL('triggered()'), self.bold)
        self.connect(self.mainWindow.ui.actionItalic, Qt.SIGNAL('triggered()'), self.italic)
        self.connect(self.mainWindow.ui.actionUnderlined, Qt.SIGNAL('triggered()'), self.underline)
        self.connect(self.mainWindow.ui.actionHighlight, Qt.SIGNAL('triggered()'), self.highlight)
        self.connect(self.mainWindow.ui.actionImage, Qt.SIGNAL('triggered()'), self.image)
        self.connect(self.mainWindow.ui.actionTimestamp, Qt.SIGNAL('triggered()'), self.insertTime)
        self.connect(self.mainWindow.ui.actionBulletedList, Qt.SIGNAL('triggered()'), self.list)

        self.writeActions = (
            self.mainWindow.ui.actionNew,
            self.mainWindow.ui.actionRename,
            self.mainWindow.ui.actionDelete,
            self.mainWindow.ui.actionSave
            )

        self.wikiActions = (
            self.mainWindow.ui.actionBacklinks,
            self.mainWindow.ui.actionCreateIndex,
            self.mainWindow.ui.actionMerge
        )

        # Tray
        self.tray = Qt.QSystemTrayIcon(self)
        self.headerAction = Qt.QWidgetAction(self)
        self.headerFrame = Qt.QFrame()
        self.headerFrame.setFrameShape(Qt.QFrame.StyledPanel)
        self.headerAction.setDefaultWidget(self.headerFrame)
        self.headerLayout = Qt.QHBoxLayout()
        self.headerLayout.setMargin(3)
        self.headerLayout.setSpacing(5)
        self.headerFrame.setLayout(self.headerLayout)
        self.headerLabel = Qt.QLabel()
        self.headerLabel.setPixmap(Qt.QPixmap(':/note_small.png'))
        self.headerLayout.insertWidget(-1, self.headerLabel, 0)
        self.headerText = Qt.QLabel('<b>NoteFinder %s</b>' % (__version__))
        self.headerLayout.insertWidget(-1, self.headerText, 20)
        
        self.menu = Qt.QMenu()
        self.menu.addAction(self.headerAction)
        self.menu.addAction(self.mainWindow.ui.actionNew)
        self.menu.addSeparator()
        self.pluginsMenu = Qt.QMenu('Plugins')
        self.menu.addMenu(self.pluginsMenu)
        self.menu.addSeparator()
        self.menu.addAction(self.mainWindow.ui.actionPreferences)
        self.menu.addAction(self.mainWindow.ui.actionExit)
        self.tray.setContextMenu(self.menu)
        self.tray.setIcon(Qt.QIcon(':/icon.png'))
        
        # Other dialogs
        self.aboutDialog = Qt.QDialog()
        self.aboutDialog.ui = Ui_AboutDialog()
        self.aboutDialog.ui.setupUi(self.aboutDialog)
        self.aboutDialog.ui.versionLabel.setText('<h2>%s</h2>' % (__version__))

        self.connect(self.mainWindow.ui.actionAbout, Qt.SIGNAL('triggered()'), self.aboutDialog.show)

        self.addTagDialog = Qt.QDialog()
        self.addTagDialog.ui = Ui_AddTagDialog()
        self.addTagDialog.ui.setupUi(self.addTagDialog)
 
        self.connect(self.mainWindow.ui.actionAddTag, Qt.SIGNAL('triggered()'), self.addTagDialog.show)
        self.connect(self.addTagDialog.ui.buttonBox, Qt.SIGNAL('accepted()'), self.addTag)

        self.copyDialog = Qt.QDialog()
        self.copyDialog.ui = Ui_CopyDialog()
        self.copyDialog.ui.setupUi(self.copyDialog)

        self.connect(self.mainWindow.ui.actionCopyEntry, Qt.SIGNAL('triggered()'), self.copyDialog.show)
        self.connect(self.copyDialog.ui.buttonBox, Qt.SIGNAL('accepted()'), self.copyEntry)

        self.creditsDialog = Qt.QDialog()
        self.creditsDialog.ui = Ui_CreditsDialog()
        self.creditsDialog.ui.setupUi(self.creditsDialog)

        self.connect(self.aboutDialog.ui.creditsButton, Qt.SIGNAL('clicked()'), self.creditsDialog.show)

        self.deleteDialog = Qt.QDialog()
        self.deleteDialog.ui = Ui_DeleteDialog()
        self.deleteDialog.ui.setupUi(self.deleteDialog)

        self.connect(self.mainWindow.ui.actionDelete, Qt.SIGNAL('triggered()'), self.deleteDialog.show)
        self.connect(self.deleteDialog.ui.buttonBox, Qt.SIGNAL('accepted()'), self.deleteNotes)
        
        self.deleteNotebookDialog = Qt.QDialog()
        self.deleteNotebookDialog.ui = Ui_DeleteNotebookDialog()
        self.deleteNotebookDialog.ui.setupUi(self.deleteNotebookDialog)

        self.connect(self.mainWindow.ui.actionDeleteNotebook, Qt.SIGNAL('triggered()'), self.deleteNotebookDialog.show)
        self.connect(self.deleteNotebookDialog.ui.buttonBox, Qt.SIGNAL('accepted()'), self.deleteNotebook)

        self.deleteTagDialog = Qt.QDialog()
        self.deleteTagDialog.ui = Ui_DeleteTagDialog()
        self.deleteTagDialog.ui.setupUi(self.deleteTagDialog)

        self.connect(self.mainWindow.ui.actionDeleteTag, Qt.SIGNAL('triggered()'), self.deleteTagDialog.show)
        self.connect(self.deleteTagDialog.ui.buttonBox, Qt.SIGNAL('accepted()'), self.deleteTag)

        self.licenseDialog = Qt.QDialog()
        self.licenseDialog.ui = Ui_LicenseDialog()
        self.licenseDialog.ui.setupUi(self.licenseDialog)

        self.connect(self.aboutDialog.ui.licenseButton, Qt.SIGNAL('clicked()'), self.licenseDialog.show)

        self.messageDialog = Qt.QDialog()
        self.messageDialog.ui = Ui_MessageDialog()
        self.messageDialog.ui.setupUi(self.messageDialog)
        
        self.notebookDialog = Qt.QDialog()
        self.notebookDialog.ui = Ui_NotebookDialog()
        self.notebookDialog.ui.setupUi(self.notebookDialog)

        self.notebookDialog.settings = {}
        for i in backends:
            self.notebookDialog.ui.backends.addItem(Qt.QIcon(self.backendIcons[i]), i)
        
        self.selectBackend()

        self.connect(self.mainWindow.ui.actionAddNotebook, Qt.SIGNAL('triggered()'), self.notebookDialog.show)
        self.connect(self.notebookDialog.ui.backends, Qt.SIGNAL('currentIndexChanged(const QString)'), self.selectBackend)
        self.connect(self.notebookDialog.ui.buttonBox, Qt.SIGNAL('accepted()'), self.addNotebook)

        self.renameDialog = Qt.QDialog()
        self.renameDialog.ui = Ui_RenameDialog()
        self.renameDialog.ui.setupUi(self.renameDialog)

        self.connect(self.mainWindow.ui.actionRename, Qt.SIGNAL('triggered()'), self.renameDialog.show)
        self.connect(self.renameDialog.ui.buttonBox, Qt.SIGNAL('accepted()'), self.renameNote)
        
        # Settings dialog
        self.settingsDialog = Qt.QDialog()
        self.settingsDialog.ui = Ui_SettingsDialog()
        self.settingsDialog.ui.setupUi(self.settingsDialog)
        self.settingsDialog.ui.updatePluginAction = Qt.QAction(self.settingsDialog)
        self.settingsDialog.ui.listWidget.setContextMenuPolicy(Qt.Qt.ActionsContextMenu)
        self.settingsDialog.ui.listWidget.addAction(self.settingsDialog.ui.updatePluginAction)

        self.connect(self.mainWindow.ui.actionPreferences, Qt.SIGNAL('triggered()'), self.settingsDialog.show)
        self.connect(self.settingsDialog.ui.buttonBox, Qt.SIGNAL('accepted()'), self.writeSettings)
        self.connect(self.settingsDialog.ui.listWidget, Qt.SIGNAL('itemSelectionChanged()'), self.updatePluginMenu)
        self.connect(self.settingsDialog.ui.updatePluginAction, Qt.SIGNAL('triggered()'), self.setPlugins)
        
        self.readSettings()
        self.applySettings()

        # Initializing notebook
        try:
            self.setNotebook(config.getNotebook())
        except:
            config.addNotebook('Default', 'FileSystem', 'Wiki', [os.path.expanduser('~/.notes')])
            self.setNotebook('Default')

        self.parameter = [self.notebook.getNotes]
        
        self.loadPlugins()
        
        self.refresh()

    def readSettings(self):
        config = Config()
        for i in self.settings:
            try: self.settings[i] = config.getboolean('UI', i)
            except: pass

    def applySettings(self):
        self.settingsDialog.ui.toolTips.setChecked(self.settings['Tooltips'])
        self.settingsDialog.ui.backendIcons.setChecked(self.settings['BackendIcons'])
        self.settingsDialog.ui.trayIcon.setChecked(self.settings['TrayIcon'])
        self.settingsDialog.ui.autoSave.setChecked(self.settings['AutoSave'])
        self.settingsDialog.ui.searchCompletion.setChecked(self.settings['SearchCompletion'])
        self.settingsDialog.ui.searchOnTheFly.setChecked(self.settings['SearchOnTheFly'])
        self.settingsDialog.ui.showMetaPanel.setChecked(self.settings['ShowMetaPanel'])
        self.settingsDialog.ui.showDates.setChecked(self.settings['Dates'])

        if self.settings['TrayIcon']:
            self.tray.show()
            self.connect(self.tray, Qt.SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), self.showHide)

        if self.settings['SearchOnTheFly']:
            self.connect(self.mainWindow.ui.searchEdit, Qt.SIGNAL('textChanged(const QString)'), self.search)
    
        if self.settings['ShowMetaPanel']:
            self.mainWindow.ui.splitter.setSizes([220, 1030])
        else:
            self.mainWindow.ui.splitter.setSizes([0, 1030])

    def writeSettings(self):
        if not config.has_section('UI'):
            config.add_section('UI')

        config.set('UI', 'AutoSave', self.settingsDialog.ui.autoSave.isChecked())
        config.set('UI', 'BackendIcons', self.settingsDialog.ui.backendIcons.isChecked())
        config.set('UI', 'SearchCompletion', self.settingsDialog.ui.searchCompletion.isChecked())
        config.set('UI', 'SearchOnTheFly', self.settingsDialog.ui.searchOnTheFly.isChecked())
        config.set('UI', 'ShowMetaPanel', self.settingsDialog.ui.showMetaPanel.isChecked())
        config.set('UI', 'Tooltips', self.settingsDialog.ui.toolTips.isChecked())
        config.set('UI', 'TrayIcon', self.settingsDialog.ui.trayIcon.isChecked())
        config.set('UI', 'Dates', self.settingsDialog.ui.showDates.isChecked())

        config.write(open(config.file, 'w'))

        self.readSettings()
        self.refresh()

    def loadPlugins(self):
        """ Loads plugins """
        if PLUGINS:
            for ep in iter_entry_points('notefinder.plugins'):
                try:
                    plugin = ep.load()
                    if isclass(plugin):
                        if issubclass(plugin, Plugin):
                            p = plugin(self)
                            
                            item = Qt.QListWidgetItem(p.icon(), p.text(), self.settingsDialog.ui.listWidget)
                            item.name = p.name
                            item.setToolTip(p.toolTip())
                            item.pluginEnabled = False

                            if config.has_option('Plugins', plugin.name):
                                if config.getboolean('Plugins', plugin.name):
                                    p.load()
    
                                    item.pluginEnabled = True
                except:
                    pass

    def setPlugins(self):
        item = self.settingsDialog.ui.listWidget.currentItem()
        item.pluginEnabled = not item.pluginEnabled
        self.updatePluginMenu()
        if not config.has_section('Plugins'):
            config.add_section('Plugins')
        config.set('Plugins', item.name, str(item.pluginEnabled))
        config.write(open(config.file, 'w'))

    def updatePluginMenu(self):
        item = self.settingsDialog.ui.listWidget.currentItem()
        if item.pluginEnabled:
            self.settingsDialog.ui.updatePluginAction.setText(self.trUtf8('Disable'))
        else:
            self.settingsDialog.ui.updatePluginAction.setText(self.trUtf8('Enable'))

    def selectBackend(self):
        backend = backends[str(self.notebookDialog.ui.backends.currentText().toUtf8())]
        for i in (self.notebookDialog.ui.path, self.notebookDialog.ui.pathEdit):
            i.setHidden(not backend.path)
            self.notebookDialog.settings[self.notebookDialog.ui.pathEdit] = backend.path
        for i in (self.notebookDialog.ui.url, self.notebookDialog.ui.urlEdit):
            i.setHidden(not backend.url)
            self.notebookDialog.settings[self.notebookDialog.ui.urlEdit] = backend.url
        for i in (self.notebookDialog.ui.login, self.notebookDialog.ui.loginEdit):
            i.setHidden(not backend.login)
            self.notebookDialog.settings[self.notebookDialog.ui.loginEdit] = backend.login
        for i in (self.notebookDialog.ui.passwd, self.notebookDialog.ui.passwdEdit):
            i.setHidden(not backend.passwd)
            self.notebookDialog.settings[self.notebookDialog.ui.passwdEdit] = backend.passwd

        self.notebookDialog.ui.desc.setText(self.trUtf8(backend.desc))
        self.notebookDialog.adjustSize()

    def setNotebook(self, notebook):
        self.notebook = Notebook(notebook)
        config.setDefault(notebook)

        for i in self.writeActions: i.setVisible(not self.notebook.backend.ReadOnly)
        for i in self.wikiActions: i.setVisible(self.notebook.Wiki)

        self.mainWindow.ui.menuTag.setEnabled(self.notebook.backend.Tag)
        self.mainWindow.ui.actionOpenExternally.setVisible(self.notebook.backend.URL)

    def closeTab(self):
        tab = self.mainWindow.ui.tabWidget.currentIndex()
        if tab != 0: self.mainWindow.ui.tabWidget.removeTab(tab)

    def showHide(self, reason):
        if reason == Qt.QSystemTrayIcon.Trigger:
            if self.mainWindow.isHidden():
                self.mainWindow.show()
                self.mainWindow.activateWindow()
            else:
                self.mainWindow.hide()

    def showMessage(self, message):
        self.messageDialog.ui.message.setText(unicode(message, 'utf'))
        self.messageDialog.show()

    def refresh(self):
        self.mainWindow.ui.metaList.clear()
        self.copyDialog.ui.notebooks.clear()

        notebooks = config.getNotebooks()

        if not len(notebooks) == 1:
            for i in notebooks:

                backend = config.getBackend(i)
    
                if self.settings['BackendIcons']: icon = self.backendIcons[backend]
                else: icon = ':/x-office-address-book.png'

                item = Qt.QListWidgetItem(Qt.QIcon(icon), unicode(i, 'utf'), self.mainWindow.ui.metaList)
                if not i == self.notebook.name and not backends[backend].ReadOnly:
                    Qt.QListWidgetItem(Qt.QIcon(icon), unicode(i, 'utf'), self.copyDialog.ui.notebooks)
                item.setToolTip(self.trUtf8('Backend: %s' % backend))
                item.type = 'notebook'
        
        if self.settings['Dates']:
            for i in self.notebook.getDates():
                item = Qt.QListWidgetItem(Qt.QIcon(':/history.png'), unicode(i, 'utf'), self.mainWindow.ui.metaList)
                item.type = 'date'

        if self.notebook.backend.Tag:
            for i in self.notebook.getTags():
                item = Qt.QListWidgetItem(Qt.QIcon(':/tag.png'), unicode(i, 'utf'), self.mainWindow.ui.metaList)

                notes = self.notebook.getNotesByTag(i)
                item.setToolTip(unicode('Notes (%i): %s' % (len(notes), ', '.join(notes)), 'utf'))
                item.type = 'tag'

        for i in self.searches:
            item = Qt.QListWidgetItem(Qt.QIcon(':/search.png'), unicode(i, 'utf'), self.mainWindow.ui.metaList)
            item.type = 'search'
        
        # Displaying entries
        self.display(self.parameter)

        # Adding search completer items
        if self.settings['SearchCompletion']:
            self.completer = Qt.QCompleter(['tag:' + unicode(i, 'utf') for i in self.notebook.getTags()] \
            + ['date:' + unicode(i, 'utf') for i in self.notebook.getDates()])
            self.mainWindow.ui.searchEdit.setCompleter(self.completer)

        # Refreshing summary
        status = unicode('Today is %s  Tags: %i  Notes: %i' % \
        ('%d-%d-%d' % localtime()[:3],  self.notebook.getTagsNumber(), self.notebook.getNotesNumber()), 'utf')
        self.mainWindow.ui.statusbar.showMessage(status)
        self.tray.setToolTip(status)

    def openMeta(self, item):
        if item.type == 'tag':
            self.parameter = [self.notebook.getNotesByTag, str(item.text().toUtf8())]
            self.display(self.parameter)
        elif item.type == 'date':
            self.parameter = [self.notebook.getNotesByDate, str(item.text().toUtf8())]
            self.display(self.parameter)
        elif item.type == 'search':
            self.search(item.text())
        elif item.type == 'notebook':
            name = str(item.text().toUtf8())
            try:
                self.setNotebook(name)
                self.parameter = [self.notebook.getNotes]
                self.refresh()
                self.emit(Qt.SIGNAL('notebookChanged()'))
            except Exception, err:
                self.showMessage(str(err))
    
    def openDate(self):
        date = self.mainWindow.ui.dateEdit.date()
        self.parameter = [self.notebook.getNotesByDate, \
        str(date.year()) + '-' + str(date.month()) + '-' + str(date.day())]
        self.display(self.parameter)
    
    def today(self):
        self.parameter = [self.notebook.getNotesByDate, '%d-%d-%d' % localtime()[:3]]
        self.display(self.parameter)
    
    def findRelated(self):
        if len(self.selectedNotes()) == 1:
            self.parameter = [Note(self.currentNote(), self.notebook).findRelated]
            self.display(self.parameter)
    
    def backlinks(self):
        if len(self.selectedNotes()) == 1:
            self.parameter = [Note(self.currentNote(), self.notebook).getBacklinks]
            self.display(self.parameter)
    
    def search(self, text = None):
        if text is None:
            text = self.mainWindow.ui.searchEdit.text()
        self.parameter = [self.notebook.search, str(text.toUtf8()).split(" ")]
        self.display(self.parameter)

    def refreshMenu(self):
        item = self.mainWindow.ui.metaList.currentItem()
        self.mainWindow.ui.actionDeleteNotebook.setVisible(item.type == 'notebook')
        self.mainWindow.ui.actionDeleteTag.setVisible(item.type == 'tag')
        self.mainWindow.ui.actionDeleteSelectedSearch.setVisible(item.type == 'search')   

    def display(self, parameter):
        if len(self.parameter) == 1: entries = self.parameter[0]()
        else: entries = self.parameter[0](self.parameter[1])
        
        self.mainWindow.ui.notesList.clear()
        
        self.mainWindow.ui.numberLabel.setText(self.trUtf8("%i result(s)" % (len(entries))))
        
        for i in entries:
            try:
                note = Note(i, self.notebook)
                item = Qt.QListWidgetItem(Qt.QIcon(':/note.png'), unicode(i, 'utf'), self.mainWindow.ui.notesList)
                
                if self.settings['Tooltips']:
                    text = note.getText()
                    if self.notebook.markup == 'Wiki': 
                        html = text2html(unicode(text, 'utf'))
                    elif self.notebook.markup == 'Code':
                        html = highlight(text, guess_lexer(text), HtmlFormatter(style='colorful'))
                    else: 
                        html = text

                    item.setToolTip(unicode('Title: %s<br>Date: %s<br>Tags: %s<br>Text: %s<br>Length: %i characters' \
                    % (i, note.getDate(), ', '.join(note.getTags()), html, note.getLength()), 'utf'))
            except:
                pass
    
    def new(self, name=None, text=None):
        if self.mainWindow.isHidden():
            self.mainWindow.show()
        tab = EditorWidget(self)
        tab.ui.nameEdit.setEnabled(True)
        if name is None:
            name = 'New note %s' % (datetime.strftime(datetime.today(), '%Y-%m-%d %H-%M-%S'))
        if not text is None:
            tab.ui.textEdit.setText(self.trUtf8(text))
    
        for i in (tab.ui.tagEdit,tab.ui.tagsList, tab.ui.addTagButton,tab.ui.delTagButton, tab.ui.autoTagButton):
            i.setHidden(not self.notebook.backend.Tag)
    
        tab.ui.nameEdit.setText(unicode(name, 'utf'))
        tab.ui.date.setText('%d-%d-%d' % localtime()[:3])
        self.mainWindow.ui.tabWidget.addTab(tab, name)
        self.mainWindow.ui.tabWidget.setCurrentIndex(self.mainWindow.ui.tabWidget.indexOf(tab))
        self.mainWindow.ui.tabWidget.setTabIcon(self.mainWindow.ui.tabWidget.indexOf(tab), Qt.QIcon(':/note.png'))
        tab.ui.nameEdit.setFocus()
    
    def openNote(self, entry):
        if self.mainWindow.isHidden():
            self.mainWindow.show()
            
        tab = EditorWidget(self)
    
        # Open preview mode by default
        tab.ui.tabWidget.setCurrentIndex(0)
    
        # Disabling namebar
        tab.ui.nameEdit.setEnabled(False)
    
        # Setting name
        tab.ui.nameEdit.setText(unicode(entry, 'utf'))
    
        # Creating Note instance
        note = Note(entry, self.notebook)
        tab.note = note
        tab.ui.date.setText(self.trUtf8(note.getDate()))
        text = note.getText()
        tab.ui.textEdit.setPlainText(unicode(note.getText(), 'utf'))
    
        # Displaying tags
        for i in (tab.ui.tagEdit, tab.ui.tagsList, tab.ui.addTagButton, tab.ui.delTagButton, tab.ui.autoTagButton):
            i.setHidden(not note.notebook.backend.Tag)
    
        if note.notebook.backend.Tag:
            for tag in note.getTags():
                item = Qt.QListWidgetItem(Qt.QIcon(':/tag.png'), unicode(tag, 'utf'), tab.ui.tagsList)
                notes = self.notebook.getNotesByTag(tag)
                item.setToolTip(self.trUtf8('Tag: %s<br>Notes (%i): %s' % (tag, len(notes), ', '.join(notes))))

        self.mainWindow.ui.tabWidget.addTab(tab, "")
        self.mainWindow.ui.tabWidget.setCurrentIndex(self.mainWindow.ui.tabWidget.indexOf(tab))
        self.mainWindow.ui.tabWidget.setTabText(self.mainWindow.ui.tabWidget.indexOf(tab), unicode(entry, 'utf'))
        self.mainWindow.ui.tabWidget.setTabIcon(self.mainWindow.ui.tabWidget.indexOf(tab), Qt.QIcon(':/note.png'))
        
        # If search was performed:
        if self.parameter[0] == self.notebook.search:
            if len(self.parameter[1]) == 1:
                searchtext = self.trUtf8(self.parameter[1][0])
                tab.ui.searchEdit.setText(searchtext)
                tab.find(searchtext)
    
    def saveNote(self):
        tab = self.mainWindow.ui.tabWidget.currentIndex()
        if tab != 0: 
            widget = self.currentWidget()
            text = str(widget.ui.textEdit.toPlainText().toUtf8())
            tags = widget.tags()
            
            if not hasattr(widget, "note"):
                widget.note = Note(str(widget.ui.nameEdit.text().toUtf8()), self.notebook)
                self.mainWindow.ui.tabWidget.setTabText(self.mainWindow.ui.tabWidget.indexOf(widget), unicode(widget.note.name, 'utf'))
            
            try:
                widget.note.write(text)
                widget.note.tag(tags)
                self.emit(Qt.SIGNAL("notesModified()"))
                widget.ui.nameEdit.setEnabled(False)
                widget.refresh()
            except:
                self.showMessage('Failed to save entry')

    def buildListIndex(self):
        self.new(text='\n'.join(["* [[" + i + "]]" for i in self.selectedNotes()]))
    
    def merge(self):
        self.new(text='\n----\n'.join(["[[" + note + "]]\n\n" + Note(note, self.notebook).getText() for note in self.selectedNotes()]))
    
    def currentNote(self):
        note = None
        index = self.mainWindow.ui.notesList.currentRow()
        item = self.mainWindow.ui.notesList.item(index)
        if not item is None:
            note = str(item.text().toUtf8())
        return note
    
    def openFromList(self):
        self.openNote(self.currentNote())
    
    def selectedNotes(self):
        return ([str(item.text().toUtf8()) for item in self.mainWindow.ui.notesList.selectedItems()])
    
    def email(self):
        if len(self.selectedNotes()) == 1:
            name = self.currentNote()
            if not name is None:
                note = Note(name, self.notebook)
                Qt.QDesktopServices.openUrl(Qt.QUrl(unicode('mailto:?subject=%s&body=%s' % (note.name, note.getText()), 'utf')))

    def openExternally(self):
        if len(self.selectedNotes()) == 1:
            name = self.currentNote()
            if not name is None:
                Qt.QDesktopServices().openUrl(Qt.QUrl(unicode(Note(name, self.notebook).getURL(), 'utf')))
    
    def deleteNotes(self):
        for note in self.selectedNotes(): Note(note, self.notebook).delete()
        self.emit(Qt.SIGNAL('notesModified()'))
   
    def renameNote(self):
        if len(self.selectedNotes()) == 1:
            name = str(self.renameDialog.ui.lineEdit.text().toUtf8())
            if name != '' and not name in self.notebook.getNotes():
                    Note(self.currentNote(), self.notebook).rename(name)
                    self.emit(Qt.SIGNAL('notesModified()'))
        else:
            self.showMessage('Only 1 note can be renamed at a time')

    def copyEntry(self):
        for note in self.selectedNotes():
            Note(note, self.notebook).copyToNotebook(\
            [str(item.text().toUtf8()) for item in self.copyDialog.ui.notebooks.selectedItems()],\
            move=self.copyDialog.ui.deleteBox.isChecked())
        self.emit(Qt.SIGNAL('notesModified()'))

    def addNotebook(self):
        """ Adds notebook """
        config.addNotebook(
            str(self.notebookDialog.ui.nameEdit.text().toUtf8()),
            str(self.notebookDialog.ui.backends.currentText().toUtf8()),
            str(self.notebookDialog.ui.markups.currentText().toUtf8()),
            [str(i.text().toUtf8()) for i in
                (
                self.notebookDialog.ui.pathEdit,
                self.notebookDialog.ui.urlEdit,
                self.notebookDialog.ui.loginEdit,
                self.notebookDialog.ui.passwdEdit
                )
                if self.notebookDialog.settings[i]
             ]
        )
        self.emit(Qt.SIGNAL('notesModified()'))
    
    def deleteNotebook(self):
        notebook = str(self.mainWindow.ui.metaList.currentItem().text().toUtf8())
        if not notebook == self.notebook.name:
            config.deleteNotebook(notebook)
            self.emit(Qt.SIGNAL('notesModified()'))
        else:
            self.showMessage('This notebook is active now')

    def addTag(self):
        tag = str(self.addTagDialog.ui.lineEdit.text().toUtf8())
        if tag != '' and not tag in self.notebook.getTags():
            self.notebook.addTag(tag)
            self.emit(Qt.SIGNAL('notesModified()'))
    
    def deleteTag(self):
        self.notebook.deleteTag(str(self.mainWindow.ui.metaList.currentItem().text().toUtf8()))
        self.emit(Qt.SIGNAL('notesModified()'))
    
    def showAll(self):
        self.parameter = [self.notebook.getNotes]
        self.display(self.parameter)
    
    def saveSearch(self):
        searchText = str(self.mainWindow.ui.searchEdit.text().toUtf8())
        if searchText != '' and not searchText in self.searches:
            self.searches.append(searchText)
            pickle.dump(self.searches, open(self.searchesFile, 'w'))
            self.emit(Qt.SIGNAL('notesModified()'))

    def deleteSearch(self):
        item = self.mainWindow.ui.metaList.currentItem()
        if not item is None and item.type == 'search':
            self.searches.remove(str(item.text().toUtf8()))
            pickle.dump(self.searches, open(self.searchesFile, 'w'))
            self.emit(Qt.SIGNAL('notesModified()'))

    def currentWidget(self):
        return self.mainWindow.ui.tabWidget.currentWidget()

    def getSelection(self):
        return self.currentWidget().ui.textEdit.textCursor().selectedText()

    def insertMarkup(self, ft, et, text=None):
        if not self.mainWindow.ui.tabWidget.currentIndex() == 0:
            if text is None:
                text = self.getSelection()
            self.currentWidget().ui.textEdit.insertPlainText(ft + text + et)
    
    def bold(self):
        if self.notebook.markup == 'Wiki':
            ft = et = '**'
        else:
            ft = '<b>'
            et = '</b>'
        self.insertMarkup(ft, et)

    def italic(self):
        if self.notebook.markup == 'Wiki':
            ft = et = '//'
        else:
            ft = '<i>'
            et = '</i>'
        self.insertMarkup(ft, et)
    
    def underline(self):
        if self.notebook.markup == 'Wiki':
            ft = et = '__'
        else:
            ft = '<u>'
            et = '</u>'
        self.insertMarkup(ft, et)
    
    def highlight(self):
        if self.notebook.markup == 'Wiki':
            ft = et = '%%'
        else:
            ft = '<span style="background: yellow;">'
            et = '</span>'
        self.insertMarkup(ft, et)
   
    def image(self):
        fileDialog = Qt.QFileDialog()
        fileDialog.setWindowTitle(self.trUtf8('Select image'))
        fileDialog.setFileMode(fileDialog.ExistingFile)
        fileDialog.setAcceptMode(fileDialog.AcceptOpen)
        fileDialog.exec_()
        path = fileDialog.selectedFiles()[0]
        
        if self.notebook.markup == 'Wiki':
            ft = '{{'
            et = '}}'
        else:
            ft = '<img src="'
            et = '">'
        self.insertMarkup(ft, et, path)

    def list(self):
        if self.notebook.markup == 'Wiki':
            ft = '* '
            et = ''
            fl = ''
            el = ''
        else:
            ft = '<li>'
            et = '</li>'
            fl = '<ul>'
            el = '</ul>'
        
        self.insertMarkup(fl, el, text=unicode('\n'.join([ft + i + et for i in str(self.getSelection().toUtf8()).split('\xe2\x80\xa9')]), 'utf'))
        
    
    def insertTime(self):
        self.insertMarkup('', '', datetime.strftime(datetime.today(), '%Y-%m-%d, %H:%M:%S'))

    def closeEvent(self, event):
        self.mainWindow.hide()
        event.ignore()

    def run(self):
        self.mainWindow.show()
        sys.exit(self.application.exec_())
    
Application().run()