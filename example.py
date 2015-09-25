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
from pztimer import Timer

MIN_POMODORO_BEFORE_REST = 4

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
#class Example(QtGui.QMainWindow,form):
    
    def __init__(self):
        super(Example, self).__init__()
        self.curConf=readconf.readConf(os.path.expanduser('~')+"/.config/pztimer/config.ini")
        self.colnames = ["task","status","created","tags"]
        self.current_job=None
        self.jobs_done = 0
        
        self.initUI()
        
    def closeEvent(self, event):
        """
        pass
        """
#         if QtGui.QMessageBox.question(None, '', "Are you sure you want to quit?",
#                             QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
#                             QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes :
#             event.accept() # let the window close
#         else:
#             event.ignore()

        self.hide()
        event.ignore()
        
#         if self.trayMsgDisplayed == False:
#             
#             QtGui.QMessageBox.information(self, "Systray",
#                     "The program will keep running in the system tray. To "
#                     "terminate the program, choose <b>Quit</b> in the "
#                     "context menu of the system tray entry.")
#             self.hide()
#             event.ignore()
#             self.trayMsgDisplayed = True

    def unhideWindow(self):
        self.show()           
        
    def initUI(self):
        
        app_path=os.path.dirname(__file__)
#         print app_path 
        
        rMinusIcon = QtGui.QPixmap(os.path.join(app_path,"Resources/button_minus_red.png"))
        rPlusIcon = QtGui.QPixmap(os.path.join(app_path,"Resources/button_plus_green.png"))
#        rLoadIcon = QtGui.QPixmap(":Icons/load.png")
        rWriteIcon = QtGui.QPixmap(os.path.join(app_path,"Resources/write.png"))
        rDoneIcon = QtGui.QPixmap(os.path.join(app_path,"Resources/done.png"))            
        rUnDoneIcon = QtGui.QPixmap(os.path.join(app_path,"Resources/undone.png"))
        rStartAlarm = QtGui.QPixmap(os.path.join(app_path,"Resources/start_alarm.png"))
        rStopAlarm = QtGui.QPixmap(os.path.join(app_path,"Resources/stop_alarm.png"))
        # Icon made by Freepik from www.flaticon.com
        rRest = QtGui.QPixmap(os.path.join(app_path,"Resources/rest.png"))
        
        self.setGeometry(300, 300, 600, 330)
        self.setWindowTitle('pzTimer')
        self.setWindowIcon(QtGui.QIcon(os.path.join(app_path,'web.png')))
        
        #self.model = QtGui.QStandardItemModel(self)
        self.model = Model()
        self.model.itemChanged.connect(self.on_dataChanged)
        
        for i in range(len(self.colnames)) :
            self.model.setHeaderData(i, QtCore.Qt.Horizontal, self.colnames[i])
        self.model.setHorizontalHeaderLabels(self.colnames)
 
        self.tableView = QtGui.QTableView(self)
        self.setTableView()
        self.loadCsv("/home/paul/.doit")
 
#         self.pushButtonLoad = QtGui.QPushButton(self)
#         self.pushButtonLoad.setIcon(QtGui.QIcon(rLoadIcon))
#         self.pushButtonLoad.setToolTip("Load Csv File!")
#         self.pushButtonLoad.clicked.connect(self.on_pushButtonLoad_clicked)
 
        self.pushButtonWrite = QtGui.QPushButton(self)
        self.pushButtonWrite.setIcon(QtGui.QIcon(rWriteIcon))        
        self.pushButtonWrite.setToolTip("Write Csv File!")
        self.pushButtonWrite.clicked.connect(self.on_pushButtonWrite_clicked)
        
        self.pushButtonRemove = QtGui.QPushButton(self)
        self.pushButtonRemove.setIcon(QtGui.QIcon(rMinusIcon))
        self.pushButtonRemove.setToolTip("Remove Task Permanently")
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

        self.pushStartTimer = QtGui.QPushButton(self)
        self.pushStartTimer.setIcon(QtGui.QIcon(rStartAlarm))
        self.pushStartTimer.setToolTip("Start Timer for a job")        
        self.pushStartTimer.clicked.connect(self.on_pushStart_clicked)

        self.pushStopTimer = QtGui.QPushButton(self)
        self.pushStopTimer.setIcon(QtGui.QIcon(rStopAlarm))
        self.pushStopTimer.setToolTip("Stop Timer") 
        self.pushStopTimer.clicked.connect(self.on_pushStop_clicked)        
        
        self.pushRestTimer = QtGui.QPushButton(self)
        self.pushRestTimer.setIcon(QtGui.QIcon(rRest))
        self.pushRestTimer.setToolTip("Your does not work enough for have a long rest") 
        self.pushRestTimer.clicked.connect(self.on_pushRest_clicked)        
        
        self.checkShowDone = QtGui.QCheckBox("ShowDone",self)
        if int(self.curConf.config["ShowDone"])!=0 :
            self.checkShowDone.setCheckState(QtCore.Qt.Checked)
        else :
            self.checkShowDone.setCheckState(QtCore.Qt.Unchecked)
        self.checkShowDone.stateChanged.connect(self.on_checkbox_changed)
