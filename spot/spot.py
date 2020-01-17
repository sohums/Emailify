#!/usr/bin/env python3

import spotipy
from authenticate import credentials
from spotipyFunctions import parse_playlists_for_artists, get_all_artists_info, get_artists_with_new_albums
from csvHandler import write_to_CSV, read_from_CSV, del_extra_files, run_today
from helperFunctions import internet_available
from emailer import send_email
from input import username

if internet_available():
	spot = credentials() # the spotipy instance

	# reads in yesterdays data to compare and see if there are any differences in number of albums
	prev_artist_info = read_from_CSV()

	# checks if the program has run today
	if not run_today():
		try:
			# gets list of all artists from users public playlists
			all_artists = parse_playlists_for_artists(spot, username)

			# gets list with all artist information for today
			all_artist_info = get_all_artists_info(spot, all_artists)

			# deletes extra .csv files if there are more than three
			del_extra_files()

			# gets the list of artists with new albums
			artists_with_new_albums = get_artists_with_new_albums(spot, prev_artist_info, all_artist_info)

			# sends email if there is an artist with a new album
			if len(artists_with_new_albums) > 0:
				email_sent = send_email(artists_with_new_albums)
				if email_sent:
					write_to_CSV(all_artist_info)
			else:
				print("No new albums")

		except ConnectionResetError:
			print("Error establishing connection (Connection Reset Error)")
		except ConnectionError:
			print("Error establishing connection (Connection Error)")
		except OSError:
			print("OSError: [Errno 50] Network is down")
else:
	
	print("No internet connection at this time")