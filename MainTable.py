from tkinter import *
import DataEngine
from FileManager import FileStatus
from FileManager import ConfigFile

class MainTable:
	months=[]

	chooseModes=None
	currentVal=[]

	upperFrame=None

	choosePerson=None

	yearOpFrame=None
	chooseYear=None
	addYear=None

	width=0
	height=0
	v=0
	frame=None

	lowerFrame=None
	lowerFrame2=None
	sumUrlopy=0
	sumUrlopyStr=''
	sumZwolnienia=0
	sumZwolnieniaStr=''
	sumUrlopyOkolicz=0
	sumUrlopyOkoliczStr=''
	sumUrlopyLabel=None
	sumZwolnieniaLabel=None
	sumUrlopyOkoliczLabel=None

	def __init__(self,master,masterHeight,masterWidth):
		MainTable.upperFrame=Frame(master)
		MainTable.upperFrame.grid(row=0,column=0,sticky=E)

		MainTable.currentVal.append(1)
		MainTable.chooseModes=Mode(MainTable.upperFrame,MainTable.currentVal)

		label1=Label(MainTable.upperFrame,width=10,height=3,text="Suma\nUrlopy",anchor=CENTER,relief="ridge",bd=4)
		label1.grid(row=0,column=4,sticky=S)

		label2=Label(MainTable.upperFrame,width=10,height=3,text="Suma\nZwolnienia",anchor=CENTER,relief="ridge",bd=4)
		label2.grid(row=0,column=5,sticky=S)

		label3=Label(MainTable.upperFrame,width=15,height=3,text="Suma\nUrlopy\nOkolicznościowe",anchor=CENTER,relief="ridge",bd=4)
		label3.grid(row=0,column=6,sticky=S)

		MainTable.choosePerson=ChoosePerson(MainTable.upperFrame)

		MainTable.yearOpFrame=Frame(MainTable.upperFrame)
		MainTable.yearOpFrame.grid(row=0,column=1,padx=10)
		MainTable.chooseYear=ChooseYear(MainTable.yearOpFrame)
		MainTable.addYear=AddYear(MainTable.yearOpFrame)

		MainTable.frame=Frame(master)
		MainTable.frame.grid(row=1,column=0,sticky=N)

		for i in range(12):
			MainTable.months.append(Month(MainTable.frame,i+1,MainTable.currentVal))

		MainTable.lowerFrame=Frame(master)
		MainTable.lowerFrame.grid(row=2,column=0,sticky=E)

		#label3=Label(MainTable.lowerFrame,width=10,height=2,text="Łącznie",anchor=CENTER,relief="ridge",bd=4)
		label3=Label(MainTable.lowerFrame,width=10,height=2,text="Łącznie",anchor=CENTER)
		label3.grid(row=0,column=0,sticky=E)

		MainTable.sumUrlopyStr=StringVar()
		MainTable.sumUrlopyStr.set('0')
		MainTable.sumZwolnieniaStr=StringVar()
		MainTable.sumZwolnieniaStr.set('0')
		MainTable.sumUrlopyOkoliczStr=StringVar()
		MainTable.sumUrlopyOkoliczStr.set('0')

		MainTable.sumUrlopyLabel=Label(MainTable.lowerFrame,width=10,height=2,bd=4,anchor=CENTER,textvariable=MainTable.sumUrlopyStr,relief="groove")
		MainTable.sumUrlopyLabel.grid(row=0,column=1,sticky=E)

		MainTable.sumZwolnieniaLabel=Label(MainTable.lowerFrame,width=10,height=2,bd=4,anchor=CENTER,textvariable=MainTable.sumZwolnieniaStr,relief="groove")
		MainTable.sumZwolnieniaLabel.grid(row=0,column=2,sticky=E)

		MainTable.sumUrlopyOkoliczLabel=Label(MainTable.lowerFrame,width=15,height=2,bd=4,anchor=CENTER,textvariable=MainTable.sumUrlopyOkoliczStr,relief="groove")
		MainTable.sumUrlopyOkoliczLabel.grid(row=0,column=3,sticky=E)

		MainTable.lowerFrame2=Frame(master)
		MainTable.lowerFrame2.grid(row=3,column=0,sticky=E)

		ShowFreeDaysLeft.Init(MainTable.lowerFrame2)

	def LoadTableDataFromPersonData(person,year):
		personVacationList=person.GetVacationCalendar(year)

		monthIdx=0
		dayIdx=0
		for month in personVacationList:
			dayIdx=0
			for dayVal in month:
				if dayVal!=MainTable.months[monthIdx].GetDayVal(dayIdx):
					MainTable.months[monthIdx].SetDayVal(dayIdx,dayVal)
				dayIdx+=1
			MainTable.months[monthIdx].UpdateStats()
			monthIdx+=1
	
	def ResetTableData():
		for monthIdx in range(12):
			for dayIdx in range(31):
				MainTable.months[monthIdx].SetDayVal(dayIdx,0)

			MainTable.months[monthIdx].UpdateStats()

		if ChoosePerson.selectedPerson.get()!="-":
			fullName=ChoosePerson.selectedPerson.get()
			fullNameTab=fullName.split(" ")
			person=DataEngine.PersonList.GetPersonFromList(fullNameTab[0],fullNameTab[1])
			person.ResetCalendarData()

	def ClearTable():
		ChoosePerson.Clear()
		ChooseYear.Clear()

		for i in range(12):
			MainTable.months[i].Clear()
			MainTable.months[i].UpdateStats()

		MainTable.UpdateUrlopyAndZwolnienia()

	def UpdateUrlopyAndZwolnienia():
		 MainTable.sumUrlopyStr.set(str(MainTable.sumUrlopy))
		 MainTable.sumZwolnieniaStr.set(str(MainTable.sumZwolnienia))
		 MainTable.sumUrlopyOkoliczStr.set(str(MainTable.sumUrlopyOkolicz))

