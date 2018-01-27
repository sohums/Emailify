import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def login():
	
	retList = []

	username = 'ENTER SPOTIFY USERNAME HERE'
	clientId = ' ENTER CLIENT ID HERE'
	clientSecret = 'ENTER CLIENT SECRET HERE' 

	client_credentials_manager = SpotifyClientCredentials(client_id=clientId, client_secret=clientSecret)
	spotifyInstance = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	retList.append(username)
	retList.append(spotifyInstance)

	return retList