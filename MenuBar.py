from tkinter import *
import DataEngine
import MainTable
import EditMenu
import FileMenu

class MenuBar:
	def __init__(self,master):
		self.mainRoot=master
		self.menuBar=Menu(master)

		self.fileMenu=FileMenu.FileMenu(self.mainRoot)
		self.menuBar.add_cascade(label="Plik",menu=self.fileMenu.GetMenu())

		self.editMenu=EditMenu.EditMenu(self.mainRoot)
		self.menuBar.add_cascade(label="Edycja",menu=self.editMenu.GetMenu())

	def GetMenuBar(self):
		return self.menuBar

	def CloseAll(self):
		self.editMenu.CloseAll()
		#self.fileMenu.CloseAll()
		self.mainRoot.destroy()
			