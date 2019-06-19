import FileManager
from tkinter import *
from MainWindow import MainWindow
from MenuBar import MenuBar
import MainTable
import FileMenu

class RootWindow:
	root=None
	mainWnd=None
	menuBar=None
	currentWidget=None

	def Init():
		FileManager.ConfigFile.Read()

		RootWindow.root=Tk()
		RootWindow.root.title("Menedżer urlopów")
		ikonaDir=FileManager.ConfigFile.mainDirectory+'logo_ikona.ico'
		#RootWindow.root.iconbitmap(r'logo_ikona.ico')
		RootWindow.root.iconbitmap(ikonaDir)
			
		FileManager.InputFile.root=RootWindow.root
		FileManager.OutputFile.root=RootWindow.root
		FileManager.FileStatus.root=RootWindow.root

		RootWindow.mainWnd=MainWindow(RootWindow.root)

		RootWindow.menuBar=MenuBar(RootWindow.root)
		RootWindow.root.config(menu=RootWindow.menuBar.GetMenuBar())

		RootWindow.root.protocol("WM_DELETE_WINDOW",RootWindow.CloseMainWindow)

		RootWindow.currentWidget=None
		RootWindow.root.bind_all("<B1-Motion>",RootWindow.MouseLeftButtonMove)
		RootWindow.root.bind_all("<Button-1>",RootWindow.MouseLeftButtonPressed)

		if FileManager.ConfigFile.lastDataFilename!="" and len(sys.argv)<=1:
			inFile=FileManager.InputFile(FileManager.ConfigFile.lastDataFilename)
			inFile.ClearAndWriteDataToDataEngine()
			MainTable.ChoosePerson.UpdatePersonList()
		elif len(sys.argv)>1:
			print(sys.argv[1])
			print((sys.argv[1])[-4:])

			if((sys.argv[1])[-4:]==".bls"):
				FileManager.ConfigFile.lastDataFilename=sys.argv[1]
				inFile=FileManager.InputFile(sys.argv[1])
				inFile.ClearAndWriteDataToDataEngine()
				MainTable.ChoosePerson.UpdatePersonList()

	def Run():
		RootWindow.root.mainloop()

	def MouseLeftButtonMove(event):
		#global currentWidget
		widget=event.widget.winfo_containing(event.x_root,event.y_root)

		if RootWindow.currentWidget!=widget:
			if RootWindow.currentWidget:
				RootWindow.currentWidget.event_generate("<<B1-Leave>>")
			RootWindow.currentWidget=widget
			RootWindow.currentWidget.event_generate("<<B1-Enter>>")

	def MouseLeftButtonPressed(event):
		#global currentWidget
		widget=event.widget.winfo_containing(event.x_root,event.y_root)

		if RootWindow.currentWidget!=widget:
			RootWindow.currentWidget=widget

	def CloseMainWindow():
		if FileManager.FileStatus.fileEditFlag==1:
			errorWindow=Toplevel(RootWindow.root)
			logoDir=FileManager.ConfigFile.mainDirectory+"logo_ikona.ico"
			errorWindow.iconbitmap(logoDir)
			errorWindowMainFrame=Frame(errorWindow)
			errorWindowMainFrame.grid(row=0,column=0,padx=30,pady=30)
			errorMsg=Label(errorWindowMainFrame,text="Nie zapisano zmian! Czy zapisać teraz?",font=("Arial",12,"bold"))
			errorMsg.grid(row=0,column=0,sticky=N)
			buttonFrame=Frame(errorWindowMainFrame)
			buttonFrame.grid(row=1,column=0,pady=10)
			yesButton=Button(buttonFrame,text="Tak",width=10,command=RootWindow.SaveFile)
			yesButton.grid(row=0,column=0,padx=10)
			noButton=Button(buttonFrame,text="Nie",width=10,command=RootWindow.Close)
			noButton.grid(row=0,column=1,padx=10)
			cancelButton=Button(buttonFrame,text="Anuluj",width=10,command=lambda : errorWindow.destroy())
			cancelButton.grid(row=0,column=2,padx=10)
		else:
			RootWindow.Close()

	def SaveFile():
		if FileManager.ConfigFile.lastDataFilename=="":
			FileMenu.SaveFileAs(RootWindow.root)
		else:
			FileMenu.SaveFile()

		RootWindow.Close()

	def Close():
		FileManager.ConfigFile.Update()

		RootWindow.menuBar.CloseAll()

