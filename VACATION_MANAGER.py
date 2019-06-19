#from tkinter import *
#from MainWindow import MainWindow
#import RootEvents
#from MenuBar import MenuBar
#import FileManager
#import DataEngine
from RootWindow import RootWindow

#root=Tk()

#mainWnd=MainWindow(root)

#menuBar=MenuBar(root)
#root.config(menu=menuBar.GetMenuBar())

#root.protocol("WM_DELETE_WINDOW",menuBar.CloseAll)

#RootEvents.currentWidget=None
#root.bind_all("<B1-Motion>",RootEvents.MouseLeftButtonMove)
#root.bind_all("<Button-1>",RootEvents.MouseLeftButtonPressed)

#FileManager.ConfigFile.Read()
#if FileManager.ConfigFile.lastDataFilename!="":
#	inFile=FileManager.InputFile(FileManager.ConfigFile.lastDataFilename)
#	inFile.ClearAndWriteDataToDataEngine()

#root.mainloop()

RootWindow.Init()

RootWindow.Run()

