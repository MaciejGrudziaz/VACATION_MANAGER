import sys
import DataEngine
import getpass

class InputFile:
	root=None

	def __init__(self,filename):


		ConfigFile.lastDataFilename=filename

		self.errorFlag=0
		self.personList=[]
		try:
			self.file=open(filename,"rb")
		except IOError:
			self.errorFlag=1

		if self.errorFlag==0:
			titleStr="Menedżer urlopów - "
			titleStr+=filename
			InputFile.root.title(titleStr)
			FileStatus.currentTitle=titleStr
			FileStatus.Reset()

			data=self.file.read()
			
			personCount=data[0]
			dataPtr=1

			for pIdx in range(personCount):
				if data[dataPtr:dataPtr+4]==bytearray([0x0a,0x0b,0x0c,0x0d]):
					dataPtr+=4;
					name=""
					while data[dataPtr:dataPtr+4]!=bytearray([0x01,0x0e,0x0a,0x09]) and data[dataPtr:dataPtr+4]!=bytearray([0x0d,0x0c,0x0b,0x0a]):
						name+=data[dataPtr:dataPtr+1].decode("iso-8859-2")
						dataPtr+=1

					fullName=name.split(" ")
					person=DataEngine.PersonData(fullName[0],fullName[1])

					
					while data[dataPtr:dataPtr+4]==bytearray([0x01,0x0e,0x0a,0x09]):
						dataPtr+=4
						yearBytes=[0x00,0x00]
						yearBytes[0]=data[dataPtr]
						yearBytes[1]=data[dataPtr+1]
						dataPtr+=2
						
						yearVal=(yearBytes[0]<<8)+yearBytes[1]

						person.LoadNewYear(yearVal)

						if data[dataPtr:dataPtr+4]==bytearray([0x0b,0x0a,0x05,0x0e]):
							dataPtr+=4
							baseFreeDaysBytes=[0x00,0x00]
							baseFreeDaysBytes[0]=data[dataPtr]
							baseFreeDaysBytes[1]=data[dataPtr+1]
							dataPtr+=2
							baseFreeDaysVal=(baseFreeDaysBytes[0]<<8)+baseFreeDaysBytes[1]

							person.SetYearBaseFreeDays(yearVal,baseFreeDaysVal)

							freeDaysLastYearBytes=[0x00,0x00]
							freeDaysLastYearBytes[0]=(data[dataPtr])&0x7F
							freeDaysLastYearBytes[1]=data[dataPtr+1]
							if data[dataPtr]&0x80 == 0x80:
								freeDaysLastYearVal=-((freeDaysLastYearBytes[0]<<8)+freeDaysLastYearBytes[1])
							else:
								freeDaysLastYearVal=(freeDaysLastYearBytes[0]<<8)+freeDaysLastYearBytes[1]
							dataPtr+=2

							person.SetYearFreeDaysLeftFromLastYear(yearVal,freeDaysLastYearVal)

						while data[dataPtr:dataPtr+4]==bytearray([0x0d,0x0a,0x07,0x0a]):
							dataPtr+=4
							month=[0 for i in range(31)]
							if data[dataPtr]==0xff:
								dataPtr+=1
								monthIdx=data[dataPtr]
								dataPtr+=1

								urlopycount=data[dataPtr]
								dataPtr+=1
								for i in range(urlopycount):
									month[data[dataPtr]]=1
									dataPtr+=1

								zwolnieniaCount=data[dataPtr]
								dataPtr+=1
								for i in range(zwolnieniaCount):
									month[data[dataPtr]]=2
									dataPtr+=1

							elif data[dataPtr]==0xfe:
								dataPtr+=1
								monthIdx=data[dataPtr]
								dataPtr+=1

								urlopyCount=data[dataPtr]
								dataPtr+=1
								for i in range(urlopyCount):
									month[data[dataPtr]]=1
									dataPtr+=1

							elif data[dataPtr]==0xfd:
								dataPtr+=1
								monthIdx=data[dataPtr]
								dataPtr+=1

								zwolnieniaCount=data[dataPtr]
								dataPtr+=1
								for i in range(zwolnieniaCount):
									month[data[dataPtr]]=2
									dataPtr+=1
							
							elif data[dataPtr]==0xfc:
								dataPtr+=1
								monthIdx=data[dataPtr]
								dataPtr+=1

								urlopyCount=data[dataPtr]
								dataPtr+=1
								for i in range(urlopyCount):
									month[data[dataPtr]]=1
									dataPtr+=1

								zwolnieniaCount=data[dataPtr]
								dataPtr+=1
								for i in range(zwolnieniaCount):
									month[data[dataPtr]]=2
									dataPtr+=1

								urlopyOkoliczCount=data[dataPtr]
								dataPtr+=1
								for i in range(urlopyOkoliczCount):
									month[data[dataPtr]]=3
									dataPtr+=1

							elif data[dataPtr]==0xfb:
								dataPtr+=1
								monthIdx=data[dataPtr]
								dataPtr+=1

								urlopyCount=data[dataPtr]
								dataPtr+=1
								for i in range(urlopyCount):
									month[data[dataPtr]]=1
									dataPtr+=1

								urlopyOkoliczCount=data[dataPtr]
								dataPtr+=1
								for i in range(urlopyOkoliczCount):
									month[data[dataPtr]]=3
									dataPtr+=1

							elif data[dataPtr]==0xfa:
								dataPtr+=1
								monthIdx=data[dataPtr]
								dataPtr+=1

								zwolnieniaCount=data[dataPtr]
								dataPtr+=1
								for i in range(zwolnieniaCount):
									month[data[dataPtr]]=2
									dataPtr+=1

								urlopyOkoliczCount=data[dataPtr]
								dataPtr+=1
								for i in range(urlopyOkoliczCount):
									month[data[dataPtr]]=3
									dataPtr+=1

							elif data[dataPtr]==0xf9:
								dataPtr+=1
								monthIdx=data[dataPtr]
								dataPtr+=1

								urlopyOkoliczCount=data[dataPtr]
								dataPtr+=1
								for i in range(urlopyOkoliczCount):
									month[data[dataPtr]]=3
									dataPtr+=1
							else:
								self.errorFlag=2
								break

							person.LoadCalendarSingleMonth(yearVal,monthIdx,month)

					if self.errorFlag==2:
						break

				else:
					self.errorFlag=2
					break

				if data[dataPtr:dataPtr+4]==bytearray([0x0d,0x0c,0x0b,0x0a]):
					self.personList.append(person)
					dataPtr+=4

			self.file.close()

	def ClearAndWriteDataToDataEngine(self):
		DataEngine.PersonList.ClearAllData()

		for person in self.personList:
			DataEngine.PersonList.AddPersonToList(person)

	def GetErrorFlag(self):
		return self.errorFlag
	
