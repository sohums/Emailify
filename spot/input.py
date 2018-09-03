import os

username = 'SPOTIFY_USERNAME'
email_to = 'EMAIL_TO'

# I recommend setting up a temp email account to send the emails to you from
email_from = 'EMAIL_FROM'
email_from_pwd = os.environ['email_from_pwd']

client_id = os.environ['spotify_client_id']
client_secret = os.environ['spotify_client_secret']