#         self.pushButtonAdd.clicked.connect(self.on_pushButtonAdd_clicked)   

        #self.myTimer = Timer([1,2])
        self.myTimer = Timer([25,5])        
        self.myTimer.isLongRest = False        
        
        self.statusBar = QtGui.QStatusBar(self)
        self.statusBar.setSizeGripEnabled(False)
        
        # GridLayout Elements Begin
        self.buttonLayout = QtGui.QGridLayout(self)
#         self.buttonLayout.addWidget(self.pushButtonLoad,0,0)
        self.buttonLayout.addWidget(self.pushButtonAdd,0,0)
        self.buttonLayout.addWidget(self.pushButtonDone,0,1)
        self.buttonLayout.addWidget(self.pushButtonUnDone,0,2)        
        self.buttonLayout.addWidget(self.pushButtonRemove,0,3)
        self.buttonLayout.addWidget(self.pushButtonWrite,0,4)
        self.buttonLayout.addWidget(self.pushStartTimer,0,5)
        self.buttonLayout.addWidget(self.pushStopTimer,0,6)
        self.buttonLayout.addWidget(self.pushRestTimer,0,7)
                                  
        self.buttonLayout.addWidget(self.tableView,1,0,1,8)
                
        self.buttonLayout.addWidget(self.checkShowDone,2,0)
        self.buttonLayout.addWidget(self.myTimer,2,5,1,2)
        
        self.buttonLayout.addWidget(self.statusBar,3,0,1,8)
#         self.pushRestTimer.setStyleSheet("QWidget { background-color: #aeadac }")
        self.pushRestTimer.setEnabled(False)
        # GridLayout Elements End        

        #Tray and Menu        
        self.contextMenu = QtGui.QMenu(self)
        #self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon(':Icons/bell.png'),self)        

        # Setup
        self.createMenu()
        self.trayIcon.setContextMenu(self.contextMenu)
        #self.trayIcon.setIcon(QtGui.QIcon(':Icons/bell.png'))
        self.trayIcon.activated.connect(self.iconActivated)
        
        #InternalTimer
        self.intTimer = QtCore.QTimer(self)
        self.intTimer.timeout.connect(self.checkTimer)
        self.intTimer.start(500)
        
        # Display
        self.trayIcon.show()             
        
          

    def createMenu(self):
        """
        This menu will be used as the context menu for the systray and the timer window.
        """
        self.toggleWindowAction = QtGui.QAction("&Restore Window", self,
                triggered=self.unhideWindow)        
#         self.toggleTimerAction = QtGui.QAction("&Toggle Timer", self,
#                 triggered=self.timer.toggleTimer)
        self.pauseTimerAction = QtGui.QAction("&Pause/Play Timer", self,
                triggered=self.myTimer.pauseTimer)
        self.resetTimerAction = QtGui.QAction("&Reset Timer", self,
                triggered=self.myTimer.resetTimer)
        self.settingsAction = QtGui.QAction("&Settings", self,
                triggered=self.myTimer.settings)
        self.quitAction = QtGui.QAction("&Quit", self,
                triggered=QtGui.qApp.quit)
        
        self.contextMenu.addAction(self.toggleWindowAction)        
