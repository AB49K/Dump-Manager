#!/bin/python
from openpyxl import load_workbook
from datetime import datetime
import csv
import sys
print("Generating spreadsheets")
now = datetime.now() # current date and time
#d = now.strftime("%d-%m-%Y")

#Get the date from system args, if none are supplied, use current date
d=sys.argv[1]
if d==None:
    d==now
colums="ABCDEFGHIJLMNOPQRSTUVWXYZ"
colums=list(colums)
# Start by opening the spreadsheet and selecting the main sheet
workbook = load_workbook(filename="reports/Visitor-Template.xlsx")
sheet = workbook.active
with open('visitors.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        rowcount=3
        colnum=0
        #These values are all required by EPA rules.
        #VTC[0]=="Car"
        #VTC[1]=="Car + Trailer"
        #VTC[2]=="Ute"
        #VTC[3]=="Ute + Trailer"
        #VTC[4]=="GVM (Truck)"
        #VTC[5]=="Van"
        VTC=["Car","Car + Trailer", "Ute", "Ute + Trailer", "GVM", "Van"]
        #This is just a list to keep count of the numbers of each type of visitor
        VTC_INT=[0,0,0,0,0,0]

        for row in csvReader:
                print(row)
                #I am well aware of how wasteful and slow this method is, and just how much better using a database would be.
                #However due to the formats that my employer wants this data, spreadsheets unfortunately are the way to go.
                if row[0]==d:
                        #Increment the vehicle type by one.
                        if row[3]=="Ute":
                            VTC_INT[2]+=1
                        else:
                            VTC_INT[int(row[3])]+=1
                        #Time
                        sheet[str(colums[colnum]+str(rowcount))] = row[2]
                        #Registration
                        sheet[str(colums[(colnum+1)]+str(rowcount))] = row[1]
                        #Vehicle Type
                        #I made an oopsie and this is a temporary workaround for November
                        print(row[3])
                        if row[3]=='Ute':
                            sheet[str(colums[(colnum+2)]+str(rowcount))] = "Ute"
                        else:
                            sheet[str(colums[(colnum+2)]+str(rowcount))] = VTC[int(row[3])]
                        #Waste Type
                        sheet[str(colums[(colnum+3)]+str(rowcount))] = row[4]
                        #Commercial or Domestic
                        sheet[str(colums[(colnum+4)]+str(rowcount))] = row[5]
                        rowcount+=1
                        if rowcount > 38:
                                rowcount=3
                                colnum+=5
#Writing down the vehicle type counter.                                
sheet['A40']=str(VTC_INT[0])
sheet['B40']=str(VTC_INT[1])
sheet['C40']=str(VTC_INT[2])
sheet['D40']=str(VTC_INT[3])
sheet['E40']=str(VTC_INT[4])
sheet['F40']=str(VTC_INT[5])
workbook.save(filename="reports/Visitor_Log-%s.xlsx" % d)

