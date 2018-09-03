import smtplib
from input import email_to, email_from, email_from_pwd

def send_email(newMusicArtist):

	FROM = email_from
	TO = email_to if type(email_to) is list else [email_to]
	SUBJECT = newMusicArtist.name + " has released a new album!"
	TEXT = str("A new album from " + newMusicArtist.name + " just released! The album name is "
	+ newMusicArtist.newAlbum + ". \n Check it out at: " + newMusicArtist.artistId 
	+ ". \n Album artwork: " + newMusicArtist.newAlbumArt)

	# Prepare actual message
	message = """From: %s\nTo: %s\nSubject: %s\n\n%s
	""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
	try:
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.ehlo()
		server.starttls()
		server.login(email_from, email_from_pwd)
		server.sendmail(FROM, TO, message)
		server.close()
		print("Successfully sent email")
	except:
		print("Failed to send email")
