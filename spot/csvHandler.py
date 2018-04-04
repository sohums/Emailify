import csv 
from datetime import date, timedelta
import os
import os.path
import glob
from artist import Artist

# writes artist, album count, and albums to csv
def write_to_CSV(all_info):
	today = date.today()
	today_str = today.strftime('%y%m%d')

	# if file does not exist then create a new one
	if not os.path.isfile('../data/'+ today_str):
		with open('../data/'+ today_str + ".csv", 'wb') as csv_file:
			writer = csv.writer(csv_file)
			for artist in all_info:
				writer.writerow([artist.name, artist.numAlbums, artist.albums])

# gets album count from csv
def read_from_CSV():
	today = date.today()
	today_str = today.strftime('%y%m%d')
	today_filename = today_str + ".csv"

	path, dirs, files = os.walk("../data/").next()
	file_count = len(files)

	prev_artist_info = []

	all_csv_files = []

	valid_prev_data = False

	# check for valid .csv file 
	for file in files:
		if ".csv" in file:
			valid_prev_data = True
			all_csv_files.append(file.split(".")[0])

	all_csv_files = sorted(all_csv_files, reverse=True)

	# check previous file closest to today
	if valid_prev_data:
		with open("../data/" + all_csv_files[0] + ".csv") as csv_file:
			reader = csv.reader(csv_file)
			for row in reader:
				artist = Artist(row[0], row[1], row[2])
				prev_artist_info.append(artist)
   	else:
   		print("No data to read from")

   	return prev_artist_info

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
