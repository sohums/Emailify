#!/usr/bin/env python3

import spotipy
from authenticate import login
from spotipyFunctions import parse_playlists_for_artists, get_all_artists_info, get_artists_with_new_albums, notify_new_album
from csvHandler import write_to_CSV, read_from_CSV, del_prev_files, run_today
from helperFunctions import internet_available

if internet_available():	

	login_information = login()
	username = login_information[0]
	spot = login_information[1] # the spotipy instance

	# reads in yesterdays data to compare and see if there are any differences in number of albums
	prev_artist_info = read_from_CSV()

	# checks if the program has run today
	if not run_today():

		# gets list of all artists from users public playlists
		all_artists = parse_playlists_for_artists(spot, username)

		# gets list with all artist information for today
		all_artist_info = get_all_artists_info(spot, all_artists)

		# writes todays data to csv file
		write_to_CSV(all_artist_info)
		
		# deletes extra .csv files if there are more than three
		del_prev_files()

		# gets the list of artists with new albums
		artists_with_new_albums = get_artists_with_new_albums(prev_artist_info, all_artist_info)

		# sends email if there is an artist with a new album
		notify_new_album(spot, artists_with_new_albums)

else:
	print("No internet connection at this time")