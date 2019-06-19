from tkinter import *
import DataEngine
import MainTable
import datetime
from FileManager import FileStatus
from FileManager import ConfigFile

class EditMenu:
	addPersonOpenFlagIdx=0
	deletePersonOpenFlagIdx=1
	editPersonOpenFlagIdx=2
	masterWidget=None

	def __init__(self,master):
		EditMenu.masterWidget=master
		self.editMenu=Menu(master,tearoff=0)
		self.editMenu.add_command(label="Dodaj osobe",command=self.AddPersonFun)
		self.editMenu.add_command(label="Usun osobe",command=self.DeletePersonFun)
		self.editMenu.add_command(label="Edytuj osbe",command=self.EditPersonFun)

		self.openFlags=[0,0,0]

	def GetMenu(self):
		return self.editMenu
	
	def AddPersonFun(self):
		if self.openFlags[EditMenu.addPersonOpenFlagIdx]==0:
			self.addRoot=AddPerson(EditMenu.masterWidget,self.openFlags)

	def DeletePersonFun(self):
		if self.openFlags[EditMenu.deletePersonOpenFlagIdx]==0:
			self.deleteRoot=DeletePerson(EditMenu.masterWidget,self.openFlags)

	def EditPersonFun(self):
		if self.openFlags[EditMenu.editPersonOpenFlagIdx]==0:
			self.editRoot=EditPerson(EditMenu.masterWidget,self.openFlags)

	def CloseAll(self):
		if self.openFlags[EditMenu.addPersonOpenFlagIdx]==1:
			self.addRoot.Close()
		if self.openFlags[EditMenu.deletePersonOpenFlagIdx]==1:
			self.deleteRoot.Close()
		if self.openFlags[EditMenu.editPersonOpenFlagIdx]==1:
			self.editRoot.Close()

class AddPerson:
	def __init__(self,master,openFlags):
		self.root=Toplevel(master)
		logoDir=ConfigFile.mainDirectory+"logo_ikona.ico"
		self.root.iconbitmap(logoDir)
		self.openFlag=openFlags
		self.openFlag[EditMenu.addPersonOpenFlagIdx]=1
		self.root.protocol("WM_DELETE_WINDOW",self.CloseProtocol)
		
		self.nameLabel=Label(self.root,text="Imie:")
		self.nameLabel.grid(row=0,column=0,padx=30,pady=10,sticky=W)
		self.nameEntry=Entry(self.root,width=40)
		self.nameEntry.grid(row=1,column=0,padx=30,sticky=W)

		self.surnameLabel=Label(self.root,text="Nazwisko:")
		self.surnameLabel.grid(row=2,column=0,padx=30,pady=10,sticky=W)
		self.surnameEntry=Entry(self.root,width=40)
		self.surnameEntry.grid(row=3,column=0,padx=30,sticky=W)

		actualYear=datetime.datetime.now().year
		self.yearStr=StringVar()
		self.yearStr.set(str(actualYear))
		self.yearLabel=Label(self.root,text="Aktualny rok:")
		self.yearLabel.grid(row=4,column=0,padx=30,pady=10,sticky=W)
		self.yearEntry=Entry(self.root,width=40,textvariable=self.yearStr)
		self.yearEntry.grid(row=5,column=0,padx=30,sticky=W)

		self.buttonsFrame=Frame(self.root)
		self.buttonsFrame.grid(row=6,column=0)

		self.registerButton=Button(self.buttonsFrame,text="OK",width=10,height=1,command=self.AddPerson)
		self.registerButton.grid(row=0,column=0,padx=20,pady=20,sticky=E)

		self.cancelButton=Button(self.buttonsFrame,text="Anuluj",width=10,height=1,command=self.CloseProtocol)
		self.cancelButton.grid(row=0,column=1,padx=20,pady=20,sticky=E)

	def CloseProtocol(self):
		self.openFlag[EditMenu.addPersonOpenFlagIdx]=0
		self.root.destroy()

	def Close(self):
		self.root.destroy()

	def AddPerson(self):
		name=self.nameEntry.get()
		surname=self.surnameEntry.get()
		valErrorFlag=0

		try:
			year=int(self.yearStr.get())
		except ValueError:
			self.errorWindow=Toplevel(self.root)
			self.errorWindow.iconbitmap(r"logo_ikona.ico")
			self.errorMsg=Label(self.errorWindow,text="Błąd! Zły format wartości roku!",font=("Arial",12,"bold"))
			self.errorMsg.grid(row=0,column=0,padx=30,pady=30,sticky=N)
			valErrorFlag=1

		if valErrorFlag==0:
			if name=="" or surname=="":
				self.errorWindow=Toplevel(self.root)
				self.errorWindow.iconbitmap(r"logo_ikona.ico")
				self.errorMsg=Label(self.errorWindow,text="Błąd! Brak imienia lub nazwiska!",font=("Arial",12,"bold"))
				self.errorMsg.grid(row=0,column=0,padx=30,pady=30,sticky=N)
			else:
				if " " in name:
					self.errorWindow=Toplevel(self.root)
					self.errorWindow.iconbitmap(r"logo_ikona.ico")
					self.errorMsg=Label(self.errorWindow,text="Błąd! Imię nie może zawierać białych znaków!",font=("Arial",12,"bold"))
					self.errorMsg.grid(row=0,column=0,padx=30,pady=30,sticky=N)
				elif " " in surname:
					self.errorWindow=Toplevel(self.root)
					self.errorWindow.iconbitmap(r"logo_ikona.ico")
					self.errorMsg=Label(self.errorWindow,text="Błąd! Nazwisko nie może zawierać białych znaków!",font=("Arial",12,"bold"))
					self.errorMsg.grid(row=0,column=0,padx=30,pady=30,sticky=N)
				else:
					FileStatus.Set()

					newPerson=DataEngine.PersonData(name,surname,year)
					DataEngine.PersonList.AddPersonToList(newPerson)
					MainTable.ChoosePerson.UpdatePersonList()
					self.CloseProtocol()

