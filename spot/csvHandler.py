import ast
import csv
import glob
import os
import os.path

from artist import Artist
from datetime import date, timedelta

# writes artist, album count, and albums to csv
def write_to_CSV(prev_info, curr_info):
    today = date.today()
    today_str = today.strftime('%y%m%d')

    all_info = merge_info(prev_info, curr_info)

    # if file does not exist then create a new one
    if not os.path.isfile('../data/' + today_str):
        with open('../data/' + today_str + ".csv", 'w') as csv_file:
            writer = csv.writer(csv_file)
            for artist in all_info:
                writer.writerow([artist.name, artist.numAlbums, artist.albums])

# gets album count from csv
def read_from_CSV():
    today = date.today()
    today_str = today.strftime('%y%m%d')
    today_filename = today_str + '.csv'

    path, dirs, files = next(os.walk('../data/'))
    prev_artist_info = []
    all_csv_files = []
    valid_prev_data = False

    # check for valid .csv file
    for file in files:
        if '.csv' in file:
            valid_prev_data = True
            all_csv_files.append(file.split('.')[0])

    all_csv_files = sorted(all_csv_files, reverse=True)

    # check previous file closest to today
    if valid_prev_data:
        with open('../data/' + all_csv_files[0] + '.csv') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                # ast converts string list to type list
                artist = Artist(row[0], row[1], ast.literal_eval(row[2]))
                prev_artist_info.append(artist)
    else:
        print('No data to read from')

    return prev_artist_info

# deletes extra .csv files if there are more than three
def del_extra_files():
    path, dirs, files = next(os.walk('../data/'))
    all_csv_files = []

    for file in files:
        if '.csv' in file:
            valid_prev_data = True
            all_csv_files.append(file.split('.')[0])

    all_csv_files = sorted(all_csv_files, reverse=True)
    file_count = len(all_csv_files)

    # while more than three files delete last file
    while file_count > 3:
        os.remove('../data/' + all_csv_files[-1] + '.csv')
        del all_csv_files[-1]
        file_count -= 1

# checks if program has run today
def run_today():
    today = date.today()
    today_str = today.strftime('%y%m%d')
    today_filename = today_str + '.csv'

    path, dirs, files = next(os.walk('../data/'))

    if today_filename in files:
        print('The program has already run today')
        return True
    else:
        return False

def data_not_present():
    path, dirs, files = next(os.walk('../data/'))
    csv_file_count = 0

    for file in files:
        if '.csv' in file:
            csv_file_count += 1
    return True if csv_file_count < 1 else False

def merge_info(prev_info, curr_info):
    prev_info = convert_to_dict(prev_info)
    curr_info = convert_to_dict(curr_info)

    all_info = []
    for artist, info in curr_info.items():
        if artist in prev_info:
            albums = list(set(prev_info[artist]['albums'] + info['albums']))
            all_info.append(Artist(artist, len(albums), albums))
        else:
            all_info.append(Artist(artist, info['numAlbums'], info['albums']))
    return all_info

def convert_to_dict(info):
    return {artist.name: {'numAlbums':artist.numAlbums, 'albums':artist.albums} for artist in info}