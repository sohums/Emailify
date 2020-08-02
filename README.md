# Emailify

I got tired of missing out on new music. That's why I developed Emailify to notify me when there is new music released by my artists on Spotify.

The following program is an emailer which notifies you of any new music released by your Spotify artists. It works by parsing your public playlists and getting all your artists from there. Then daily it compares number of albums by all of the artists in those playlists. If it detects a change then the program automatically emails you with a link to the artists profile.

# Installation Instructions
1. Clone the repo
2. pip install -r requirements.txt
3. Login or create a new Spotify developer account and create an application (https://developer.spotify.com/dashboard/). You can call it whatever you want. Note down your application's client id and client secret.
4. Insert your spotify username and email addresses in input.py
5. Export environment variables for client id and client secret which can be found in the application you created on the Spotify developer portal in input.py

    `export SPOTIPY_CLIENT_ID='your-spotify-client-id'`

    `export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'`

    `export SPOTIPY_REDIRECT_URI='http://localhost/'`

6. Try and run the program you should be prompted to open a URL in your browser. Enter the URL and then paste the URL you are forwarded back into the terminal.
7. Type in email username in input.py to send emails from (I recommend creating a separate email account to send emails from). Then setup email password as an environment variable ('email\_from\_pwd')
8. Run the program whenever you want ($ python3 spot.py) or create a crontab to run the program daily. The commands to create the crontab in command line on a Mac are shown below. Replace MINUTE, HOUR, and YOURFILEPATH with their respective values. Note that HOUR is in military/24 hour time

`$ crontab -e`

    MINUTE HOUR * * * cd YOURFILEPATH/Emailify/spot && YOURPATHTOPYTHON3/python3 spot.py

9. If you are running the program via cron you may want to place your environment variables in the crontab file.