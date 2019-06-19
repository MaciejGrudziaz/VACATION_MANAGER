import sys

class PersonList:
	personDataList=[]
	dataEditFlag=0

	def AddPersonToList(newPerson):
		fullName=[newPerson.GetName(),newPerson.GetSurname()]
		if fullName not in PersonList.personDataList:
			PersonList.personDataList.append(newPerson)
			PersonList.dataEditFlag=1

	def GetPersonFromList(index):
		if index>=0 and index<len(PersonList.personDataList):
			return PersonList.personDataList[index]
		else:
			return None

	def GetPersonFromList(imie,nazwisko):
		fullName=[imie,nazwisko]
		if fullName in PersonList.personDataList:
			personIdx=PersonList.personDataList.index(fullName)
			return PersonList.personDataList[personIdx]
		else:
			return None

	def DeletePersonFromList(imie,nazwisko):
		fullName=[imie,nazwisko]
		
		if fullName in PersonList.personDataList:
			PersonList.personDataList.remove(fullName)

		PersonList.dataEditFlag=1

	def GetFullPersonDataList():
		return PersonList.personDataList

	def ClearAllData():
		PersonList.personDataList[:]=[]

	def ClearDataEditFlag():
		PersonList.dataEditFlag=0
		
class PersonData:
	def __init__(self,imie_,nazwisko_,year_=-1):
		self.imie=imie_
		self.nazwisko=nazwisko_
		#self.vacationCalendar=[[0 for i in range(31)] for j in range(12)]

		self.yearsList=[]
		if year_!=-1:
			self.yearsList.append(VacationYearData(year_))

	def GetName(self):
		return self.imie

	def GetSurname(self):
		return self.nazwisko

	def SetName(self,name):
		self.imie=name
		PersonList.dataEditFlag=1

	def SetSurname(self,surname):
		self.nazwisko=surname
		PersonList.dataEditFlag=1

	def GetAllCalendars(self):
		return self.yearsList

	def GetVacationCalendar(self,year):
		if year in self.yearsList:
			idx=self.yearsList.index(year)
			return self.yearsList[idx].GetVacationCalendar()
		else:
		   return None

	def  GetYearBaseFreeDays(self,year):
		if year in self.yearsList:
			idx=self.yearsList.index(year)
			return self.yearsList[idx].GetBaseFreeDays()
		else:
			return None

	def GetYearFreeDaysFromLastYear(self,year):
		if year in self.yearsList:
			idx=self.yearsList.index(year)
			return self.yearsList[idx].GetFreeDaysFromLastYear()
		else:
			return None

	def SetYearBaseFreeDays(self,year,baseFreeDays):
		if year in self.yearsList:
			idx=self.yearsList.index(year)
			self.yearsList[idx].LoadBaseFreeDays(baseFreeDays)

		year+=1	
		while year in self.yearsList:
			idx=self.yearsList.index(year)
			idx2=self.yearsList.index(year-1)
			self.yearsList[idx].LoadFreeDaysFromLastYear(self.yearsList[idx2].GetBaseFreeDays() + self.yearsList[idx2].GetFreeDaysFromLastYear() - self.yearsList[idx2].GetVacationDays())
			year+=1

	def SetYearFreeDaysLeftFromLastYear(self,year,freeDaysFromLastYear):
		if year in self.yearsList:
			idx=self.yearsList.index(year)
			self.yearsList[idx].LoadFreeDaysFromLastYear(freeDaysFromLastYear)

		year+=1	
		while year in self.yearsList:
			idx=self.yearsList.index(year)
			idx2=self.yearsList.index(year-1)
			self.yearsList[idx].LoadFreeDaysFromLastYear(self.yearsList[idx2].GetBaseFreeDays() + self.yearsList[idx2].GetFreeDaysFromLastYear() - self.yearsList[idx2].GetVacationDays())
			year+=1

	def LoadCalendarData(self,year,calendar):
		if year in yearsList:
			idx=self.yearsList.index(year)
			self.yearsList[idx].LoadCalendarData(calendar)
		else:
			self.yearsList.append(VacationYearData(year))
			idx=len(self.yearsList)-1
			self.yearsList[idx].LoadCalendarData(calendar)
			self.yearsList.sort(key=lambda val : val.GetYear(),reverse=True)
		PersonList.dataEditFlag=1

	def LoadCalendarSingleMonth(self,year,monthIdx,monthData):
		if year in self.yearsList:
			idx=self.yearsList.index(year)
			self.yearsList[idx].LoadCalendarSingleMonth(monthIdx,monthData)
			PersonList.dataEditFlag=1

	def ResetCalendarData(self,year):
		if year in self.yearsList:
			idx=self.yearsList.index(year)
			self.yearsList[idx].ResetCalendarData()
			PersonList.dataEditFlag=1

	def LoadSingleVal(self,year,month,day,val):
		if year in self.yearsList:
			idx=self.yearsList.index(year)
			self.yearsList[idx].LoadSingleVal(month,day,val)
			PersonList.dataEditFlag=1

	def LoadNewYear(self,year):
		if year not in self.yearsList:
			self.yearsList.append(VacationYearData(year))
			self.yearsList.sort(key=lambda val : val.GetYear())

	def GetYearVacationDays(self,year):
		if year in self.yearsList:
			idx=self.yearsList.index(year)
			return self.yearsList[idx].GetVacationDays()
		else:
			return -1


	def __eq__(self,other):
		if self.imie==other[0] and self.nazwisko==other[1]:
			return True
		else:
			return False


class VacationYearData:
	def __init__(self,year_):
		self.year=year_
		self.vacationCalendar=[[0 for i in range(31)] for j in range(12)]
		self.baseFreeDays=26;
		self.lastYearFreeDays=0;

	def GetVacationCalendar(self):
		return self.vacationCalendar

	def LoadCalendarData(self,calendar):
		self.vacationCalendar=calendar
		PersonList.dataEditFlag=1

	def LoadCalendarSingleMonth(self,monthIdx,monthData):
		self.vacationCalendar[monthIdx]=monthData
		PersonList.dataEditFlag=1

	def ResetCalendarData(self):
		self.vacationCalendar[:]=[[0 for i in range(31)] for j in range(12)]
		PersonList.dataEditFlag=1

	def LoadSingleVal(self,month,day,val):
		self.vacationCalendar[month-1][day-1]=val
		PersonList.dataEditFlag=1

	def LoadBaseFreeDays(self,baseFreeDays):
		self.baseFreeDays=baseFreeDays

	def LoadFreeDaysFromLastYear(self,freeDaysFromLastYear):
		self.lastYearFreeDays=freeDaysFromLastYear

	def GetBaseFreeDays(self):
		return self.baseFreeDays

	def GetFreeDaysFromLastYear(self):
		return self.lastYearFreeDays

	def GetYear(self):
		return self.year

	def GetVacationDays(self):
		vacationDays=0

		for month in self.vacationCalendar:
			for day in month:
				if day==1:
					vacationDays+=1

		return vacationDays

	def __eq__(self,other):
		if self.year==other:
			return True
		else:
			return False