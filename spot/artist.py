
class Artist:
	
	def __init__(self, name, numAlbums, albums):
		self.name = name
		self.numAlbums = numAlbums
		self.albums = albums

	def __str__(self):
		
		retString = ""
		
		retString += "Name: " + self.name + "\n"
		retString += "Number of albums: " + str(self.numAlbums) + "\n"
		retString += "Albums: " + str(self.albums)

		return retString