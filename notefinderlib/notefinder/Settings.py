# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/gforgx/UI/settings.ui'
#
# Created: Mon Oct 27 20:15:20 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        SettingsDialog.resize(323, 257)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/preferences.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SettingsDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(SettingsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtGui.QDialogButtonBox(SettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(SettingsDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.showMetaPanel = QtGui.QCheckBox(self.tab)
        self.showMetaPanel.setObjectName("showMetaPanel")
        self.verticalLayout.addWidget(self.showMetaPanel)
        self.backendIcons = QtGui.QCheckBox(self.tab)
        self.backendIcons.setObjectName("backendIcons")
        self.verticalLayout.addWidget(self.backendIcons)
        self.showDates = QtGui.QCheckBox(self.tab)
        self.showDates.setObjectName("showDates")
        self.verticalLayout.addWidget(self.showDates)
        self.toolTips = QtGui.QCheckBox(self.tab)
        self.toolTips.setObjectName("toolTips")
        self.verticalLayout.addWidget(self.toolTips)
        self.trayIcon = QtGui.QCheckBox(self.tab)
        self.trayIcon.setObjectName("trayIcon")
        self.verticalLayout.addWidget(self.trayIcon)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.tabWidget.addTab(self.tab, icon, "")
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.searchCompletion = QtGui.QCheckBox(self.tab_4)
        self.searchCompletion.setObjectName("searchCompletion")
        self.verticalLayout_3.addWidget(self.searchCompletion)
        self.searchOnTheFly = QtGui.QCheckBox(self.tab_4)
        self.searchOnTheFly.setObjectName("searchOnTheFly")
        self.verticalLayout_3.addWidget(self.searchOnTheFly)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_4, icon1, "")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.autoSave = QtGui.QCheckBox(self.tab_3)
        self.autoSave.setObjectName("autoSave")
        self.verticalLayout_2.addWidget(self.autoSave)
        self.label = QtGui.QLabel(self.tab_3)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/rename.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_3, icon2, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_2 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.listWidget = QtGui.QListWidget(self.tab_2)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout_2.addWidget(self.listWidget, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(SettingsDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), SettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), SettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QtGui.QApplication.translate("SettingsDialog", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.showMetaPanel.setText(QtGui.QApplication.translate("SettingsDialog", "Show meta panel", None, QtGui.QApplication.UnicodeUTF8))
        self.backendIcons.setText(QtGui.QApplication.translate("SettingsDialog", "Show backend icons", None, QtGui.QApplication.UnicodeUTF8))
        self.showDates.setText(QtGui.QApplication.translate("SettingsDialog", "Show dates", None, QtGui.QApplication.UnicodeUTF8))
        self.toolTips.setText(QtGui.QApplication.translate("SettingsDialog", "Show tooltips", None, QtGui.QApplication.UnicodeUTF8))
        self.trayIcon.setText(QtGui.QApplication.translate("SettingsDialog", "Tray icon", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("SettingsDialog", "Interface", None, QtGui.QApplication.UnicodeUTF8))
        self.searchCompletion.setText(QtGui.QApplication.translate("SettingsDialog", "Search completion", None, QtGui.QApplication.UnicodeUTF8))
        self.searchOnTheFly.setText(QtGui.QApplication.translate("SettingsDialog", "Search on-the-fly", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("SettingsDialog", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.autoSave.setText(QtGui.QApplication.translate("SettingsDialog", "Autosave", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SettingsDialog", "Note: may be very slow for networked notebook", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("SettingsDialog", "Editing", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("SettingsDialog", "Plugins", None, QtGui.QApplication.UnicodeUTF8))

import notefinder_rc