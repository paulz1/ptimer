#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

In this example, we create a simple
window in PyQt4.

author: Jan Bodnar
website: zetcode.com 
last edited: October 2011
"""

import sys
import csv
from PyQt4 import QtGui, QtCore, uic
import readconf
import os
import example
from pztimer import Timer

class Model(QtGui.QStandardItemModel):

    def __init__(self, parent = None):

        QtGui.QStandardItemModel.__init__(self, parent)

    def data(self, index, role):        
#         print index.data().toString()
        model=index.model()
#        print QtGui.QStandardItemModel.data(self,model.index(index.row(), 0),QtCore.Qt.DisplayRole).toString()
#        if index.row() == 3 and role == QtCore.Qt.BackgroundRole:
        if str(QtGui.QStandardItemModel.data(self,model.index(index.row(), 0),QtCore.Qt.DisplayRole).toString()).startswith("#") and role == QtCore.Qt.BackgroundRole:            
            return QtCore.QVariant(QtGui.QBrush(QtCore.Qt.gray))                
        else:
            return QtGui.QStandardItemModel.data(self, index, role)

#form = uic.loadUiType("untitled2.ui")[0]
#print form

class MyMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
#        super(MyMainWindow, self).__init__()
        QtGui.QMainWindow.__init__(self, parent)        
        self.ex=example.Example()
        self.setGeometry(300, 300, 600, 310)
        self.setCentralWidget(self.ex)
        

def main():
    
    app = QtGui.QApplication(sys.argv)
    
#     ex = Example()
#     ex.show()
    
    myWindow = MyMainWindow()
    myWindow.show() 

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()   
