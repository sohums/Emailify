import smtplib

def send_email(artist, artistLink):

    # Credentials for email account that sends emails to you
    gmail_email = 'GMAIL EMAIL'
    gmail_pwd = 'GMAIL PASSWORD'

    # The email account where you want to receive new music notifications
    recipient = 'YOUR EMAIL HERE'    
    
    FROM = gmail_email
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = artist + " has released a new album!"
    TEXT = "A new album from " + artist + " just released! Check it out at: " + artistLink

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_email, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print("Successfully sent email")
    except:
        print("Failed to send email")
