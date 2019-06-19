import sys
from tkinter import *
from MainTable import MainTable

initWndWidth=1000
initWndHeight=600

class MainWindow:
	width=0
	height=0
	mainFrame=None
	table=None

	def __init__(self,master):
		self.width=initWndWidth
		self.height=initWndHeight

		self.mainFrame=Frame(master)
		self.mainFrame.pack()
		#self.mainFrame.bind("<Configure>",lambda event : "break")
		
		self.table=MainTable(self.mainFrame,self.width,self.height)

		
	