MonthNames=["Styczeń","Luty","Marzec","Kwiecien","Maj","Czerwiec","Lipiec","Sierpień","Wrzesien","Październik","Listopad","Grudzień"]

class Month:
	def __init__(self,master,monthVal_,currVal_):
		self.monthVal=monthVal_

		labelStr="{0}. {1}".format(str(self.monthVal),MonthNames[self.monthVal-1])
		self.monthLabel=Label(master,text=labelStr)
		self.monthLabel.grid(row=self.monthVal-1,column=0,sticky=W)

		self.daysFrame=Frame(master)
		self.daysFrame.grid(row=self.monthVal-1,column=1,sticky=N)

		self.daysFrame.bind("<<Update>>",lambda event : self.UpdateStats())

		self.days=[]

		for i in range(31):
			self.days.append(Day(self.daysFrame,i+1,self.monthVal,currVal_))

		self.sumUrlopy=0
		self.sumUrlopyStr=StringVar()
		self.sumUrlopyStr.set('0')

		self.sumZwolnienia=0
		self.sumZwolnieniaStr=StringVar()
		self.sumZwolnieniaStr.set('0')

		self.sumUrlopyOkolicz=0
		self.sumUrlopyOkoliczStr=StringVar()
		self.sumUrlopyOkoliczStr.set('0')
		
		self.sumUrlopyLabel=Label(master,width=10,height=1,bd=4,anchor=CENTER,textvariable=self.sumUrlopyStr,relief="groove")
		self.sumUrlopyLabel.grid(row=self.monthVal-1,column=2,sticky=E)

		self.sumZwolnieniaLabel=Label(master,width=10,height=1,bd=4,anchor=CENTER,textvariable=self.sumZwolnieniaStr,relief="groove")
		self.sumZwolnieniaLabel.grid(row=self.monthVal-1,column=3,sticky=E)

		self.sumUrlopyOkoliczLabel=Label(master,width=15,height=1,bd=4,anchor=CENTER,textvariable=self.sumUrlopyOkoliczStr,relief="groove")
		self.sumUrlopyOkoliczLabel.grid(row=self.monthVal-1,column=4,sticky=E)

	def UpdateStats(self):
		MainTable.sumUrlopy-=self.sumUrlopy
		MainTable.sumZwolnienia-=self.sumZwolnienia
		MainTable.sumUrlopyOkolicz-=self.sumUrlopyOkolicz

		self.sumUrlopy=0;
		self.sumZwolnienia=0
		self.sumUrlopyOkolicz=0
		for i in range(31):
			if self.days[i].GetVal()==1:
				self.sumUrlopy+=1
			elif self.days[i].GetVal()==2:
				self.sumZwolnienia+=1
			elif self.days[i].GetVal()==3:
				self.sumUrlopyOkolicz+=1

		self.sumUrlopyStr.set(str(self.sumUrlopy))
		self.sumZwolnieniaStr.set(str(self.sumZwolnienia))
		self.sumUrlopyOkoliczStr.set(str(self.sumUrlopyOkolicz))

		MainTable.sumUrlopy+=self.sumUrlopy
		MainTable.sumZwolnienia+=self.sumZwolnienia
		MainTable.sumUrlopyOkolicz+=self.sumUrlopyOkolicz

		MainTable.UpdateUrlopyAndZwolnienia()

		ShowFreeDaysLeft.Update()

	def SetDayVal(self,dayIdx,setVal):
		self.days[dayIdx].LoadVal(setVal)

	def GetDayVal(self,dayIdx):
		return self.days[dayIdx].GetVal()

	def Clear(self):
		for i in range(31):
			self.days[i].LoadVal(0)

