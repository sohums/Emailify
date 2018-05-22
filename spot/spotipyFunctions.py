from helperFunctions import increment_progress_bar
from progress.bar import Bar
from emailer import send_email
from artist import Artist, newMusicArtist

# adds all artists from playlist to a set
def add_artists(spotipy_instance, tracks, set_artists):
	for i, item in enumerate(tracks['items']):
		track = item['track']
		set_artists.add((track['artists'][0]['name']))

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
	for album in albums:
		name = album['name']
		# print(album['name'] + ": " + album['id'])
		if name not in seen:
			# seen.add(name.encode('utf-8'))
			seen.add(name)
	return list(sorted(seen))

def get_all_artists_info(spotipy_instance, list_of_all_artists):
	all_artist_info = []
	print("Getting number of albums for all artists")
	bar = Bar('Loading...', max=len(list_of_all_artists), suffix='%(index)d/%(max)d - %(percent).1f%% - %(eta)ds')
	for artist_name in list_of_all_artists:
		increment_progress_bar(bar)
		# print(artist_name)
		artist_info = get_artist_info(spotipy_instance, artist_name)
		if artist_info is not None:  
			albums = get_artist_albums(spotipy_instance, artist_info)
			# print(albums)
			artist = Artist(artist_name, len(albums), albums)
			all_artist_info.append(artist)
		else:
			print("\nCan't find " + str(artist_name))
			artist = Artist(artist_name, -1, [])
			all_artist_info.append(artist)
		# print(" ")
	bar.finish()
	print("Done!\n")

	all_artist_info.sort(key=lambda artist: artist.name)

	return all_artist_info

# given artist name returns their spotify id
def get_artist_id(spotipy_instance, artist_name):
	return get_artist_info(spotipy_instance, artist_name)['external_urls']['spotify']

# given two dictionaries with artists and their album count returns artists with new albums
def get_artists_with_new_albums(spotipy_instance, prev_artist_info, artist_info):
	artists_with_new_albums = []
	
	prev_album_count = get_album_count(prev_artist_info)
	album_count = get_album_count(artist_info)

	for artist in artist_info:
		if artist.name in album_count and artist.name in prev_album_count:
			if str(album_count[artist.name])[0] > str(prev_album_count[artist.name])[0]:

				# get diff between two lists
				for prev_artist in prev_artist_info:
					if prev_artist.name == artist.name:
						new_album = get_new_album_name(prev_artist.albums, artist.albums)

				artist_id = get_artist_id(spotipy_instance, artist.name)
				new_album_art = get_album_art(spotipy_instance, new_album)

				artist_with_new_music = newMusicArtist(artist.name, artist_id, new_album, new_album_art)
				artists_with_new_albums.append(artist_with_new_music)

	return artists_with_new_albums

# given two lists of album names gets the difference (the new album)
def get_new_album_name(prev_artist_albums, artist_albums):
	
	return list(set(artist_albums)-set(prev_artist_albums))[0]
 
# given a list of artist objects returns a dictionary with their album count
def get_album_count(artist_info):
	album_count = {}
	
	for artist in artist_info:
		album_count[artist.name] = artist.numAlbums

	return album_count

# given a list of artists sends emails w/ links to artists profile
def notify_new_album(spotipy_instance, list_of_artists):
	if len(list_of_artists) > 0:
		for newMusicArtist in list_of_artists:
			send_email(newMusicArtist)
			print("New music is available from " + newMusicArtist.name)
	else:
		print("No new albums")

def get_album_art(spotipy_instance, album_name):
	results = spotipy_instance.search(q='album:' + album_name, type='album')
	image_url = results['albums']['items'][0]['images'][0]['url'] # change second num to get different pic size (640x640, 300x300, or 64x64)
	
	return image_url