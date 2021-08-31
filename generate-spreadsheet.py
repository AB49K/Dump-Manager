#!/bin/python
from openpyxl import load_workbook
from datetime import datetime
import csv
now = datetime.now() # current date and time
d = now.strftime("%d-%m-%Y")
colums="ABCDEFGHIJLMNOPQRSTUVWXYZ"
colums=list(colums)
# Start by opening the spreadsheet and selecting the main sheet
workbook = load_workbook(filename="reports/Visitor-Template.xlsx")
sheet = workbook.active
with open('visitors.csv') as csvDataFile:
	csvReader = csv.reader(csvDataFile)
	rowcount=3
	colnum=0
	for row in csvReader:
		print(row)
		if row[0]==d:
			sheet[str(colums[colnum]+str(rowcount))] = row[2]
			sheet[str(colums[(colnum+1)]+str(rowcount))] = row[1]
			sheet[str(colums[(colnum+2)]+str(rowcount))] = row[3]
			sheet[str(colums[(colnum+3)]+str(rowcount))] = row[4]
			sheet[str(colums[(colnum+4)]+str(rowcount))] = row[5]
			rowcount+=1
			if rowcount > 38:
				rowcount=3
				colnum+=5
# Write what you want into a specific cell

# Save the spreadsheet
workbook.save(filename="reports/Visitor_Log-%s.xlsx" % d)



# workbook = load_workbook(filename="reports/Report-Template.xlsx")
# sheet = workbook.active
# with open('visitors.csv') as csvDataFile:
	# csvReader = csv.reader(csvDataFile)
	# rowcount=3
	# colnum=0
	# for row in csvReader:
		# print(row)
		# if row[0]==d:
			# sheet[str(colums[colnum]+str(rowcount))] = row[2]
			# sheet[str(colums[(colnum+1)]+str(rowcount))] = row[1]
			# sheet[str(colums[(colnum+2)]+str(rowcount))] = row[3]
			# sheet[str(colums[(colnum+3)]+str(rowcount))] = row[4]
			# sheet[str(colums[(colnum+4)]+str(rowcount))] = row[5]
			# rowcount+=1
			# if rowcount > 38:
				# rowcount=3
				# colnum+=5
# # Write what you want into a specific cell

# # Save the spreadsheet
# workbook.save(filename="reports/Visitor_Log-%s.xlsx" % d)