class ChoosePerson:
	personList=[]
	selectedPerson=""
	selectMenu=None

	def __init__(self,master):
		fullPersonList=DataEngine.PersonList.GetFullPersonDataList()
		if len(fullPersonList)>0:
			for p in fullPersonList:
				entry=p.GetName()+" "+p.GetSurname()
				ChoosePerson.personList.append(entry)
		else:
			ChoosePerson.personList=["-"]

		ChoosePerson.selectedPerson=StringVar()
		ChoosePerson.selectedPerson.set(ChoosePerson.personList[0])

		ChoosePerson.selectMenu=OptionMenu(master,ChoosePerson.selectedPerson,*ChoosePerson.personList)
		ChoosePerson.selectMenu.grid(row=0,column=0,sticky=W,padx=10)
		ChoosePerson.selectMenu.config(width=40)

	def UpdatePersonList():
		fullPersonList=DataEngine.PersonList.GetFullPersonDataList()

		ChoosePerson.personList[:]=[]
		if len(fullPersonList)>0:
			for p in fullPersonList:
				entry=p.GetName()+" "+p.GetSurname()
				ChoosePerson.personList.append(entry)
		else:
			ChoosePerson.personList=["-"]

		if ChoosePerson.selectedPerson.get() not in ChoosePerson.personList:
			ChoosePerson.Select(ChoosePerson.personList[0])

		menu=ChoosePerson.selectMenu["menu"]
		menu.delete(0,"end")
		
		for person in ChoosePerson.personList:
			menu.add_command(label=person,command=lambda val = person : ChoosePerson.Select(val))

		ChooseYear.UpdateYearsList()

	def Select(name):
		ChoosePerson.selectedPerson.set(name)
		
		if name!="-":
			ChooseYear.UpdateYearsList()

			fullName=name.split(" ")
			person=DataEngine.PersonList.GetPersonFromList(fullName[0],fullName[1])

			year=ChooseYear.selectedYear

			MainTable.LoadTableDataFromPersonData(person,year)
		else:
			MainTable.ResetTableData()

		ShowFreeDaysLeft.UpdateData()

	def Clear():
		ChoosePerson.selectedPerson.set("-")
		ChoosePerson.personList[:]=["-"]
		menu=ChoosePerson.selectMenu["menu"]
		menu.delete(0,"end")
		menu.add_command(label="-",command=lambda val = "-" : ChoosePerson.Select(val))

class Day:
	def __init__(self,master,dayVal_,monthVal_,currVal_):
		self.dayVal=dayVal_
		self.monthVal=monthVal_
		self.currVal=currVal_
		self.masterWidget=master
		
		self.frame=Button(master,text=str(self.dayVal),bg="white",width=2,height=1,overrelief=SUNKEN)
		self.frame.grid(row=0,column=self.dayVal-1,sticky=W)
		self.frame.bind("<Button-1>",lambda event : self.SetVal())
		self.frame.bind("<<B1-Enter>>",lambda event : self.SetVal())

		self.set=0

	def SetVal(self):
		if ChoosePerson.selectedPerson.get()!="-":
			FileStatus.Set()

		if self.set!=0:
			if self.set!=self.currVal[0]:
				self.set=self.currVal[0]
			else:
				self.set=0
		else:
			self.set=self.currVal[0]
		
		if self.set==0:
			self.frame.config(bg="white")
		elif self.set==1:
			self.frame.config(bg="green")
		elif self.set==2:
			self.frame.config(bg="red")
		elif self.set==3:
			self.frame.config(bg="yellow")

		self.masterWidget.event_generate("<<Update>>")

		if ChoosePerson.selectedPerson.get() != "-":
			fullName=ChoosePerson.selectedPerson.get()
			year=ChooseYear.selectedYear
			fullNameTab=fullName.split(" ")
			person=DataEngine.PersonList.GetPersonFromList(fullNameTab[0],fullNameTab[1])
			person.LoadSingleVal(year,self.monthVal,self.dayVal,self.set)

	def GetVal(self):
		return self.set

	def LoadVal(self,val):
		self.set=val

		if self.set==0:
			self.frame.config(bg="white")
		elif self.set==1:
			self.frame.config(bg="green")
		elif self.set==2:
			self.frame.config(bg="red")
		elif self.set==3:
			self.frame.config(bg="yellow")