class OutputFile:
	root=None

	def __init__(self,filename):
		titleStr="Menedżer urlopów - "
		titleStr+=filename
		OutputFile.root.title(titleStr)
		FileStatus.currentTitle=titleStr
		FileStatus.Reset()

		ConfigFile.lastDataFilename=filename

		self.file=open(filename,"wb")
		self.file.truncate(0)

		personList=DataEngine.PersonList.GetFullPersonDataList()

		personsCount=[len(personList)]
		self.file.write(bytearray(personsCount))

		for person in personList:
			self.file.write(b"\x0a\x0b\x0c\x0d")

			fullName=person.GetName()+" "+person.GetSurname()
			bytes=bytearray(fullName,encoding="iso-8859-2")
			self.file.write(bytes)

			

			allYearsCalendar=person.GetAllCalendars()

			for yearData in allYearsCalendar:
			
				urlopy=[[] for i in range(12)]
				zwolnienia=[[] for i in range(12)]
				urlopyOkolicz=[[] for i in range(12)]

				vacationCalendar=yearData.GetVacationCalendar()
				
				self.file.write(b'\x01\x0E\x0A\x09')
				yearVal=yearData.GetYear()
				yearValBytes=[0x00,0x00]
				yearValBytes[0]=(yearVal & 0x0000FF00)>>8
				yearValBytes[1]=(yearVal & 0x00FF)
				self.file.write(bytearray(yearValBytes))

				self.file.write(b'\x0B\x0A\x05\x0E')
				baseFreeDays=yearData.GetBaseFreeDays()
				baseFreeDaysBytes=[0x00,0x00]
				baseFreeDaysBytes[0]=(baseFreeDays & 0xFF00)>>8
				baseFreeDaysBytes[1]=(baseFreeDays & 0x00FF)
				self.file.write(bytearray(baseFreeDaysBytes))

				freeDaysLastYear=yearData.GetFreeDaysFromLastYear()
				freeDaysLastYearBytes=[0x00,0x00]
				freeDaysLastYearBytes[0]=(abs(freeDaysLastYear) & 0xFF00)>>8
				freeDaysLastYearBytes[1]=(abs(freeDaysLastYear) & 0x00FF)
				if freeDaysLastYear<0:
					freeDaysLastYearBytes[0]|=0x80
				else:
					freeDaysLastYearBytes[0]&=0x7F

				self.file.write(bytearray(freeDaysLastYearBytes))

				for month in range(12):
					for day in range(31):
						if vacationCalendar[month][day]==1:
							urlopy[month].append(day)
						if vacationCalendar[month][day]==2:
							zwolnienia[month].append(day)
						if vacationCalendar[month][day]==3:
							urlopyOkolicz[month].append(day)


				for month in range(12):
					urlopyCount=len(urlopy[month])
					zwolnieniaCount=len(zwolnienia[month])
					urlopyOkoliczCount=len(urlopyOkolicz[month])

					if urlopyCount>0 and zwolnieniaCount>0 and urlopyOkoliczCount==0:
						self.file.write(b"\x0d\x0a\x07\x0a\xff")
						monthList=[]
						monthList.append(month)
						monthList.append(urlopyCount)
						for day in urlopy[month]:
							monthList.append(day)
						monthList.append(zwolnieniaCount)
						for day in zwolnienia[month]:
							monthList.append(day)

						self.file.write(bytearray(monthList))
					elif urlopyCount>0 and urlopyOkoliczCount==0:
						self.file.write(b"\x0d\x0a\x07\x0a\xfe")
						monthList=[]
						monthList.append(month)
						monthList.append(urlopyCount)
						for day in urlopy[month]:
							monthList.append(day)

						self.file.write(bytearray(monthList))
					elif zwolnieniaCount>0 and urlopyOkoliczCount==0:
						self.file.write(b"\x0d\x0a\x07\x0a\xfd")
						monthList=[]
						monthList.append(month)
						monthList.append(zwolnieniaCount)
						for day in zwolnienia[month]:
							monthList.append(day)

						self.file.write(bytearray(monthList))
					elif urlopyOkoliczCount>0 and zwolnieniaCount>0 and urlopyCount>0:
						self.file.write(b'\x0d\x0a\x07\x0a\xfc')
						monthList=[]
						monthList.append(month)
						monthList.append(urlopyCount)
						for day in urlopy[month]:
							monthList.append(day)
						monthList.append(zwolnieniaCount)
						for day in zwolnienia[month]:
							monthList.append(day)
						monthList.append(urlopyOkoliczCount)
						for day in urlopyOkolicz[month]:
							monthList.append(day)
						
						self.file.write(bytearray(monthList))
					elif urlopyOkoliczCount>0 and urlopyCount>0:
						self.file.write(b'\x0d\x0a\x07\x0a\xfb')
						monthList=[]
						monthList.append(month)
						monthList.append(urlopyCount)
						for day in urlopy[month]:
							monthList.append(day)
						monthList.append(urlopyOkoliczCount)
						for day in urlopyOkolicz[month]:
							monthList.append(day)
						
						self.file.write(bytearray(monthList))
					elif urlopyOkoliczCount>0 and zwolnieniaCount>0:
						self.file.write(b'\x0d\x0a\x07\x0a\xfa')
						monthList=[]
						monthList.append(month)
						monthList.append(zwolnieniaCount)
						for day in zwolnienia[month]:
							monthList.append(day)
						monthList.append(urlopyOkoliczCount)
						for day in urlopyOkolicz[month]:
							monthList.append(day)
						
						self.file.write(bytearray(monthList))
					elif urlopyOkoliczCount>0:
						self.file.write(b'\x0d\x0a\x07\x0a\xf9')
						monthList=[]
						monthList.append(month)
						monthList.append(urlopyOkoliczCount)
						for day in urlopyOkolicz[month]:
							monthList.append(day)

						self.file.write(bytearray(monthList))

			self.file.write(b"\x0d\x0c\x0b\x0a")

		self.file.close()

