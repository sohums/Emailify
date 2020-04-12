import spotipy

from input import username

def credentials():
    scope = 'user-library-read' # add extra scopes w/ spaces
    token = spotipy.util.prompt_for_user_token(username, scope)

    return spotipy.Spotify(auth=token)
