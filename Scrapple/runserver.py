"""
This script runs the Scrapple application using a development server.
"""

from os import environ
from Server import app

@app.before_first_request
def _run_on_start():
    print("The app started")

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    print("Server starting")
    app.run(HOST, PORT)