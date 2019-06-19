import unicodedata
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Image
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont  
from reportlab.pdfbase.pdfmetrics import stringWidth 
from reportlab.lib import utils
from FileManager import ConfigFile

def CreatePDF(filename_,name_,surname_,year_,data_,baseFreeDays_,freeDaysLastYear_):
	pdfmetrics.registerFont(TTFont('Arial', ConfigFile.mainDirectory+'arial.ttf'))
	pdfmetrics.registerFont(TTFont('ArialBold',ConfigFile.mainDirectory+"arial_bold.ttf"))

	data=[[i for i in range(35)] for j in range(12)]

	widthTab=35*[0.7*cm]
	widthTab[0]=2.0*cm
	widthTab[32]=1.5*cm
	widthTab[33]=2.0*cm
	widthTab[34]=1.5*cm

	data[0][0]='Styczeń'
	data[1][0]='Luty'
	data[2][0]='Marzec'
	data[3][0]='Kwiecień'
	data[4][0]='Maj'
	data[5][0]='Czerwiec'
	data[6][0]='Lipiec'
	data[7][0]='Sierpień'
	data[8][0]='Wrzesień'
	data[9][0]='Październik'
	data[10][0]='Listopad'
	data[11][0]='Grudzień'

	overallSumUrlopy=0
	overallSumZwolnienia=0
	overallSumUrlopyOkolicz=0
	overallPozostaleUrlopy=0
	for i in range(12):
		sumUrlopy=0
		sumZwolnienia=0
		sumUrlopyOkolicz=0
		for j in range(31):
			if data_[i][j]==1:
				sumUrlopy+=1
			elif data_[i][j]==2:
				sumZwolnienia+=1
			elif data_[i][j]==3:
				sumUrlopyOkolicz+=1

		data[i][32]=sumUrlopy
		data[i][33]=sumZwolnienia
		data[i][34]=sumUrlopyOkolicz

		overallSumUrlopy+=sumUrlopy
		overallSumZwolnienia+=sumZwolnienia
		overallSumUrlopyOkolicz+=sumUrlopyOkolicz

	overallPozostaleUrlopy=baseFreeDays_ + freeDaysLastYear_ - overallSumUrlopy

	t=Table(data,widthTab,12*[0.7*cm])

	t.setStyle(TableStyle([('INNERGRID',(0,0),(-1,-1),0.25,colors.black),
						   ('FONT',(0,0),(-1,-1),"Arial"),
						   ('ALIGN',(0,0),(-1,-1),'CENTER'),
						   ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
						   ('BOX',(0,0),(-1,-1),0.25,colors.black)]))


	for i in range(12):
		for j in range(31):
			if data_[i][j]==1:
				t.setStyle(TableStyle([('BACKGROUND',(j+1,i),(j+1,i),colors.green)]))
			elif data_[i][j]==2:
				t.setStyle(TableStyle([('BACKGROUND',(j+1,i),(j+1,i),colors.red)]))
			elif data_[i][j]==3:
				t.setStyle(TableStyle([('BACKGROUND',(j+1,i),(j+1,i),colors.yellow)]))

	data2=[['suma\nurlopy','suma\nzwolnienia','suma\nurlopy\nokolicz.']]

	t2=Table(data2,[1.5*cm,2.0*cm,1.5*cm],1*[1.4*cm])

	t2.setStyle(TableStyle([('INNERGRID',(0,0),(-1,-1),0.25,colors.black),
							('FONT',(0,0),(-1,-1),"Arial"),
							('ALIGN',(0,0),(-1,-1),"CENTER"),
							('VALIGN',(0,0),(-1,-1),'MIDDLE'),
							('BOX',(0,0),(-1,-1),0.25,colors.black)]))

	data3=[['','-','urlopy']]

	t3=Table(data3,[0.7*cm,1.0*cm,3.0*cm],[0.7*cm])
	t3.setStyle(TableStyle([('FONT',(0,0),(-1,-1),"Arial"),
							('ALIGN',(0,0),(1,0),"CENTER"),
							('ALIGN',(2,0),(2,0),"LEFT"),
							('BACKGROUND',(0,0),(0,0),colors.green)]))

	data3[0][2]='zwolnienia'
	t4=Table(data3,[0.7*cm,1.0*cm,3.0*cm],[0.7*cm])
	t4.setStyle(TableStyle([('FONT',(0,0),(-1,-1),"Arial"),
							('ALIGN',(0,0),(1,0),"CENTER"),
							('ALIGN',(2,0),(2,0),"LEFT"),
							('BACKGROUND',(0,0),(0,0),colors.red)]))

	data3[0][2]='urlopy okolicznościowe'
	t5=Table(data3,[0.7*cm,1.0*cm,3.0*cm],[0.7*cm])
	t5.setStyle(TableStyle([('FONT',(0,0),(-1,-1),"Arial"),
							('ALIGN',(0,0),(1,0),"CENTER"),
							('ALIGN',(2,0),(2,0),"LEFT"),
							('BACKGROUND',(0,0),(0,0),colors.yellow)]))

	data4=[['Łącznie',overallSumUrlopy,overallSumZwolnienia,overallSumUrlopyOkolicz]]
	t6=Table(data4,[2.0*cm,1.5*cm,2.0*cm,1.5*cm],[1.0*cm])
	t6.setStyle(TableStyle([('INNERGRID',(1,0),(-1,-1),0.25,colors.black),
							('FONT',(0,0),(-1,-1),"Arial"),
							('ALIGN',(0,0),(-1,-1),"CENTER"),
							('VALIGN',(0,0),(-1,-1),'MIDDLE'),
							('BOX',(1,0),(-1,-1),0.25,colors.black)]))

	data5=[['Pozostałych dni urlopu:',overallPozostaleUrlopy]]
	t7=Table(data5,[5.0*cm,1.0*cm],[1.4*cm])
	t7.setStyle(TableStyle([('FONT',(0,0),(-1,-1),"ArialBold"),
							('ALIGN',(0,0),(-1,-1),"CENTER"),
							('VALIGN',(0,0),(-1,-1),'MIDDLE')]))

	doc=canvas.Canvas(filename_,pagesize=landscape(A4))

	t.wrapOn(doc,0,0)
	t.drawOn(doc,0.5*cm,5.6*cm)

	t2.wrapOn(doc,0,0)
	t2.drawOn(doc,24.2*cm,14.0*cm)

	t3.wrapOn(doc,0,0)
	t3.drawOn(doc,13*cm,4*cm)

	t4.wrapOn(doc,0,0)
	t4.drawOn(doc,13*cm,3*cm)

	t5.wrapOn(doc,0,0)
	t5.drawOn(doc,13*cm,2*cm)

	t6.wrapOn(doc,0,0)
	t6.drawOn(doc,22.2*cm,4.6*cm)

	t7.wrapOn(doc,0,0)
	t7.drawOn(doc,22.0*cm,3.3*cm)

	doc.setFont('ArialBold',14)

	year="ROK "
	year+=year_
	textwidth=stringWidth(year,"ArialBold",14)
	yearPos=(29.7*cm-textwidth)/2
	textObject=doc.beginText()
	textObject.setTextOrigin(yearPos,15.4*cm)
	textObject.textLine(text=year)
	doc.drawText(textObject)

	name=name_
	surname=surname_
	namePos=0.5*cm

	textObject=doc.beginText()
	textObject.setTextOrigin(0.5*cm,17.4*cm)
	textObject.setFont("ArialBold",14)
	textObject.textOut("Imię: ")
	textObject.setFont("Arial",14)
	textObject.textOut(name)
	textObject.textLine("")
	textObject.getStartOfLine()
	textObject.setFont("ArialBold",14)
	textObject.textOut("Nazwisko: ")
	textObject.setFont("Arial",14)
	textObject.textOut(surname)
	textObject.getStartOfLine()
	doc.drawText(textObject)

	doc.setFont("ArialBold",size=16)
	title="Wykaz urlopów i zwolnień"
	textwidth=stringWidth(title,"ArialBold",16)
	titlePos=(29.7*cm-textwidth)/2
	textObject=doc.beginText()
	textObject.setTextOrigin(titlePos,19.4*cm)
	textObject.textLine(title)
	doc.drawText(textObject)

	im=utils.ImageReader(ConfigFile.mainDirectory+"logo2.png")
	iw,ih=im.getSize()
	aspect=ih/float(iw)

	imageWidth=3*cm
	imageHeight=imageWidth*aspect
	im=Image(ConfigFile.mainDirectory+"logo2.png",imageWidth,imageHeight)

	im.wrapOn(doc,0,0)
	im.drawOn(doc,26.2*cm,16.3*cm)

	doc.save()
