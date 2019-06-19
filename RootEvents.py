import sys
from tkinter import *
from FileManager import ConfigFile

currentWidget=None

def MouseLeftButtonMove(event):
	global currentWidget
	widget=event.widget.winfo_containing(event.x_root,event.y_root)

	if currentWidget!=widget:
		if currentWidget:
			currentWidget.event_generate("<<B1-Leave>>")
		currentWidget=widget
		currentWidget.event_generate("<<B1-Enter>>")

def MouseLeftButtonPressed(event):
	global currentWidget
	widget=event.widget.winfo_containing(event.x_root,event.y_root)

	if currentWidget!=widget:
		currentWidget=widget

def CloseMainWindow(root,menuBar):
	ConfigFile.Update()

	menuBar.CloseAll()
	root.destroy()