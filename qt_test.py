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
import readconf
import os

class CommentedFile:
    def __init__(self, f, commentstring="#"):
        self.f = f
        self.commentstring = commentstring
    def next(self):
        line = self.f.next()
        while line.startswith(self.commentstring):
            line = self.f.next()
        return line
    def __iter__(self):
        return self

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.curConf=readconf.readConf(os.path.expanduser('~')+"/.config/pztimer/config.ini")
        
        self.initUI()        
        
    def initUI(self):
        
        colnames = ["task","status","created","tags"]
        rMinusIcon = QtGui.QPixmap("Resources/button_minus_red.png")
        rPlusIcon = QtGui.QPixmap("Resources/button_plus_green.png")
        rLoadIcon = QtGui.QPixmap("Resources/load.png")
        rWriteIcon = QtGui.QPixmap("Resources/write.png")        
        
        self.setGeometry(300, 300, 500, 210)
        self.setWindowTitle('Icon3')
        self.setWindowIcon(QtGui.QIcon('web.png'))        
    
        self.model = QtGui.QStandardItemModel(self)
        
        for i in range(len(colnames)) :
            self.model.setHeaderData(i, QtCore.Qt.Horizontal, colnames[i])
        #self.model.setHeaderData(1, QtCore.Qt.Horizontal, colnames[1])
        self.model.setHorizontalHeaderLabels(colnames)
 
        self.tableView = QtGui.QTableView(self)
        #self.tableView = QtGui.QTableWidget(self)
        self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(0,250)
        self.tableView.setColumnWidth(1,50)
        self.tableView.setColumnWidth(2,100)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        #self.tableView.setHorizontalHeaderLabels(['a', 'b', 'c', 'd', 'e'])
 
        self.pushButtonLoad = QtGui.QPushButton(self)
        self.pushButtonLoad.setIcon(QtGui.QIcon(rLoadIcon))
        self.pushButtonLoad.setToolTip("Load Csv File!")
        self.pushButtonLoad.clicked.connect(self.on_pushButtonLoad_clicked)
 
        self.pushButtonWrite = QtGui.QPushButton(self)
        self.pushButtonWrite.setIcon(QtGui.QIcon(rWriteIcon))        
        self.pushButtonWrite.setToolTip("Write Csv File!")
        self.pushButtonWrite.clicked.connect(self.on_pushButtonWrite_clicked)
        
        self.pushButtonRemove = QtGui.QPushButton(self)
        self.pushButtonRemove.setIcon(QtGui.QIcon(rMinusIcon))
        self.pushButtonRemove.setToolTip("Remove Task Permanently")
        #self.pushButtonRemove.setText("Remove Line")
        self.pushButtonRemove.clicked.connect(self.on_pushButtonRemove_clicked)
        
        self.pushButtonAdd = QtGui.QPushButton(self)
        self.pushButtonAdd.setIcon(QtGui.QIcon(rPlusIcon))
        self.pushButtonAdd.setToolTip("Add Task")        
        #self.pushButtonAdd.setText("Add Task")
        self.pushButtonAdd.clicked.connect(self.on_pushButtonAdd_clicked)
        
        self.checkShowDone = QtGui.QCheckBox("ShowDone",self)
        if int(self.curConf.config["ShowDone"])!=0 :
            self.checkShowDone.setCheckState(QtCore.Qt.Checked)
        else :
            self.checkShowDone.setCheckState(QtCore.Qt.Unchecked)
        self.checkShowDone.stateChanged.connect(self.on_checkbox_changed)
#         self.pushButtonAdd.clicked.connect(self.on_pushButtonAdd_clicked)        
        
#         self.layoutVertical = QtGui.QVBoxLayout(self)
#         self.layoutVertical.addWidget(self.tableView)
#         self.layoutVertical.addWidget(self.pushButtonLoad)
#         self.layoutVertical.addWidget(self.pushButtonWrite)
#         self.layoutVertical.addWidget(self.pushButtonRemove)
        self.buttonLayout = QtGui.QGridLayout(self)
        self.buttonLayout.addWidget(self.pushButtonLoad,0,0)
        self.buttonLayout.addWidget(self.pushButtonWrite,0,1)
        self.buttonLayout.addWidget(self.pushButtonAdd,0,2)
        self.buttonLayout.addWidget(self.pushButtonRemove,0,3)
        self.buttonLayout.addWidget(self.tableView,1,0,1,4)        
        self.buttonLayout.addWidget(self.checkShowDone,2,0)        
                        

    def clearModel(self):
        self.model.clear()

    def loadCsv(self, fileName):
        self.clearModel()        
        with open(fileName, "rb") as fileInput:
            for row in csv.reader(fileInput,delimiter=';'):
                if ''.join(row).strip() :
                    
                    items = [
                             QtGui.QStandardItem(field)
                             for field in row
                             ]                    
                    items[0], items[1] = items[1], items[0]
                    if str(items[1].text()).isdigit() :
                        if ( (int(items[1].text())!=0) or (int(self.curConf.config["ShowDone"])!=0) ) :
                            self.model.appendRow(items)
                    else :
                        self.model.appendRow(items)

    def writeCsv(self, fileName):
        with open(fileName, "wb") as fileOutput:        
            writer = csv.writer(fileOutput,delimiter=';')
            for rowNumber in range(self.model.rowCount()):
                fields = [
                    self.model.data(
                        self.model.index(rowNumber, columnNumber),
                        QtCore.Qt.DisplayRole
                    )
                    for columnNumber in range(self.model.columnCount())
                ]
                fields=[ str(x.toString()) for x in fields ]
                print(fields)
                writer.writerow(fields)                
                
    def removeLine(self):
        #print [ x.row() for x in self.tableView.selectionModel().selection().indexes() ]
        selection=self.tableView.selectionModel().selectedRows()
        print selection
        for cur in selection :
            #print cur.row()
            self.model.removeRow(cur.row())                
    
    def addLine(self):
        self.model.appendRow([])        

    def changeConf(self):
        if  self.checkShowDone.checkState() == QtCore.Qt.Checked :
            self.curConf.config["ShowDone"]=1
        else :
            self.curConf.config["ShowDone"]=0
        self.curConf.writeShowDoneConf(self.curConf.config["ShowDone"])
        self.loadCsv("/home/paul/.doit")        


#=========EVENTS    
    @QtCore.pyqtSlot()
    def on_pushButtonWrite_clicked(self):
        self.writeCsv("/home/paul/.doit")

    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        #self.loadCsv(self.fileName)
        self.loadCsv("/home/paul/.doit")
        
    @QtCore.pyqtSlot()
    def on_pushButtonRemove_clicked(self):
        self.removeLine()
      

    @QtCore.pyqtSlot()
    def on_pushButtonAdd_clicked(self):
        self.addLine()

    @QtCore.pyqtSlot()
    def on_checkbox_changed(self):
        self.changeConf()        
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()   