#         self.contextMenu.addAction(self.toggleTimerAction)
        self.contextMenu.addAction(self.pauseTimerAction)
        self.contextMenu.addAction(self.resetTimerAction)
        self.contextMenu.addSeparator()
        self.contextMenu.addAction(self.settingsAction)
        self.contextMenu.addSeparator()
        self.contextMenu.addAction(self.quitAction)

    def iconActivated(self, reason):
        """
        pass
        """
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            if self.isVisible() :
                self.hide()
            else :
                self.unhideWindow()
            #self.myTimer.toggleTimer()

    def clearModel(self):
        self.model.clear()
        
    def setTableView(self):
        #self.tableView = QtGui.QTableWidget(self)
        self.tableView.setModel(self.model)        
        self.tableView.setColumnWidth(0,275)
        self.tableView.setColumnWidth(1,75)
        self.tableView.setColumnWidth(2,75)
        self.tableView.setColumnWidth(2,125)        
        self.tableView.horizontalHeader().setStretchLastSection(True)
        #self.tableView.setHorizontalHeaderLabels(['a', 'b', 'c', 'd', 'e'])        

    def loadCsv(self, fileName):
        self.clearModel()
        if not os.path.isfile(fileName) :
            open(fileName, 'a').close()
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
        
    def startJob(self):
        if (not self.myTimer.isActive ) :
            if self.myTimer.isLongRest :
                self.current_job = -1
                self.myTimer.startJobTimer()
                message = "Starting Long Rest :-) "
            elif self.myTimer.working_type!=1 :            
                message = "No job was selected, nothing to start"
                selection=self.tableView.selectionModel().selectedRows()
                for cur in selection :
                    self.current_job = cur.row()
                    self.myTimer.startJobTimer()
                    message = "Starting job : " + str(cur.row())
            else :
                message = "You are resting now, could not start new job"                
        else :
            message = "Some job is already active, could not start a new job"
        self.statusBar.showMessage(message)

    def stopJob(self):
        #print self.myTimer.curTime
        if self.current_job is not None :
            self.current_job = None
# Stop self.myTimer.isLongRest = False is done in self.myTimer.stopTimer(), not need to do it here             
#             self.myTimer.isLongRest = False
            self.myTimer.stopTimer()
            
    def enableRestButton(self):
        self.pushRestTimer.setEnabled(True)
        self.pushRestTimer.setToolTip("Have a long rest")

    def disableRestButton(self):
        self.pushRestTimer.setEnabled(False)
        self.pushRestTimer.setToolTip("Your does not work enough for have a long rest")
            
    def checkTimer(self):
        # Check if job is finished
        #if (self.myTimer.isDone) and ( self.current_job is not None ) :
        if (self.myTimer.isDone) :
            self.sendNotification()
            print self.myTimer.working_type
            self.myTimer.isDone = False
            if (not self.myTimer.isLongRest) and ( self.current_job is not None ) :
                self.model.item(self.current_job,1).setData(self.model.item(self.current_job,1).data(QtCore.Qt.DisplayRole).toString().toInt()[0]+1,QtCore.Qt.EditRole)
                self.writeCsv("/home/paul/.doit")    
                self.loadCsv("/home/paul/.doit")
                self.current_job = None                
                self.jobs_done+=1
            elif self.myTimer.isLongRest :
                self.current_job = None                
                self.myTimer.isLongRest = False
                self.jobs_done=0                            
            else :
                self.current_job = None
            # Check if job is finished            
        if self.jobs_done >= MIN_POMODORO_BEFORE_REST :
            self.enableRestButton()
        else :
            self.disableRestButton()        
#             self.statusBar.showMessage("You does not work enough for have a long rest.")

    def sendNotification(self):        
            if self.myTimer.isLongRest :
                self.trayIcon.showMessage("","The Long Rest is over! It's time to hard working.",QtGui.QSystemTrayIcon().Information,0)
            elif self.myTimer.working_type == 0 :
                self.trayIcon.showMessage("","The Work is Over! Have a little rest now.",QtGui.QSystemTrayIcon().NoIcon,0)
            elif self.myTimer.working_type == 1 :
                self.trayIcon.showMessage("","The little rest is over! You should work now",QtGui.QSystemTrayIcon().Information,0)
            else :
                self.trayIcon.showMessage("","Something happen",QtGui.QSystemTrayIcon().Information,0)

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
    
    @QtCore.pyqtSlot()        
    def on_pushStart_clicked(self):
        self.startJob()

    @QtCore.pyqtSlot()        
    def on_pushStop_clicked(self):
        self.stopJob()

    @QtCore.pyqtSlot()        
    def on_pushRest_clicked(self):
        self.myTimer.isLongRest = True
        self.startJob()        

    @QtCore.pyqtSlot()        
    def on_dataChanged(self):
        self.writeCsv("/home/paul/.doit")

       
def main():
    
    app = QtGui.QApplication(sys.argv)
    
    ex = Example()
    ex.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()   
