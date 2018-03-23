import csv 
from datetime import date, timedelta
import os
import os.path
import glob

def write_to_CSV(mydict):
	today = date.today()
	today_str = today.strftime('%m%d%y')

	# if file does not exist then create a new one
	if not os.path.isfile('../data/'+ today_str):
		with open('../data/'+ today_str + ".csv", 'wb') as csv_file:
		    writer = csv.writer(csv_file)
		    for key in sorted(mydict.iterkeys()):
		       writer.writerow([key, mydict[key]])

def read_from_CSV():
	today = date.today()
	today_str = today.strftime('%m%d%y')
	today_filename = today_str + ".csv"

	path, dirs, files = os.walk("../data/").next()
	file_count = len(files)
   	
	prev_data = {}

	# check for valid .csv file 
	valid_prev_data = False
	for file in files:
		if ".csv" in file:
			valid_prev_data = True

	# check if file already exists
   	if today_filename in files:
   		print("You have already run the program today") 

	# check previous file closest to today
   	elif valid_prev_data:
   		files_path = os.path.join('../data/', '*')
		most_recent_file = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True)[0]
		prev_data = open_file(most_recent_file)
		
   	else:
   		print("No data to read from")

   	return prev_data

# opens the file and stores the data in a dictionary
def open_file(filename):
	data = {}
	with open(filename, 'rb') as csv_file:
		reader = csv.reader(csv_file)
		data = dict(reader)
	for key in data:
		# takes in just the number of albums at the beginning of the value (ex.Artist Name, 2 ['album1', 'album2'] -> 2)
		data[key] = int(data[key][0]) 

	return data