class DeletePerson:
	def __init__(self,master,openFlags_):
		self.root=Toplevel(master)
		logoDir=ConfigFile.mainDirectory+"logo_ikona.ico"
		self.root.iconbitmap(logoDir)
		self.openFlags=openFlags_
		self.openFlags[EditMenu.deletePersonOpenFlagIdx]=1
		self.root.protocol("WM_DELETE_WINDOW",self.CloseProtocol)

		self.choosePersonLabel=Label(self.root,text="Wybierz osobe:")
		self.choosePersonLabel.grid(row=0,column=0,sticky=W,padx=30,pady=10)

		self.optionsList=[]

		for person in DataEngine.PersonList.GetFullPersonDataList():
			name=person.GetName()
			surname=person.GetSurname()
			fullName=name+" "+surname
			self.optionsList.append(fullName)

		if len(self.optionsList)==0:
			self.optionsList.append("-")

		self.selectVar=StringVar()
		self.selectVar.set(self.optionsList[0])
		self.optionMenu=OptionMenu(self.root,self.selectVar,*self.optionsList)
		self.optionMenu.config(width=50)
		self.optionMenu.grid(row=1,column=0,sticky=W,padx=30)

		self.buttonsFrame=Frame(self.root)
		self.buttonsFrame.grid(row=2,column=0)

		self.deleteButton=Button(self.buttonsFrame,text="Usun",width=10,command=self.Delete)
		self.deleteButton.grid(row=0,column=0,padx=20,pady=20)
		self.cancelButton=Button(self.buttonsFrame,text="Anuluj",width=10,command=self.Cancel)
		self.cancelButton.grid(row=0,column=1,padx=20,pady=20)

	def CloseProtocol(self):
		self.openFlags[EditMenu.deletePersonOpenFlagIdx]=0
		self.root.destroy()

	def Close(self):
		self.root.destroy()

	def Delete(self):
		fullName=self.selectVar.get()
		
		if fullName!="-":
			FileStatus.Set()

			fullNameTab=fullName.split(" ")

			DataEngine.PersonList.DeletePersonFromList(fullNameTab[0],fullNameTab[1])

			MainTable.ChoosePerson.UpdatePersonList()

		self.CloseProtocol()

	def Cancel(self):
		self.CloseProtocol()

