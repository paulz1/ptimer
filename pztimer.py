#!/usr/bin/python
"""
pztimer - A reverse counting timer with multiple subsequent timers.
Clone of ptimer project of Amjith Ramanujam (amjith@gmail.com).
Cloned for add some additional functionality.

Usage: 
pztimer.py val1 [val2 ...]

Example: (Starts a timer for 10mins and then for 15mins when 10mins expires)
    ptimer.py 10 15
"""
__author__ = "Paul Zakharov (paul.zakharov@gmail.com)"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2015/06/22 $"
__copyright__ = "Copyright (c) 2010, Amjith Ramanujam, (c) 2015 Paul Zakharov"

import sys
from itertools import cycle
from PyQt4 import QtCore, QtGui

from Resources.LcdNumber_ui import Ui_Form
from Resources.AlarmSetupDialog_ui import Ui_DialogAlarmSetup
#from SettingsDialog import SettingsDialog

#import qt_test
#import example

# global variables for logging and debugging

err = sys.stderr
_debug = 0
log = sys.stdout

MINUTE_LEN = 60

class Timer(QtGui.QMainWindow):
    """
    The Timer class uses the QtTimer to keep count and to display the count-down timer.
    A systray is also implemented with the option to toggle the timer, pause/play, reset, settings and quit.
    """
    def __init__(self, timer_values, parent=None):
        #QtGui.QWidget.__init__(self, parent)
        #QtGui.QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.FramelessWindowHint)
        QtGui.QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)        
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Initialization 

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateTimerDisplay)
        self.isPaused = False
        self.isActive = False
        self.isDone = False       
        self.isLongRest = False        
        self.alarm_times = []
        self.alarm_types = [0,1] #Globally there are 2 alarm times : type 0 - work or long rest, 1 - short rest
        self.working_type = -1 # -1 (or something else than 0 or 1) - undefined, 0 - working, 1 - rest              
        self.settingsDialog = None

        if (len(timer_values) > 0):
            self.setTimer(timer_values)
#            self.startTimer()
        else:
            self.settings()

        self.blinkTimer = QtCore.QTimer(self)
        self.blinkTimer.timeout.connect(self.toggleTimerColor)
        self.color_names = [ "Normal", "Black" ]
        self.color_idx = 1

    def createMenu(self):
        """
        This menu will be used as the context menu for the systray and the timer window.
        """
        self.toggleTimerAction = QtGui.QAction("&Toggle Timer", self,
                triggered=self.toggleTimer)
        self.pauseTimerAction = QtGui.QAction("&Pause/Play Timer", self,
                triggered=self.pauseTimer)
        self.resetTimerAction = QtGui.QAction("&Reset Timer", self,
                triggered=self.resetTimer)
        self.settingsAction = QtGui.QAction("&Settings", self,
                triggered=self.settings)
        self.quitAction = QtGui.QAction("&Quit", self,
                triggered=QtGui.qApp.quit)
        
        self.contextMenu.addAction(self.toggleTimerAction)
        self.contextMenu.addAction(self.pauseTimerAction)
        self.contextMenu.addAction(self.resetTimerAction)
        self.contextMenu.addSeparator()
        self.contextMenu.addAction(self.settingsAction)
        self.contextMenu.addSeparator()
        self.contextMenu.addAction(self.quitAction)
        
    def settings(self):
        if not self.settingsDialog:
            if (self.alarm_times):
                self.settingsDialog = SettingsDialog(self, self.alarm_times)
            else:
                self.settingsDialog = SettingsDialog(self)
        self.settingsDialog.show()
        self.connect(self.settingsDialog, QtCore.SIGNAL("Accept"),self.pullTimes)        

    def toggleTimer(self):
        """
        Toggles the display of the timer. 
        """
        try:
            if self.ui.lcdNumber.isVisible():
                self.hide()
            else:
                self.show()
        except AttributeError:
            return

    def pauseTimer(self):
        if (self.isPaused == False):
            self.timer.stop()
            self.blinkTimer.stop()
            self.isPaused = True
        else:
            self.timer.start(1000)
            self.isActive = True
            self.isPaused = False
        self.ui.lcdNumber.setStyleSheet("QWidget { background-color: Normal }" )

    def pullTimes(self):
        self.alarm_times = [int(self.settingsDialog.ui.lineEditAlarm1.text()) * MINUTE_LEN, int(self.settingsDialog.ui.lineEditAlarm2.text()) * MINUTE_LEN]
        self.resetTimer()

    def setTimer(self, timer_list):
        self.alarm_times = [x*MINUTE_LEN for x in timer_list]
#         self.alarm_types = range(len(self.alarm_times))
#         self.timer_iter = cycle(self.alarm_times)    # An iterator that cycles through the list
        self.timer_iter = cycle(self.alarm_types)    # An iterator that cycles through the list        
#         self.curTime = self.timer_iter.next()      # Current timer value
        self.working_type = self.timer_iter.next()
        self.curTime = self.alarm_times[self.working_type]      # Current timer value
        
    def resetTimer(self):
