# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/gforgx/UI_I/editor_widget.ui'
#
# Created: Tue Nov 25 19:33:02 2008
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(760, 659)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtGui.QFrame(Form)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_3 = QtGui.QGridLayout(self.frame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1)
        self.nameEdit = QtGui.QLineEdit(self.frame)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout_3.addWidget(self.nameEdit, 1, 1, 1, 1)
        self.addTagButton = QtGui.QToolButton(self.frame)
        self.addTagButton.setObjectName("addTagButton")
        self.gridLayout_3.addWidget(self.addTagButton, 4, 4, 1, 1)
        self.delTagButton = QtGui.QToolButton(self.frame)
        self.delTagButton.setObjectName("delTagButton")
        self.gridLayout_3.addWidget(self.delTagButton, 4, 5, 1, 1)
        self.autoTagButton = QtGui.QToolButton(self.frame)
        self.autoTagButton.setObjectName("autoTagButton")
        self.gridLayout_3.addWidget(self.autoTagButton, 4, 2, 1, 1)
        self.tagsList = QtGui.QListWidget(self.frame)
        self.tagsList.setObjectName("tagsList")
        self.gridLayout_3.addWidget(self.tagsList, 1, 2, 2, 4)
        self.dateLabel = QtGui.QLabel(self.frame)
        self.dateLabel.setObjectName("dateLabel")
        self.gridLayout_3.addWidget(self.dateLabel, 2, 0, 1, 1)
        self.date = QtGui.QLineEdit(self.frame)
        self.date.setEnabled(False)
        self.date.setObjectName("date")
        self.gridLayout_3.addWidget(self.date, 2, 1, 1, 1)
        self.tagEdit = QtGui.QComboBox(self.frame)
        self.tagEdit.setEditable(True)
        self.tagEdit.setObjectName("tagEdit")
        self.gridLayout_3.addWidget(self.tagEdit, 4, 3, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.South)
        self.tabWidget.setObjectName("tabWidget")
        self.view = QtGui.QWidget()
        self.view.setObjectName("view")
        self.gridLayout_2 = QtGui.QGridLayout(self.view)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textBrowser = QtGui.QTextBrowser(self.view)
        self.textBrowser.setOpenExternalLinks(False)
        self.textBrowser.setOpenLinks(False)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_2.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.tabWidget.addTab(self.view, "")
        self.edit = QtGui.QWidget()
        self.edit.setObjectName("edit")
        self.gridLayout_4 = QtGui.QGridLayout(self.edit)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.textEdit = QtGui.QTextEdit(self.edit)
        self.textEdit.setAcceptRichText(False)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_4.addWidget(self.textEdit, 0, 0, 1, 1)
        self.tabWidget.addTab(self.edit, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.searchEdit = QtGui.QLineEdit(Form)
        self.searchEdit.setObjectName("searchEdit")
        self.horizontalLayout.addWidget(self.searchEdit)
        self.findButton = QtGui.QToolButton(Form)
        self.findButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.findButton.setObjectName("findButton")
        self.horizontalLayout.addWidget(self.findButton)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Title: ", None, QtGui.QApplication.UnicodeUTF8))
        self.addTagButton.setToolTip(QtGui.QApplication.translate("Form", "Assign entered tag", None, QtGui.QApplication.UnicodeUTF8))
        self.addTagButton.setText(QtGui.QApplication.translate("Form", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.delTagButton.setToolTip(QtGui.QApplication.translate("Form", "Remove selected tag", None, QtGui.QApplication.UnicodeUTF8))
        self.delTagButton.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.delTagButton.setShortcut(QtGui.QApplication.translate("Form", "Del", None, QtGui.QApplication.UnicodeUTF8))
        self.autoTagButton.setToolTip(QtGui.QApplication.translate("Form", "Assign tags automatically", None, QtGui.QApplication.UnicodeUTF8))
        self.dateLabel.setText(QtGui.QApplication.translate("Form", "Date", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.view), QtGui.QApplication.translate("Form", "Rich Text", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.edit), QtGui.QApplication.translate("Form", "Wiki source", None, QtGui.QApplication.UnicodeUTF8))
        self.findButton.setText(QtGui.QApplication.translate("Form", "Find", None, QtGui.QApplication.UnicodeUTF8))

import notefinder_rc
