"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import request
from Server import app
from Scrapple import scrapple

@app.route('/data')
@app.route('/start_scraper', methods=["POST"])
def start_scraper():
    strScraperName = request.args.get('scraper')
    scrapple.start_scraper(strScraperName)
    scrapple.run_spiders()
    print("starting scraper " + strScraperName)
    return "success"