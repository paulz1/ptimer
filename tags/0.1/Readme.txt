ptimer  
======

Intro:
------
ptimer is a Pomodoro Timer that can be used to set multiple alarms. It has a visual notification once the
timer expires. 

Usage:
------
$ ptimer.py val1 [val2 ...]

Example:
    $ ptimer.py 10 15

Starts a timer for 10mins and  notifies user. When user clicks on the Timer, it will start another timer for 15mins.

Dependencies:
-------------
This is a python script that is tested on Python 2.6.
This uses PyQt4 for GUI, so it required PyQt4 to be installed on your system. (http://www.riverbankcomputing.co.uk/software/pyqt/download)

You can check if your system has PyQt4 by doing the following. 

Launch the Python REPL and type 'import PyQt4' in the prompt. If it throws an error then you don't have PyQt4.

eg:
$ python
Python 2.6.5 (r265:79063, Jul 14 2010, 13:38:11)
[GCC 4.4.3] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import PyQt4
>>>
