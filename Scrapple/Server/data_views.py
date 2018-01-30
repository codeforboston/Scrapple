"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import request
from Server import app
from Scrapple import scrapple
from Database import dataFactory
import json


@app.route('/listings', methods=["POST"])
def listings_handler():
    rid = request.args.get('rid', None)
    dfrom = request.args.get('dfrom', None)
    dto = request.args.get('dto', None)
    pagesize = request.args.get('pagesize', None)
    if pagesize:
        pagesize = int(pagesize)
    output = dataFactory.listings_getter(rid, dfrom, dto, pagesize)
    emit_sjson = json.dumps(output)
    return emit_sjson


@app.route('/start_scraper', methods=["POST"])
def start_scraper():
    strScraperName = request.args.get('scraper')
    scrapple.start_scraper(strScraperName)
    scrapple.run_spiders()
    print("starting scraper " + strScraperName)
    return "success"
