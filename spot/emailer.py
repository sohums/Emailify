import smtplib
from input import email_to, email_from, email_from_pwd


def send_email(list_of_artists):
    FROM = email_from
    TO = email_to if type(email_to) is list else [email_to]

    if len(list_of_artists) == 1:
        newMusicArtist = list_of_artists[0]
        SUBJECT = newMusicArtist.name + " has released a new album!"
        TEXT = str("A new album from " + newMusicArtist.name + " just released! The album name is "
                + newMusicArtist.newAlbum + ". \nCheck it out at: " + newMusicArtist.artistId
                + ". \nAlbum artwork: " + newMusicArtist.newAlbumArt)
    else:
        SUBJECT = 'New music from your artists on Spotify!'
        TEXT = ''
        for newMusicArtist in list_of_artists:
            TEXT += str("A new album from " + newMusicArtist.name + " just released! The album name is "
                    + newMusicArtist.newAlbum + ". \nCheck it out at: " + newMusicArtist.artistId
                    + ". \nAlbum artwork: " + newMusicArtist.newAlbumArt + "\n\n")

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
        return True
    except Exception as e:
        print(str(e))
        print("Failed to send email")
        print(TEXT)
        return False
