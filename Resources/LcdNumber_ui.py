# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LcdNumber.ui'
#
# Created: Sun Apr  4 22:10:24 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")

        Form.resize(14, 35)
        self.lcdNumber = QtGui.QLCDNumber(Form)
        self.lcdNumber.setGeometry(QtCore.QRect(1, 1, 65, 31))
        # self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)

        self.retranslateUi(Form)

        QtCore.QMetaObject.connectSlotsByName(Form)
        print(type)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
