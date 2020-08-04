#!/usr/bin/env python3

import logging
import spotipy

from authenticate import credentials
from csvHandler import data_not_present, del_extra_files, read_from_CSV, run_today, write_to_CSV
from emailer import send_email
from helperFunctions import internet_available
from spotipyFunctions import get_all_artists_info, get_all_artists_names, get_artists_with_new_albums

logging.basicConfig(filename='info.log', level=logging.INFO, format='%(asctime)s %(message)s')

if internet_available():
    spot = credentials()  # the spotipy instance

    # reads in yesterdays data to compare and see if there are any differences in number of albums
    prev_artist_info = read_from_CSV()

    if not run_today():
        logging.info('Running')
        try:
            # gets list of all artists from users public playlists
            all_artists = get_all_artists_names(spot)

            # gets list with all artist information for today
            curr_artist_info = get_all_artists_info(spot, all_artists)

            # gets the list of artists with new albums
            artists_with_new_albums = get_artists_with_new_albums(spot, prev_artist_info, curr_artist_info)

            if data_not_present():
                logging.info('Ran program for the first time')
                write_to_CSV(prev_artist_info, curr_artist_info)
            elif len(artists_with_new_albums) >= 1:
                email_sent = send_email(artists_with_new_albums)
                if email_sent:
                    write_to_CSV(prev_artist_info, curr_artist_info)
            else:
                print('No new albums')

            # deletes extra .csv files if there are more than three
            del_extra_files()

        except ConnectionResetError:
            print('Error establishing connection (Connection Reset Error)')
        except ConnectionError:
            print('Error establishing connection (Connection Error)')
        except OSError:
            print('OSError: [Errno 50] Network is down')
else:
    print('No internet connection at this time')

logging.info('---------------')
