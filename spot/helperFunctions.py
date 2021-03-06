import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from progress.bar import Bar  # sudo pip install progress
from emailer import send_email

# found at https://gist.github.com/89465127/5468929
def progress_bar():
    bar = Bar('Processing', max=20,
              suffix='%(index)d/%(max)d - %(percent).1f%% - %(eta)ds')
    for i in range(20):
        time.sleep(.05)  # Do some work
        bar.next()
    bar.finish()

# the incrementing part of the progress bar
def increment_progress_bar(bar):
    time.sleep(.05)  # Do some work
    sys.stdout.flush()
    bar.next()

def internet_available():
    try:
        urllib.request.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib.error.URLError as err:
        return False
