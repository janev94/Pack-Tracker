# import Tkinter, win32api, win32con, pywintypes
from Tkinter import *

from setuptools.command.test import test

line = 0


def changeText(event, textArea):
    global line
    line += 1
    textArea.insert(END, "%s: %s" % (line, "test msg\n"))


def logMsg(ta, msg):
    ta.insert(END, msg)


def setupOverlay():
    master = Tk()
    master.geometry("+5+5")
    master.wm_attributes("-topmost", True)

    textArea = Text(master, height=12, width=50)
    textArea.pack()

    master.bind("<Button-1>", lambda event, ta=textArea: changeText(event, ta))

    return textArea


def start():
    mainloop()

if __name__ == '__main__':
    setupOverlay()