class EditPerson:
	def __init__(self,master,openFlags_):
		self.root=Toplevel(master)
		logoDir=ConfigFile.mainDirectory+"logo_ikona.ico"
		self.root.iconbitmap(logoDir)
		self.openFlags=openFlags_
		self.openFlags[EditMenu.editPersonOpenFlagIdx]=1
		self.root.protocol("WM_DELETE_WINDOW",self.CloseProtocol)

		self.choosePersonLabel=Label(self.root,text="Wybierz osobe:")
		self.choosePersonLabel.grid(row=0,column=0,sticky=W,padx=30,pady=10)

		self.optionsList=[]

		for person in DataEngine.PersonList.GetFullPersonDataList():
			name=person.GetName()
			surname=person.GetSurname()
			fullName=name+" "+surname
			self.optionsList.append(fullName)

		if len(self.optionsList)==0:
			self.optionsList.append("-")

		self.selectVar=StringVar()
		self.selectVar.set(self.optionsList[0])
		self.optionMenu=OptionMenu(self.root,self.selectVar,*self.optionsList)
		self.optionMenu.config(width=50)
		self.optionMenu.grid(row=1,column=0,sticky=W,padx=30)

		self.nameLabel=Label(self.root,text="Imie:")
		self.nameLabel.grid(row=2,column=0,sticky=W,padx=30,pady=10)
		self.nameEntry=Entry(self.root,width=40)
		self.nameEntry.grid(row=3,column=0,sticky=W,padx=30)

		self.surnameLabel=Label(self.root,text="Nazwisko:")
		self.surnameLabel.grid(row=4,column=0,sticky=W,padx=30,pady=10)
		self.surnameEntry=Entry(self.root,width=40)
		self.surnameEntry.grid(row=5,column=0,sticky=W,padx=30)

		if self.selectVar.get()=="-":
			self.nameEntry.config(state=DISABLED)
			self.surnameEntry.config(state=DISABLED)

		self.buttonsFrame=Frame(self.root)
		self.buttonsFrame.grid(row=6,column=0)

		self.deleteButton=Button(self.buttonsFrame,text="Modyfikuj",width=10,command=self.Modify)
		self.deleteButton.grid(row=0,column=0,padx=20,pady=20)
		self.cancelButton=Button(self.buttonsFrame,text="Anuluj",width=10,command=self.CloseProtocol)
		self.cancelButton.grid(row=0,column=1,padx=20,pady=20)

	def CloseProtocol(self):
		self.openFlags[EditMenu.editPersonOpenFlagIdx]=0
		self.root.destroy()

	def Close(self):
		self.root.destroy()

	def Modify(self):
		if self.selectVar.get()!="-":
			name=self.nameEntry.get()
			surname=self.surnameEntry.get()

			if name!="" and surname!="":
				if " " in name:
					self.errorWindow=Toplevel(self.root)
					self.errorWindow.iconbitmap(r"logo_ikona.ico")
					self.errorMsg=Label(self.errorWindow,text="Błąd! Imię nie może zawierać białych znaków!",font=("Arial",12,"bold"))
					self.errorMsg.grid(row=0,column=0,padx=30,pady=30,sticky=N)
				elif " " in surname:
					self.errorWindow=Toplevel(self.root)
					self.errorWindow.iconbitmap(r"logo_ikona.ico")
					self.errorMsg=Label(self.errorWindow,text="Błąd! Nazwisko nie może zawierać białych znaków!",font=("Arial",12,"bold"))
					self.errorMsg.grid(row=0,column=0,padx=30,pady=30,sticky=N)
				else:
					FileStatus.Set()

					basicName=self.selectVar.get()
					basicNameTab=basicName.split(" ")

					person=DataEngine.PersonList.GetPersonFromList(basicNameTab[0],basicNameTab[1])

					person.SetName(name)
					person.SetSurname(surname)

					MainTable.ChoosePerson.UpdatePersonList()

					self.CloseProtocol()
			else:
				self.errorWindow=Toplevel(self.root)
				self.errorWindow.iconbitmap(r"logo_ikona.ico")
				self.errorMsg=Label(self.errorWindow,text="Błąd! Złe dane osobowe!",font=("Arial",12,"bold"))
				self.errorMsg.grid(row=0,column=0,padx=30,pady=30,sticky=N)
		else:
			self.errorWindow=Toplevel(self.root)
			self.errorWindow.iconbitmap(r"logo_ikona.ico")			  
			self.errorMsg=Label(self.errorWindow,text="Błąd! Nie wybrano osoby!",font=("Arial",12,"bold"))
			self.errorMsg.grid(row=0,column=0,padx=30,pady=30,sticky=N)
		
