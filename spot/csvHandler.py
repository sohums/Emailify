import csv 
from datetime import date, timedelta
import os
import os.path
import glob
import ast

from artist import Artist

# writes artist, album count, and albums to csv
def write_to_CSV(all_info):
	today = date.today()
	today_str = today.strftime('%y%m%d')

	# if file does not exist then create a new one
	if not os.path.isfile('../data/'+ today_str):
		with open('../data/'+ today_str + ".csv", 'w') as csv_file:
			writer = csv.writer(csv_file)
			for artist in all_info:
				writer.writerow([artist.name, artist.numAlbums, artist.albums])

# gets album count from csv
def read_from_CSV():
	today = date.today()
	today_str = today.strftime('%y%m%d')
	today_filename = today_str + ".csv"

	path, dirs, files = next(os.walk("../data/"))
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
				artist = Artist(row[0], row[1], ast.literal_eval(row[2]))  # ast converts string list to type list
				prev_artist_info.append(artist)
	else:
		print("No data to read from")

	return prev_artist_info

# deletes extra .csv files if there are more than three
def del_prev_files():
	path, dirs, files = next(os.walk("../data/"))
	all_csv_files = []

	for file in files:
		if ".csv" in file:
			valid_prev_data = True
			all_csv_files.append(file.split(".")[0])

	all_csv_files = sorted(all_csv_files, reverse=True)
	file_count = len(all_csv_files)
	
	# while more than three files delete last file
	while file_count > 3:
		os.remove("../data/" + all_csv_files[-1] + ".csv")
		del all_csv_files[-1]
		file_count -= 1

# checks if program has run today
def run_today():
	today = date.today()
	today_str = today.strftime('%y%m%d')
	today_filename = today_str + ".csv"

	path, dirs, files = next(os.walk("../data/"))

	if today_filename in files:
		print("The program has already run today")
		return True 
	else:
		return False
