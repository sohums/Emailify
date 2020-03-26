import smtplib
from input import email_to, email_from, email_from_pwd


def send_email(list_of_artists):
    FROM = email_from
    TO = email_to if type(email_to) is list else [email_to]
    TEXT = ''
    if len(list_of_artists) == 1:
        newMusicArtist = list_of_artists[0]
        SUBJECT =  '{} has released a new album!'.format(newMusicArtist.name)
        TEXT += 'A new album from {} just released! The album name is {}.\n'.format(newMusicArtist.name, newMusicArtist.newAlbum)
        TEXT += 'Check it out at: {}\n'.format(newMusicArtist.artistId)
        TEXT += 'Album artwork: {}'.format(newMusicArtist.newAlbumArt)
    else:
        SUBJECT = 'New music from your artists on Spotify!'
        for newMusicArtist in list_of_artists:
            TEXT += 'A new album from {} just released! The album name is {}.\n'.format(newMusicArtist.name, newMusicArtist.newAlbum)
            TEXT += 'Check it out at: {}\n'.format(newMusicArtist.artistId)
            TEXT += 'Album artwork: {}\n\n'.format(newMusicArtist.newAlbumArt)

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
	""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(email_from, email_from_pwd)
        server.sendmail(FROM, TO, message.encode('utf8'))
        server.close()
        print('Successfully sent email')
        return True
    except Exception as e:
        print(str(e))
        print('Failed to send email')
        print(TEXT)
        return False