class Mode:
	urlopyButton=None
	zwolnieniaButton=None
	frame=None

	currVal=[]

	selectedVar=0

	def __init__(self,master,currentVal):
		self.frame=Frame(master)
		self.frame.grid(row=0,column=3,sticky=E,padx=15)

		self.selectedVal=IntVar()
		self.selectedVal=1

		self.currVal=currentVal
		self.selectedVar=IntVar()

		self.urlopyButton=Radiobutton(self.frame,text="Urlopy",selectcolor="green",variable=self.selectedVar,value=1,indicatoron=0,width=10,height=2,command=self.SetVariableVal,overrelief="groove")
		self.urlopyButton.grid(row=0,column=0,sticky=E)
		self.zwolnieniaButton=Radiobutton(self.frame,text="Zwolnienia",selectcolor="red",variable=self.selectedVar,value=2,indicatoron=0,width=10,height=2,command=self.SetVariableVal,overrelief="groove")
		self.zwolnieniaButton.grid(row=0,column=1,sticky=E)
		self.urlopyOkoliczButton=Radiobutton(self.frame,text="Urlopy\nOkolicznościowe",selectcolor="yellow",variable=self.selectedVar,value=3,indicatoron=0,width=15,height=2,command=self.SetVariableVal,overrelief="groove")
		self.urlopyOkoliczButton.grid(row=0,column=2,sticky=E)
		self.urlopyButton.select()

	def SetVariableVal(self):
		self.currVal[0]=self.selectedVar.get()




class ChooseYear:
	yearsList=[]
	yearsListStr=[]
	selectedYear=0
	selectedYearStr=""
	selectMenu=None
		
	def __init__(self,master):
		fullName=ChoosePerson.selectedPerson.get()
		ChooseYear.yearsList[:]=[]
		ChooseYear.yearsListStr[:]=[]

		if fullName != "-":
			fullNameTab=fullName.split(' ')
			fullPersonYearsCalendar=DataEngine.PersonList.GetPersonFromList(fullNameTab[0],fullNameTab[1]).GetAllCalendars()
			
			for calendar in fullPersonYearsCalendar:
				ChooseYear.yearsList.append(calendar.GetYear())
				ChooseYear.yearsListStr.append(str(calendar.GetYear()))
			
			ChooseYear.yearsList.reverse()
			ChooseYear.yearsListStr.reverse()
		else:
			ChooseYear.yearsList=[-1]
			ChooseYear.yearsListStr=["-"]

			
		ChooseYear.selectedYearStr=StringVar()
		ChooseYear.selectedYear=ChooseYear.yearsList[0]
		ChooseYear.selectedYearStr.set(ChooseYear.yearsListStr[0])
		
		ChooseYear.selectMenu=OptionMenu(master,ChooseYear.selectedYearStr,*ChooseYear.yearsListStr)
		ChooseYear.selectMenu.grid(row=0,column=0,sticky=W,padx=0)
		ChooseYear.selectMenu.config(width=10)

	def UpdateYearsList():
		fullName=ChoosePerson.selectedPerson.get()
		ChooseYear.yearsList[:]=[]
		ChooseYear.yearsListStr[:]=[]

		if fullName != "-":
			fullNameTab=fullName.split(' ')
			fullPersonYearsCalendar=DataEngine.PersonList.GetPersonFromList(fullNameTab[0],fullNameTab[1]).GetAllCalendars()
			
			for calendar in fullPersonYearsCalendar:
				yearVal=calendar.GetYear()
				ChooseYear.yearsList.append(yearVal)
				ChooseYear.yearsListStr.append(str(yearVal))
			
			ChooseYear.yearsList.reverse()
			ChooseYear.yearsListStr.reverse()
		else:
			ChooseYear.yearsList=[-1]
			ChooseYear.yearsListStr=["-"]

		if ChooseYear.selectedYear not in ChooseYear.yearsList:
			ChooseYear.selectedYear=ChooseYear.yearsList[0]
			ChooseYear.selectedYearStr.set(ChooseYear.yearsListStr[0])

		menu=ChooseYear.selectMenu["menu"]
		menu.delete(0,"end")
		
		for year in ChooseYear.yearsListStr:
			menu.add_command(label=year,command=lambda val=year : ChooseYear.Select(val))

	def Select(yearStr):
		ChooseYear.selectedYearStr.set(yearStr)
		ChooseYear.selectedYear=int(yearStr)
		
		if yearStr!="-":
			name=ChoosePerson.selectedPerson.get()
			fullName=name.split(" ")
			person=DataEngine.PersonList.GetPersonFromList(fullName[0],fullName[1])

			MainTable.LoadTableDataFromPersonData(person,int(yearStr))
		else:
			MainTable.ResetTableData()

		ShowFreeDaysLeft.UpdateData()

	def Clear():
		ChooseYear.yearsList[:]=[-1]
		ChooseYear.yearsListStr[:]=["-"]
		ChooseYear.selectedYear=-1
		ChooseYear.selectedYearStr.set("-")
		menu=ChooseYear.selectMenu["menu"]
		menu.delete(0,"end")
		menu.add_command(label="-",command=lambda val="-" : ChooseYear.Select(val))

