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
from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()        
        
    def initUI(self):
        
        colnames = ["task","status"]
        
        self.setGeometry(300, 300, 250, 190)
        self.setWindowTitle('Icon3')
        self.setWindowIcon(QtGui.QIcon('web.png'))        
    
        self.model = QtGui.QStandardItemModel(self)
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, colnames[0])
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, colnames[1])
        self.model.setHorizontalHeaderLabels(colnames)
 
        self.tableView = QtGui.QTableView(self)
        #self.tableView = QtGui.QTableWidget(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        #self.tableView.setHorizontalHeaderLabels(['a', 'b', 'c', 'd', 'e'])
 
        self.pushButtonLoad = QtGui.QPushButton(self)
        self.pushButtonLoad.setText("Load Csv File!")
        self.pushButtonLoad.clicked.connect(self.on_pushButtonLoad_clicked)
 
        self.pushButtonWrite = QtGui.QPushButton(self)
        self.pushButtonWrite.setText("Write Csv File!")
        self.pushButtonWrite.clicked.connect(self.on_pushButtonWrite_clicked)
 
        self.layoutVertical = QtGui.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.tableView)
        self.layoutVertical.addWidget(self.pushButtonLoad)
        self.layoutVertical.addWidget(self.pushButtonWrite)

    def loadCsv(self, fileName):
        with open(fileName, "rb") as fileInput:
            for row in csv.reader(fileInput,delimiter=';'):    
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]
                self.model.appendRow(items)

    def writeCsv(self, fileName):
        with open(fileName, "wb") as fileOutput:
            writer = csv.writer(fileOutput)
            for rowNumber in range(self.model.rowCount()):
                fields = [
                    self.model.data(
                        self.model.index(rowNumber, columnNumber),
                        QtCore.Qt.DisplayRole
                    )
                    for columnNumber in range(self.model.columnCount())
                ]
                writer.writerow(fields)                
    
    @QtCore.pyqtSlot()
    def on_pushButtonWrite_clicked(self):
        self.writeCsv("/home/paul/.doit")

    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        #self.loadCsv(self.fileName)
        self.loadCsv("/home/paul/.doit")
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()   
