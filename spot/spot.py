import spotipy
from authenticate import login
from spotipyFunctions import parse_playlists_for_artists, get_artists_album_count, get_artists_with_new_albums, notify_new_album
from csvHandler import write_to_CSV, read_from_CSV
	
login_information = login()
username = login_information[0]
spot = login_information[1] # the spotipy instance

# reads in yesterdays data to compare and see if there are any differences in number of albums
prev_album_count = read_from_CSV()

# gets list of all artists from users public playlists
all_artists = parse_playlists_for_artists(spot, username)

# gets dictionary with the total number of albums for each artist
album_count = get_artists_album_count(spot, all_artists)

# writes todays data to csv file
write_to_CSV(album_count)

# gets the list of artists with new albums
artists_with_new_albums = get_artists_with_new_albums(prev_album_count, album_count)

# sends email if there is an artist with a new album
notify_new_album(spot, artists_with_new_albums)