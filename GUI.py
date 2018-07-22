# import Tkinter, win32api, win32con, pywintypes
from Tkinter import *

line = 0


def changeText(event):
    global textArea, line
    line += 1
    textArea.insert(END, "%s: %s" % (line, "test msg\n"))

master = Tk()
master.geometry("+5+5")
master.wm_attributes("-topmost", True)


textArea = Text(master, height=12, width=50)
textArea.pack()

master.bind("<Button-1>", changeText)

mainloop()
