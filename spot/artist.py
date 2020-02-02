class Artist:
    def __init__(self, name, numAlbums, albums):
        self.name = name
        self.numAlbums = numAlbums
        self.albums = albums

    def __str__(self):
        retString = "Name: " + self.name + "\n"
        retString += "Number of albums: " + str(self.numAlbums) + "\n"
        retString += "Albums: " + str(self.albums)
        return retString

class newMusicArtist:
    def __init__(self, name, artistId, newAlbum, newAlbumArt):
        self.name = name
        self.artistId = artistId
        self.newAlbum = newAlbum
        self.newAlbumArt = newAlbumArt

    def __str__(self):
        retString = "Name: " + self.name + "\n"
        retString += "New album: " + str(self.newAlbum) + "\n"
        retString += "New album art url: " + str(self.newAlbumArt)
        return retString