#         self.timer_iter = cycle(self.alarm_times)
#         self.timer_iter = cycle(self.alarm_types)
#         self.working_type = self.timer_iter.next()                
#         self.curTime = self.alarm_times[self.working_type]        
        self.startTimer()
        self.blinkTimer.stop()
        self.ui.lcdNumber.setStyleSheet("QWidget { background-color: Normal }" )
        self.isActive = True

    def startTimer(self):        
        self.timer.start(1000)
        self.isActive = True
        self.isDone = False
        
    def startJobTimer(self):
        self.working_type = 0                
        self.curTime = self.alarm_times[self.working_type]       
        self.startTimer()
        self.blinkTimer.stop()
        self.ui.lcdNumber.setStyleSheet("QWidget { background-color: Normal }" )           

    def stopTimer(self):
        self.curTime = 0
        text = "%d:%02d" % (self.curTime/MINUTE_LEN,self.curTime % MINUTE_LEN)
        self.ui.lcdNumber.display(text)
        self.isActive = False
        self.isDone = False
        self.isLongRest = False # If LongRest is stopped, it's over        
        self.working_type = -1             
        self.timer.stop()        
        
    def showTimer(self):
        self.show()

    def updateTimerDisplay(self):
        text = "%d:%02d" % (self.curTime/MINUTE_LEN,self.curTime % MINUTE_LEN)
        self.ui.lcdNumber.display(text)
        if self.isActive :
            if (self.curTime == 0) :
                self.timer.stop()
                self.isDone = True                
                if not self.isLongRest :
                    self.blinkTimer.start(250)
                else :
                    self.isActive = False
                    self.working_type = -1
            else:
                self.curTime -= 1

    def toggleTimerColor(self):
        self.color_idx = 3 - self.color_idx
        self.showTimer()
        self.ui.lcdNumber.setStyleSheet("QWidget { background-color: %s }" % self.color_names[self.color_idx - 1])

    def mousePressEvent(self, event):
        button = event.button()
        if button == 1:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft();
        elif button == 2:
            self.contextMenu.exec_(QtGui.QCursor.pos())

    def mouseReleaseEvent(self, event):
        button = event.button()
        if button == 1: # left click
            if (self.curTime == 0): # blinking timer should be closed on a left click
                self.blinkTimer.stop()
                self.isDone = False                
                if self.working_type < 0 :
                    self.isActive = False
                elif self.working_type != 0 : # we were in the rest mode, but the rest is over, so stop and do nothing
                    self.isActive = False
                    self.working_type = -1
                else : # the job is over, so going to rest
                    self.working_type = 1
                    self.isActive = True
                    self.curTime = self.alarm_times[self.working_type]
                    self.resetTimer()                    
                self.ui.lcdNumber.setStyleSheet("QWidget { background-color: Normal }" )

    def mouseMoveEvent(self, event):
        if event.buttons() != QtCore.Qt.LeftButton: # not left click
            return 
        
#         self.move(event.globalPos() - self.dragPosition)

    def iconActivated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            self.toggleTimer()            


class SettingsDialog(QtGui.QDialog):

    def __init__(self, parent=None, alarm_times = [25*MINUTE_LEN,5*MINUTE_LEN]):
        QtGui.QDialog.__init__(self, parent)
        #print "Settings Dialog\n"
        self.setWindowModality(QtCore.Qt.ApplicationModal)             # Make this a application blocking dialog.
        self.ui = Ui_DialogAlarmSetup()
        self.ui.setupUi(self)
        intValidator = QtGui.QIntValidator(0,99,self.ui.lineEditAlarm1) # create a int validator with range from 0 to 60
        self.ui.lineEditAlarm1.setValidator(intValidator);
        self.ui.lineEditAlarm2.setValidator(intValidator);
        self.ui.lineEditAlarm1.setText(str(alarm_times[0]/MINUTE_LEN))
        self.ui.lineEditAlarm2.setText(str(alarm_times[1]/MINUTE_LEN))
        self.ui.lineEditAlarm1.selectAll();
        self.ui.lineEditAlarm2.selectAll();

        self.trayMsgDisplayed = False
        self.show()

    #def __del__(self):
        #print "Destructor for Settings Dialog\n"

    def closeEvent(self, event):
        if self.trayMsgDisplayed == False:
            QtGui.QMessageBox.information(self, "Systray",
                    "The program will keep running in the system tray. To "
                    "terminate the program, choose <b>Quit</b> in the "
                    "context menu of the system tray entry.")
            self.hide()
            event.ignore()
            self.trayMsgDisplayed = True

    def reject(self):
        self.close();

    def accept(self):
        timer_list = [int(self.ui.lineEditAlarm1.text()) * MINUTE_LEN, int(self.ui.lineEditAlarm2.text()) * MINUTE_LEN ]
        self.emit(QtCore.SIGNAL("Accept"))
        self.close();

def Str2Num(str_list):
    num = []
    for str in str_list:
        try:
            num.append(int(str))
        except ValueError:
            num.append(float(str))
    return num

def usage():
	print >>err, __doc__

def printTest():
    print "test printTest()"

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(None, "Systray",
                "No system tray on this system. Fail")
        sys.exit(1)
    QtGui.QApplication.setQuitOnLastWindowClosed(False)
    timerList = Str2Num(sys.argv[1:])
    #myapp = Timer(timerList)
    myapp = Timer([25,5])    
    sys.exit(app.exec_())

