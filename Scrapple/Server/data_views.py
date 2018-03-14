"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import abort, render_template, request, Response
from Server import app
from Scrapple import scrapple
from Database import dataFactory
import json


@app.route('/listings/get', methods=["GET"])
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


@app.route('/start_spider_sch', methods=["POST"])
def start_spider_sch():
    status_msg = "no msg"
    scraper_name = request.args.get('scraper')
    if scraper_name:
        print("start_spider_sch>Try to start scrapy schedule for " + scraper_name)
        status_msg = scrapple.start_spider_sch(scraper_name)
        return status_msg
    else:
        abort(Response("Missing parameter: scraper", status=401))


@app.route('/stop_spider_sch', methods=["POST"])
def stop_spider_sch():
    status_msg = "no msg"
    scraper_name = request.args.get('scraper')
    if scraper_name:
        print("stop_spider_sch> Try to stop scraper " + scraper_name)
        status_msg = scrapple.stop_spider_sch(scraper_name)
        return status_msg
    else:
        abort(Response("Missing parameter: scraper", status=401))