class ConfigFile:
	lastDataFilename=""
	lastLocationWriteTo=""
	lastLocationReadFrom=""
	mainDirectory=""

	configFilename=""

	def Read():
		if ConfigFile.configFilename=="":
			username=getpass.getuser()
			ConfigFile.configFilename="C:/Users/"+username+"/AppData/Local/Urlopy/config.cfg"


		readSignatures=['addr','readLoc','writeLoc','mainDir']
		readSignaturesVal=[ConfigFile.lastDataFilename,ConfigFile.lastLocationReadFrom,ConfigFile.lastLocationWriteTo]

		try:
			file=open(ConfigFile.configFilename,"r")
		except OSError:
			return 1

		data=file.readlines()

		for line in data:
			linePtr=0
			if line[:4]=="addr":
				linePtr+=4
				while line[linePtr]==" " or line[linePtr]=="=":
					linePtr+=1

				ConfigFile.lastDataFilename=line[linePtr:-1]

			elif line[:7]=="readLoc":
				linePtr+=7
				while line[linePtr]==" " or line[linePtr]=="=":
					linePtr+=1
				ConfigFile.lastLocationReadFrom=line[linePtr:-1]
			elif line[:8]=="writeLoc":
				linePtr+=8
				while line[linePtr]==" " or line[linePtr]=="=":
					linePtr+=1
				ConfigFile.lastLocationWriteTo=line[linePtr:-1]
			elif line[:7]=="mainDir":
				linePtr+=7
				while line[linePtr]==" " or line[linePtr]=="=":
					linePtr+=1
				ConfigFile.mainDirectory=line[linePtr:-1]

		file.close()

		return 0

	def Update():
		if ConfigFile.configFilename=="":
			username=getpass.getuser()
			ConfigFile.configFilename="C:/Users/"+username+"/AppData/Local/Urlopy/config.cfg"


		updateSignatures=['addr','readLoc','writeLoc']
		lineUpdated=[0,0,0]
		updateSignaturesVal=[ConfigFile.lastDataFilename,ConfigFile.lastLocationReadFrom,ConfigFile.lastLocationWriteTo]
		#updateSignaturesLoc=[-1 for i in range(len(updateSignatures))]
		errorFlag=0

		try:
			file = open(ConfigFile.configFilename,"r")
		except OSError:
			errorFlag=1
		
		if errorFlag==0:
			data=file.readlines()
			file.close()
		else:
			data=[]

		if len(data)==0:
			file=open(ConfigFile.configFilename,"w+")
			for idx in range(len(updateSignatures)):
				line=updateSignatures[idx]+" = "+str(updateSignaturesVal[idx])+"\n"
				file.write(line)

			file.close()

		else:
			file=open(ConfigFile.configFilename,"w")
			file.truncate(0)

			for lineIdx in range(len(data)):
				line=data[lineIdx]
				for sigIdx in range(len(updateSignatures)):
					if line[:len(updateSignatures[sigIdx])]==updateSignatures[sigIdx]:
						lineUpdated[sigIdx]=1
						newLine=updateSignatures[sigIdx]+" = "+str(updateSignaturesVal[sigIdx])+"\n"
						data[lineIdx]=newLine
			
			for idx in range(len(lineUpdated)):
				if lineUpdated[idx]==0:
					newLine=updateSignatures[idx]+" = "+str(updateSignaturesVal[idx])+"\n"
					data.append(newLine)

			file.writelines(data)
			file.close()

class PDFfile:
	def CreatePDF(imie,nazwisko):
		personData=DataEngine.PersonList.GetPersonFromList(imie,nazwisko)

class FileStatus:
	fileEditFlag=0
	root=None	
	currentTitle=""

	def Set():
		if FileStatus.currentTitle=="":
			FileStatus.root.title("Menedżer urlopów*")
		else:
			newTitle=FileStatus.currentTitle+"*"
			FileStatus.root.title(newTitle)

		FileStatus.fileEditFlag=1

	def Reset():
		if FileStatus.currentTitle=="":
			FileStatus.root.title("Menedżer urlopów")
		else:
			FileStatus.root.title(FileStatus.currentTitle)

		FileStatus.fileEditFlag=0

	def NewFile():
		FileStatus.currentTitle=""
		FileStatus.fileEditFlag=0
		FileStatus.root.title("Menedżer urlopów")
