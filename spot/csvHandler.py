import csv 
from datetime import date, timedelta
import os
import os.path
import glob

# writes artist, album count, and albums to csv
def write_to_CSV(mydict):
	today = date.today()
	today_str = today.strftime('%y%m%d')

	# if file does not exist then create a new one
	if not os.path.isfile('../data/'+ today_str):
		with open('../data/'+ today_str + ".csv", 'wb') as csv_file:
			writer = csv.writer(csv_file)
			for key in sorted(mydict.iterkeys()):
				try:
					writer.writerow([key, mydict[key].split(",")[0], mydict[key][2::]])
				except AttributeError:
					writer.writerow([key, "-1", "N/A"])

# gets album count from csv
def read_from_CSV():
	today = date.today()
	today_str = today.strftime('%y%m%d')
	today_filename = today_str + ".csv"

	path, dirs, files = os.walk("../data/").next()
	file_count = len(files)
   	
	prev_data = {}

	all_csv_files = []

	# check for valid .csv file 
	for file in files:
		if ".csv" in file:
			valid_prev_data = True
			all_csv_files.append(file.split(".")[0])

	all_csv_files = sorted(all_csv_files, reverse=True)

	# check previous file closest to today
   	if valid_prev_data:
		prev_data = open_file("../data/" + all_csv_files[0] + ".csv")
   	else:
   		print("No data to read from")

   	return prev_data

# checks if program has run today
def run_today():
	today = date.today()
	today_str = today.strftime('%y%m%d')
	today_filename = today_str + ".csv"

	path, dirs, files = os.walk("../data/").next()

	if today_filename in files:
		print("The program has already run today")
		return True 
	else:
		return False

# opens the file and stores the data in a dictionary
def open_file(filename):
	data = {}

	file = open(filename)
	csv_file = csv.reader(file)

	for row in csv_file:
		try:
			data[row[0]] = row[1]
		except ValueError:
			data[row[0]] = -1

	return data