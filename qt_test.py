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

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.curConf=readconf.readConf(os.path.expanduser('~')+"/.config/pztimer/config.ini")
        self.colnames = ["task","status","created","tags"]
        
        self.initUI()
        
    def closeEvent(self, event):
        if QtGui.QMessageBox.question(None, '', "Are you sure you want to quit?",
                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                            QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes :
            event.accept() # let the window close
        else:
            event.ignore()
            
        
    def initUI(self):        
        
        rMinusIcon = QtGui.QPixmap("Resources/button_minus_red.png")
        rPlusIcon = QtGui.QPixmap("Resources/button_plus_green.png")
        rLoadIcon = QtGui.QPixmap("Resources/load.png")
        rWriteIcon = QtGui.QPixmap("Resources/write.png")
        rDoneIcon = QtGui.QPixmap("Resources/done.png")               
        rUnDoneIcon = QtGui.QPixmap("Resources/undone.png")        
        
        self.setGeometry(300, 300, 600, 310)
        self.setWindowTitle('pzTimer')
        self.setWindowIcon(QtGui.QIcon('web.png'))
        
        #self.model = QtGui.QStandardItemModel(self)
        self.model = Model()        
        
        for i in range(len(self.colnames)) :
            self.model.setHeaderData(i, QtCore.Qt.Horizontal, self.colnames[i])
        #self.model.setHeaderData(1, QtCore.Qt.Horizontal, self.colnames[1])
        self.model.setHorizontalHeaderLabels(self.colnames)
 
        self.tableView = QtGui.QTableView(self)
        self.setTableView()
 
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
        
        self.pushButtonDone = QtGui.QPushButton(self)
        self.pushButtonDone.setIcon(QtGui.QIcon(rDoneIcon))
        self.pushButtonDone.setToolTip("Comment/Mark task as Done")        
        self.pushButtonDone.clicked.connect(self.on_pushButtonDone_clicked)
        
        self.pushButtonUnDone = QtGui.QPushButton(self)
        self.pushButtonUnDone.setIcon(QtGui.QIcon(rUnDoneIcon))
        self.pushButtonUnDone.setToolTip("UnComment task")        
        self.pushButtonUnDone.clicked.connect(self.on_pushButtonUnDone_clicked)                
        
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
        self.buttonLayout.addWidget(self.pushButtonDone,0,3)
        self.buttonLayout.addWidget(self.pushButtonUnDone,0,4)        
        self.buttonLayout.addWidget(self.pushButtonRemove,0,5)
        self.buttonLayout.addWidget(self.tableView,1,0,1,6)        
        self.buttonLayout.addWidget(self.checkShowDone,2,0)        
                        



    def clearModel(self):
        self.model.clear()
        
    def setTableView(self):
        #self.tableView = QtGui.QTableWidget(self)
        self.tableView.setModel(self.model)        
        self.tableView.setColumnWidth(0,350)
        self.tableView.setColumnWidth(1,50)
        self.tableView.setColumnWidth(2,50)
        self.tableView.setColumnWidth(2,100)        
        self.tableView.horizontalHeader().setStretchLastSection(True)
        #self.tableView.setHorizontalHeaderLabels(['a', 'b', 'c', 'd', 'e'])        

    def loadCsv(self, fileName):
        self.clearModel()
        fileInput=open(fileName, "rb")
        for row in csv.reader(fileInput,delimiter=';'):
            if ''.join(row).strip() :                                    
                items = [
                         QtGui.QStandardItem(field)
                         for field in row
                         ]                    
#                 items[0], items[1] = items[1], items[0]
            if (int(self.curConf.config["ShowDone"])==0) and (str((items[0]).text()).startswith("#")) :
                self.model.appendRow(items)
                self.tableView.setRowHidden(self.model.rowCount()-1,True)
            else :
                self.model.appendRow(items)                
        self.model.setHorizontalHeaderLabels(self.colnames)
        self.setTableView()

    def writeCsv(self, fileName):
        os.rename(os.path.realpath(fileName), os.path.realpath(fileName)+"~")

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
#                 fields[0], fields[1] = fields[1], fields[0]
                fields=[ str(x.toString()) for x in fields ]
                print(fields)
                writer.writerow(fields)
        fileOutput.close()                
                
    def removeLine(self):
        #print [ x.row() for x in self.tableView.selectionModel().selection().indexes() ]
        selection=self.tableView.selectionModel().selectedRows()
        print selection
        for cur in selection :
            #print cur.row()
            self.model.removeRow(cur.row())                
            
    def markDone(self):
        selection=self.tableView.selectionModel().selectedRows()
        for cur in selection :            
            # print cur.row()
#             print self.model.item(cur.row(),0).data(QtCore.Qt.DisplayRole).toString()
            if not str(self.model.item(cur.row(),0).data(QtCore.Qt.DisplayRole).toString()).startswith("#") :
                self.model.item(cur.row(),0).setData("#"+self.model.item(cur.row(),0).data(QtCore.Qt.DisplayRole).toString(),QtCore.Qt.EditRole)
            self.writeCsv("/home/paul/.doit")    
            self.loadCsv("/home/paul/.doit")
            
    def markUnDone(self):
        selection=self.tableView.selectionModel().selectedRows()
        for cur in selection :            
            if str(self.model.item(cur.row(),0).data(QtCore.Qt.DisplayRole).toString()).startswith("#") :
                self.model.item(cur.row(),0).setData(self.model.item(cur.row(),0).data(QtCore.Qt.DisplayRole).toString()[1:],QtCore.Qt.EditRole)
            self.writeCsv("/home/paul/.doit")    
            self.loadCsv("/home/paul/.doit")        
    
    def addLine(self):
        import datetime
        cur_date=datetime.datetime.now()
        self.model.appendRow([QtGui.QStandardItem(""),QtGui.QStandardItem("0"),QtGui.QStandardItem(cur_date.strftime('%Y-%m-%d')),QtGui.QStandardItem("")])
#         self.model.appendRow([])        

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
    def on_pushButtonDone_clicked(self):
        self.markDone()

    @QtCore.pyqtSlot()
    def on_pushButtonUnDone_clicked(self):
        self.markUnDone()        

    @QtCore.pyqtSlot()
    def on_checkbox_changed(self):
        self.changeConf()        

def sigint_handler(*args):
    """Handler for the SIGINT signal."""
    sys.stderr.write('\r')

        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()   
