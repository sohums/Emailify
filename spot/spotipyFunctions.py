from helperFunctions import increment_progress_bar
from progress.bar import Bar
from emailer import send_email

# adds all artists from playlist to a set
def add_artists(spotipy_instance, tracks, set_artists):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        set_artists.add((track['artists'][0]['name']).encode('utf-8'))

# iterates through users public playlists and adds all unique artists to list, returns a list of unique artists
def parse_playlists_for_artists(spotipy_instance, username):
    playlists = spotipy_instance.user_playlists(username)
    artists = set()
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            # print 'number of songs:', playlist['tracks']['total']
            results = spotipy_instance.user_playlist(username, playlist['id'],fields="tracks,next")
            tracks = results['tracks']
            add_artists(spotipy_instance, tracks, artists)
            while tracks['next']:
                tracks = spotipy_instance.next(tracks)
                add_artists(spotipy_instance, tracks, artists)
    
    return list(artists)

# given artist name returns all info related to artist 
def get_artist_info(spotipy_instance, name):
    results = spotipy_instance.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

# returns list of all albums given artist name 
def get_artist_albums(spotipy_instance, artist):
    albums = []
    results = spotipy_instance.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = spotipy_instance.next(results)
        albums.extend(results['items'])
    seen = set() # to avoid dups
    # albums.sort(key=lambda album:album['name'].lower())
    for album in albums:
        name = album['name']
        # print(album['name'] + ": " + album['id'])
        if name not in seen:
            seen.add(name.encode('utf-8'))
    return list(seen)

# given a list of artists returns a dict with key being artist and value the number of albums they have
def get_artists_album_count(spotipy_instance, list_of_all_artists):
    album_count = {}
    print("Getting number of albums for all artists")
    bar = Bar('Loading...', max=len(list_of_all_artists), suffix='%(index)d/%(max)d - %(percent).1f%% - %(eta)ds')
    for artist_name in list_of_all_artists:
        increment_progress_bar(bar)
        # print(artist_name)
        artist_info = get_artist_info(spotipy_instance, artist_name)
        if artist_info is not None:  
            albums = get_artist_albums(spotipy_instance, artist_info)
            # print(albums)
            album_count[artist_name] = str(len(albums)) + " " + str(albums)
        else:
            print("Can't find that artist!")
            album_count[artist_name] = -1
        # print(" ")
    bar.finish()
    print("Done!\n")

    return album_count

# given artist name returns their spotify id
def get_artist_id(spotipy_instance, artist_name):
    return get_artist_info(spotipy_instance, artist_name)['external_urls']['spotify']

# given two dictionaries with artists and their album count returns artists with new albums
def get_artists_with_new_albums(prev_album_count, album_count):
    artists_with_new_albums = []
    
    for item in album_count.items():
        artist = item[0]       
        if artist in album_count and artist in prev_album_count:
            if str(album_count[artist])[0] > str(prev_album_count[artist])[0]:
                artists_with_new_albums.append(artist)

    return artists_with_new_albums

# given a list of artists sends emails w/ links to artists profile
def notify_new_album(spotipy_instance, list_of_artists):
    if len(list_of_artists) > 0:
        for artist in list_of_artists:
            artist_id = get_artist_id(spotipy_instance, artist)
            send_email(artist, artist_id)
        print("New music is available")
    else:
        print("No new albums")
