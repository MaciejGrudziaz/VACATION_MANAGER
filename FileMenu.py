from tkinter import *
from tkinter import filedialog
import DataEngine
import MainTable
import FileManager
import getpass
from PDFcreator import CreatePDF
from datetime import datetime

class FileMenu:
	masterWidget=None

	#readFileOpenFlagIdx=0
	#saveFileOpenFlagIdx=1
	#exportFileOpenFlagIdx=2

	def __init__(self,master):
		FileMenu.masterWidget=master
		self.fileMenu=Menu(master,tearoff=0)
		self.fileMenu.add_command(label="Nowy",command=NewFile.Create)
		self.fileMenu.add_command(label="Wczytaj",command=self.ReadFileFun)
		self.fileMenu.add_command(label="Zapisz",command=self.SaveFileFun)
		self.fileMenu.add_command(label="Zapisz jako",command=self.SaveFileAsFun)
		self.fileMenu.add_command(label="Eksportuj",command=lambda : ExportFile.Export())
		self.openFlags=[0,0,0]

	def GetMenu(self):
		return self.fileMenu

	def SaveFileFun(self):
		if FileManager.ConfigFile.lastDataFilename=="":
			self.saveRoot=SaveFileAs(self.masterWidget)
		else:
			SaveFile();

	def SaveFileAsFun(self):
		self.saveRoot=SaveFileAs(self.masterWidget)

	def ReadFileFun(self):
		self.readRoot=ReadFile(self.masterWidget)


class SaveFileAs:
	def __init__(self,master):
		dirPath=""
		if FileManager.ConfigFile.lastLocationWriteTo!="":
			dirPath=FileManager.ConfigFile.lastLocationWriteTo
		else:
			dirPath=GetStandardPath()

		filename=filedialog.asksaveasfilename(initialdir=dirPath,title="Zapisz jako",defaultextension=".bls",filetypes=(("bls files","*.bls"),("all files","*.*")))

		if filename!="":
			FileManager.OutputFile(filename)

			pathIdx=filename.rfind("/")
			FileManager.ConfigFile.lastLocationWriteTo=filename[:pathIdx]

class SaveFile:
	def __init__(self):
		if FileManager.ConfigFile!="":
			FileManager.OutputFile(FileManager.ConfigFile.lastDataFilename)


class NewFile:
	def Create():
		if FileManager.FileStatus.fileEditFlag==1:
			errorWindow=Toplevel(FileMenu.masterWidget)
			logoDir=ConfigFile.mainDirectory+"logo_ikona.ico"
			errorWindow.iconbitmap(logoDir)
			errorWindowMainFrame=Frame(errorWindow)
			errorWindowMainFrame.grid(row=0,column=0,padx=30,pady=30)
			errorMsg=Label(errorWindowMainFrame,text="Nie zapisano zmian! Czy zapisać teraz?",font=("Arial",12,"bold"))
			errorMsg.grid(row=0,column=0,sticky=N)
			buttonFrame=Frame(errorWindowMainFrame)
			buttonFrame.grid(row=1,column=0,pady=10)
			yesButton=Button(buttonFrame,text="Tak",width=10,command=lambda : NewFile.SaveFile(FileMenu.masterWidget,errorWindow))
			yesButton.grid(row=0,column=0,padx=10)
			noButton=Button(buttonFrame,text="Nie",width=10,command=lambda : NewFile.ClearDataAndUpdate(errorWindow))
			noButton.grid(row=0,column=1,padx=10)
			cancelButton=Button(buttonFrame,text="Anuluj",width=10,command=lambda : errorWindow.destroy())
			cancelButton.grid(row=0,column=2,padx=10)
		else:
			NewFile.ClearDataAndUpdate(None)

	def SaveFile(master,errorWindow):
		errorWindow.destroy()

		if FileManager.ConfigFile.lastDataFilename!="":
			SaveFile()
		else:
			SaveFileAs(master)

		NewFile.ClearDataAndUpdate(errorWindow)
		FileManager.FileStatus.NewFile()
		
	def ClearDataAndUpdate(errorWindow):
		if errorWindow!=None:
			errorWindow.destroy()

		DataEngine.PersonList.ClearAllData()
		MainTable.MainTable.ClearTable()
		FileManager.ConfigFile.lastDataFilename=""
		FileManager.FileStatus.NewFile()
		

class ReadFile:
	def __init__(self,master):
		dirPath=""
		if FileManager.ConfigFile.lastLocationReadFrom!="":
			dirPath=FileManager.ConfigFile.lastLocationReadFrom
		else:
			dirPath=GetStandardPath()

		filename=filedialog.askopenfilename(initialdir=dirPath,title="Wybierz plik",defaultextension=".bls",filetypes=(("bls files","*.bls"),("all files","*.*")))

		if filename!="":
			input=FileManager.InputFile(filename)

			errorFlag=input.GetErrorFlag()
			if errorFlag==0:
				input.ClearAndWriteDataToDataEngine()
				MainTable.ChoosePerson.UpdatePersonList()
				DataEngine.PersonList.ClearDataEditFlag()
			else:
				self.errorRoot=Toplevel(self.root)
				self.errorMsg=Label(self.errorRoot,font=("Arial",12,"bold"))

				if errorFlag==1:
					self.errorMsg.config(text="Błąd! Nie można otworzyć pliku!")
				elif errorFlag==2:
					self.errorMsg.config(text="Błąd! Plik uszkodzony!")

				self.errorMsg.grid(row=0,column=0,padx=30,pady=30)

			pathIdx=filename.rfind("/")
			FileManager.ConfigFile.lastLocationReadFrom=filename[:pathIdx]

class ExportFile:
	def Export():
		fullName=MainTable.ChoosePerson.selectedPerson.get()
		splitName=fullName.split(' ')
		person=DataEngine.PersonList.GetPersonFromList(splitName[0],splitName[1])

		initDir=""
		if FileManager.ConfigFile.lastLocationWriteTo!="":
			initDir=FileManager.ConfigFile.lastLocationWriteTo
		else:
			initDir="C:/"

		filename=filedialog.asksaveasfilename(initialdir=initDir,title="Eksportuj",defaultextension=".pdf",filetypes=(("pdf files","*.pdf"),("all files","*.*")))

		if filename!="":
			year=MainTable.ChooseYear.selectedYear

			CreatePDF(filename,splitName[0],splitName[1],str(year),person.GetVacationCalendar(year),person.GetYearBaseFreeDays(year),person.GetYearFreeDaysFromLastYear(year))

def GetStandardPath():
	username=getpass.getuser()
	path="C:/Users/"
	path+=username
	path+="/Documents"

	return path



