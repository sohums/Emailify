import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def login():
	
	ret_list = []

	username = 'ENTER SPOTIFY USERNAME HERE'
	client_id = ' ENTER CLIENT ID HERE'
	client_secret = 'ENTER CLIENT SECRET HERE'  

	client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
	spotify_instance = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	ret_list.append(username)
	ret_list.append(spotify_instance)

	return ret_list