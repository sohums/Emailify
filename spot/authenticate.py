import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from input import client_id, client_secret

def credentials():
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    spotify_instance = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    return spotify_instance