class AddYear:
	def __init__(self,master_):
		self.button=Button(master_,text="Dodaj rok",command=self.Add,width=10,overrelief="groove")
		self.button.grid(row=0,column=1,padx=5)
		self.master=master_
		self.opened=0

	def Add(self):
		if ChoosePerson.selectedPerson.get()!="-" and self.opened==0:
			self.addRoot=Toplevel(self.master)
			ikonaDir=ConfigFile.mainDirectory+'logo_ikona.ico'
			self.addRoot.iconbitmap(ikonaDir)
			self.opened=1
			self.addRoot.protocol("WM_DELETE_WINDOW",self.Close)
			label=Label(self.addRoot,text="Dodaj rok")
			label.grid(row=0,column=0,padx=20,pady=20)
			self.addRootEntry=Entry(self.addRoot,width=30)
			self.addRootEntry.grid(row=1,column=0,padx=20)
			frame=Frame(self.addRoot)
			frame.grid(row=2,column=0)
			self.addRootOK=Button(frame,width=20,text="OK",command=self.Confirm)
			self.addRootOK.grid(row=0,column=0,padx=20,pady=20)
			self.addRootCancel=Button(frame,width=20,text="Anuluj",command=self.Close)
			self.addRootCancel.grid(row=0,column=1,padx=20,pady=20)

	def Close(self):
		self.opened=0
		self.addRoot.destroy()

	def Confirm(self):
		str=self.addRootEntry.get()
		valErrorFlag=0

		try:
			year=int(str)
		except ValueError:
			self.errorWindow=Toplevel(self.addRoot)
			self.errorMsg=Label(self.errorWindow,text="ERROR! Wrong year!",font=("Arial",12,"bold"))
			self.errorMsg.grid(row=0,column=0,padx=30,pady=30,sticky=N)
			valErrorFlag=1

		if valErrorFlag==0:
			fullName=ChoosePerson.selectedPerson.get()
			fullNameTab=fullName.split()

			person=DataEngine.PersonList.GetPersonFromList(fullNameTab[0],fullNameTab[1])
			checkYear=person.GetVacationCalendar(year)

			if checkYear!=None:
				self.errorWindow=Toplevel(self.addRoot)
				self.errorMsg=Label(self.errorWindow,text="Błąd! Rok został już przypisany do wybranej osoby!",font=("Arial",12,"bold"))
				self.errorMsg.grid(row=0,column=0,padx=30,pady=30,sticky=N)
			else:
				FileStatus.Set()

				person.LoadNewYear(year)
				ChooseYear.UpdateYearsList()

				fullName=ChoosePerson.selectedPerson.get()
				fullName=fullName.split()
				person=DataEngine.PersonList.GetPersonFromList(fullName[0],fullName[1])
				if person.GetVacationCalendar(year-1)!=None:
					person.SetYearFreeDaysLeftFromLastYear(year,person.GetYearBaseFreeDays(year-1) + person.GetYearFreeDaysFromLastYear(year-1) - person.GetYearVacationDays(year-1))
				else:
					person.SetYearFreeDaysLeftFromLastYear(year,0)
				ShowFreeDaysLeft.UpdateData()
				ShowFreeDaysLeft.Update()

				self.Close()
		
