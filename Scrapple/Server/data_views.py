"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import abort, render_template, request, Response
from Server import app
from Scrapple import scrapple
from Database import dataFactory
import json


@app.route('/listings', methods=["GET"])
def listings_handler():
    rid = request.args.get('rid', None)
    dfrom = request.args.get('dfrom', None)
    dto = request.args.get('dto', None)

    if not rid and not (dfrom or dto):
        abort(Response(
            "You must provide an rid or a start (dfrom) and end date (dto) "
            "in the form YYYY-mm-dd.",
            status=401))

    pagesize = request.args.get('pagesize', None)
    if pagesize:
        pagesize = int(pagesize)
    output = dataFactory.listings_getter(rid, dfrom, dto, pagesize)
    emit_sjson = json.dumps(output)
    return emit_sjson

@app.route('/start_scraper', methods=["POST"])
def start_scraper():
    scraper_name = request.args.get('scraper')

    if scraper_name:
        scrapple.start_scraper(scraper_name)
        scrapple.run_spiders()
        print("starting scraper " + scraper_name)
        return "success"
    else:
        abort(Response("Missing parameter: scraper", status=401))
