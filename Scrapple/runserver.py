"""
This script runs the Scrapple application using a development server.
"""

from os import environ
from Server import app
from Scrapple import scrapple

if __name__ == '__main__':
    #tesing code please remove
    scrapple.intialize()
    #scrapple.start_scraper("craigslist")
    #scrapple.run_spiders()

    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    print("Server starting")
    app.run(HOST, PORT)