class ShowFreeDaysLeft:
	label1=None
	label2=None
	button=None
	daysLeftStr=None

	baseFreeDays=0
	baseFreeDaysStr=None
	freeDaysLastYear=0
	freeDaysLastYearStr=None
	usedFreeDays=0
	moreWndLabel1_1=None
	moreWndSetBaseFreeDays=None
	moreWndLabel2_1=None
	moreWndLabel2_2=None
	moreWndSetDaysLastYear=None
	moreWndLabel3_1=None
	moreWndLabel3_2=None
	moreWndLabel4_1=None
	moreWndLabel4_2=None
	moreWndOkButton=None

	moreWnd=None
	moreWndFrame=None
	moreWndFrame2=None

	master=None

	opened=0

	cyfry=['0','1','2','3','4','5','6','7','8','9']

	def Init(parent):
		ShowFreeDaysLeft.master=parent
		ShowFreeDaysLeft.daysLeftStr=StringVar()
		if ChoosePerson.selectedPerson.get()=="-":
			ShowFreeDaysLeft.daysLeftStr.set("-")
		else:
			ShowFreeDaysLeft.daysLeftStr.set(str(ShowFreeDaysLeft.baseFreeDays + ShowFreeDaysLeft.freeDaysLastYear - MainTable.sumUrlopy))
		#ShowFreeDaysLeft.daysLeftStr.set(str(ShowFreeDaysLeft.baseFreeDays + ShowFreeDaysLeft.freeDaysLastYear - MainTable.sumUrlopy))

		ShowFreeDaysLeft.label1=Label(parent,text="Pozostałych dni urlopu:",width=22,height=2,anchor=CENTER)
		ShowFreeDaysLeft.label1.grid(row=0,column=0,sticky=E)
		
		ShowFreeDaysLeft.label2=Label(parent,textvariable=ShowFreeDaysLeft.daysLeftStr,width=10,height=2,anchor=CENTER,bd=4,relief="groove")
		ShowFreeDaysLeft.label2.grid(row=0,column=1,sticky=E)

		ShowFreeDaysLeft.button=Button(parent,text="Więcej...",width=15,height=2,overrelief="groove",bd=2,command=ShowFreeDaysLeft.More)
		ShowFreeDaysLeft.button.grid(row=0,column=2,sticky=E)

	def Update():
		if ChoosePerson.selectedPerson.get()=="-":
			ShowFreeDaysLeft.daysLeftStr.set("-")
		else:
			ShowFreeDaysLeft.daysLeftStr.set(str(ShowFreeDaysLeft.baseFreeDays + ShowFreeDaysLeft.freeDaysLastYear - MainTable.sumUrlopy))

		fullName=ChoosePerson.selectedPerson.get()
		#fullName=fullName.split()
		if fullName!="-":
			fullName=fullName.split()
			if DataEngine.PersonList.GetPersonFromList(fullName[0],fullName[1]).GetVacationCalendar(ChooseYear.selectedYear+1)!=None:
				DataEngine.PersonList.GetPersonFromList(fullName[0],fullName[1]).SetYearFreeDaysLeftFromLastYear(ChooseYear.selectedYear+1,ShowFreeDaysLeft.baseFreeDays+ShowFreeDaysLeft.freeDaysLastYear-MainTable.sumUrlopy)

	def UpdateData():
		fullName=ChoosePerson.selectedPerson.get()
		if fullName!="-":
			fullName=fullName.split(" ")
			ShowFreeDaysLeft.baseFreeDays=DataEngine.PersonList.GetPersonFromList(fullName[0],fullName[1]).GetYearBaseFreeDays(ChooseYear.selectedYear)
			ShowFreeDaysLeft.freeDaysLastYear=DataEngine.PersonList.GetPersonFromList(fullName[0],fullName[1]).GetYearFreeDaysFromLastYear(ChooseYear.selectedYear)
			ShowFreeDaysLeft.Update()

	def More():
		if ChoosePerson.selectedPerson.get()!="-" and ShowFreeDaysLeft.opened==0:
			ShowFreeDaysLeft.moreWnd=Toplevel(ShowFreeDaysLeft.master)
			ikonaDir=ConfigFile.mainDirectory+'logo_ikona.ico'
			ShowFreeDaysLeft.moreWnd.iconbitmap(ikonaDir)

			ShowFreeDaysLeft.opened=1
			ShowFreeDaysLeft.moreWnd.protocol("WM_DELETE_WINDOW",ShowFreeDaysLeft.CloseProtocol)

			ShowFreeDaysLeft.moreWndFrame=Frame(ShowFreeDaysLeft.moreWnd)
			ShowFreeDaysLeft.moreWndFrame.grid(row=0,column=0,padx=30,pady=10)

			ShowFreeDaysLeft.moreWndFrame2=Frame(ShowFreeDaysLeft.moreWnd)
			ShowFreeDaysLeft.moreWndFrame2.grid(row=1,column=0,pady=10,padx=30)

			ShowFreeDaysLeft.moreWndLabel1_1=Label(ShowFreeDaysLeft.moreWndFrame,width=35,height=2,text="Przysługujących dni urlopu:",anchor=W)
			ShowFreeDaysLeft.moreWndLabel1_1.grid(row=0,column=0,sticky=E)

			#ShowFreeDaysLeft.moreWndLabel1_2=Label(ShowFreeDaysLeft.moreWndFrame,width=10,height=2,text=str(ShowFreeDaysLeft.baseFreeDays))
			ShowFreeDaysLeft.baseFreeDaysStr=StringVar()
			ShowFreeDaysLeft.baseFreeDaysStr.set(str(ShowFreeDaysLeft.baseFreeDays))
			ShowFreeDaysLeft.baseFreeDaysStr.trace("w",ShowFreeDaysLeft.CheckInsertedBaseDays)
			#ShowFreeDaysLeft.moreWndLabel1_2.grid(row=0,column=1,sticky=E)
			ShowFreeDaysLeft.moreWndSetBaseFreeDays=Entry(ShowFreeDaysLeft.moreWndFrame,width=3,font=("Arial",12),textvariable=ShowFreeDaysLeft.baseFreeDaysStr)
			ShowFreeDaysLeft.moreWndSetBaseFreeDays.grid(row=0,column=1,sticky=N)

			ShowFreeDaysLeft.moreWndLabel2_1=Label(ShowFreeDaysLeft.moreWndFrame,width=35,height=2,text="Dni urlopu pozostałe z poprzedniego roku:",anchor=W)
			ShowFreeDaysLeft.moreWndLabel2_1.grid(row=1,column=0,sticky=E)

			fullName=ChoosePerson.selectedPerson.get()
			fullName=fullName.split(" ")
			if DataEngine.PersonList.GetPersonFromList(fullName[0],fullName[1]).GetVacationCalendar(ChooseYear.selectedYear-1)!=None:
				ShowFreeDaysLeft.freeDaysLastYearStr=None
				ShowFreeDaysLeft.moreWndLabel2_2=Label(ShowFreeDaysLeft.moreWndFrame,width=10,height=2,text=str(ShowFreeDaysLeft.freeDaysLastYear))
				ShowFreeDaysLeft.moreWndLabel2_2.grid(row=1,column=1,sticky=E)
			else:
				ShowFreeDaysLeft.freeDaysLastYearStr=StringVar()
				ShowFreeDaysLeft.freeDaysLastYearStr.set(str(ShowFreeDaysLeft.freeDaysLastYear))
				ShowFreeDaysLeft.freeDaysLastYearStr.trace("w",ShowFreeDaysLeft.CheckInsertedLastYearDays)
				DataEngine.PersonList.GetPersonFromList(fullName[0],fullName[1]).SetYearFreeDaysLeftFromLastYear(ChooseYear.selectedYear,0)					
				ShowFreeDaysLeft.moreWndSetDaysLastYear=Entry(ShowFreeDaysLeft.moreWndFrame,width=3,font=("Arial",12),textvariable=ShowFreeDaysLeft.freeDaysLastYearStr)
				ShowFreeDaysLeft.moreWndSetDaysLastYear.grid(row=1,column=1,sticky=N)

			ShowFreeDaysLeft.moreWndLabel3_1=Label(ShowFreeDaysLeft.moreWndFrame,width=35,height=2,text="Wykorzystane dni urlopu:",anchor=W)
			ShowFreeDaysLeft.moreWndLabel3_1.grid(row=2,column=0,sticky=E)

			ShowFreeDaysLeft.moreWndLabel3_2=Label(ShowFreeDaysLeft.moreWndFrame,width=10,height=2,text=str(MainTable.sumUrlopy))
			ShowFreeDaysLeft.moreWndLabel3_2.grid(row=2,column=1,sticky=E)

			ShowFreeDaysLeft.moreWndLabel4_1=Label(ShowFreeDaysLeft.moreWndFrame,width=35,height=2,text="Pozostałe dni urlopu:",anchor=W)
			ShowFreeDaysLeft.moreWndLabel4_1.grid(row=3,column=0,sticky=E)

			ShowFreeDaysLeft.moreWndLabel4_2=Label(ShowFreeDaysLeft.moreWndFrame,width=10,height=2,text=str(ShowFreeDaysLeft.baseFreeDays + ShowFreeDaysLeft.freeDaysLastYear - MainTable.sumUrlopy))
			ShowFreeDaysLeft.moreWndLabel4_2.grid(row=3,column=1,sticky=E)

			ShowFreeDaysLeft.moreWndOkButton=Button(ShowFreeDaysLeft.moreWndFrame2,text='OK',command=ShowFreeDaysLeft.CloseProtocol,width=10,height=2)
			ShowFreeDaysLeft.moreWndOkButton.grid(row=0,column=0,sticky=N)


	def CheckInsertedBaseDays(*args):
		if(len(ShowFreeDaysLeft.baseFreeDaysStr.get())>0):
			if(len(ShowFreeDaysLeft.baseFreeDaysStr.get())>3):
				ShowFreeDaysLeft.baseFreeDaysStr.set((ShowFreeDaysLeft.baseFreeDaysStr.get())[:3])
			elif(not (ShowFreeDaysLeft.baseFreeDaysStr.get())[-1] in ShowFreeDaysLeft.cyfry):
				ShowFreeDaysLeft.baseFreeDaysStr.set((ShowFreeDaysLeft.baseFreeDaysStr.get())[:len(ShowFreeDaysLeft.baseFreeDaysStr.get())-1])

		if(len(ShowFreeDaysLeft.baseFreeDaysStr.get())>0):
			ShowFreeDaysLeft.baseFreeDays=int(ShowFreeDaysLeft.baseFreeDaysStr.get())
		else:
			ShowFreeDaysLeft.baseFreeDays=0

		ShowFreeDaysLeft.UpdateFreeDaysLeft()
		FileStatus.Set()

	def CheckInsertedLastYearDays(*args):
		if len(ShowFreeDaysLeft.freeDaysLastYearStr.get())>0:
			if(len(ShowFreeDaysLeft.freeDaysLastYearStr.get())>3):
				ShowFreeDaysLeft.freeDaysLastYearStr.set((ShowFreeDaysLeft.freeDaysLastYearStr.get())[:3])
			elif(not (((ShowFreeDaysLeft.freeDaysLastYearStr.get())[-1] in ShowFreeDaysLeft.cyfry) and ((ShowFreeDaysLeft.freeDaysLastYearStr.get())[-1]!='-'))):
				ShowFreeDaysLeft.freeDaysLastYearStr.set((ShowFreeDaysLeft.freeDaysLastYearStr.get())[:len(ShowFreeDaysLeft.freeDaysLastYearStr.get())-1])

		if(len(ShowFreeDaysLeft.freeDaysLastYearStr.get())>0):
			ShowFreeDaysLeft.freeDaysLastYear=int(ShowFreeDaysLeft.freeDaysLastYearStr.get())
		else:
			ShowFreeDaysLeft.freeDaysLastYear=0

		ShowFreeDaysLeft.UpdateFreeDaysLeft()
		FileStatus.Set()

	def CloseProtocol():
		ShowFreeDaysLeft.opened=0
		ShowFreeDaysLeft.moreWnd.destroy()

	def UpdateFreeDaysLeft():
		ShowFreeDaysLeft.daysLeftStr.set(ShowFreeDaysLeft.baseFreeDays + ShowFreeDaysLeft.freeDaysLastYear - MainTable.sumUrlopy)
		ShowFreeDaysLeft.moreWndLabel4_2.config(text=str(ShowFreeDaysLeft.baseFreeDays + ShowFreeDaysLeft.freeDaysLastYear - MainTable.sumUrlopy))

		fullName=ChoosePerson.selectedPerson.get()
		fullName=fullName.split()
		if fullName!="-":
			DataEngine.PersonList.GetPersonFromList(fullName[0],fullName[1]).SetYearBaseFreeDays(ChooseYear.selectedYear,ShowFreeDaysLeft.baseFreeDays)
			if ShowFreeDaysLeft.freeDaysLastYearStr!=None:
				DataEngine.PersonList.GetPersonFromList(fullName[0],fullName[1]).SetYearFreeDaysLeftFromLastYear(ChooseYear.selectedYear,ShowFreeDaysLeft.freeDaysLastYear)

			#DataEngine.PersonList.GetPersonFromList(fullName[0],fullName[1]).SetYearFreeDaysLeftFromLastYear(ChooseYear.selectedYear+1,ShowFreeDaysLeft.baseFreeDays+ShowFreeDaysLeft.freeDaysLastYear-MainTable.sumUrlopy)


