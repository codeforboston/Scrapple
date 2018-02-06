# Legal Housing: Craiglist Scraper 

  This is a partner project of [Legal Housing](https://github.com/codeforboston/legalhousing). Check there for a more complete
  description of the project motivation and goals.

  This project implements:
  
  * A scraper that pulls Boston-area housing listings from Craigslist and stores
    them in a Postgres database.
    
  * A webserver that can dispatch the scraper on demand and return the listings
    in JSON format, with optional filtering.
    
# Setup

## Requirements

  - Python 3
  - Postgres
  
## Python dependencies
   
   (You should create a new Python virtual environment for use with this
   project, but that process is outside the scope of this document.)

  - [Flask](http://flask.pocoo.org) - a lightweight web framework
  - [psycopg2](http://initd.org/psycopg/) - a Postgres adapter
  - [Scrapy](https://scrapy.org) - a framework for webscraping
  
  You can install all of these dependencies by running 
  `pip install -r Scrapple/requirements.txt`, or by installing them 
  individually.

## Database initialization

  To perform initial setup on the database, you need to execute the commands in
  `Scrapple/Database/create_listings.sql`. You can use `psql`. For instance:
  
  `psql <conn_str> -f Scrapple/Database/create_listings.sql`

  Where `<conn_str>` is any way of specifying the location, database, and
  credentials to use: URI (`postgresql://...`), flags (`--user`, etc.), param
  lists (`"host=localhost user=..."`).
  
## Start

  In the `Scrapple` subdirectory, run:
  
  `FLASK_APP=./runserver.py FLASK_DEBUG=1 flask run`
  
  Omit `FLASK_DEBUG=1` to disable automatic code reloading.
  
# Alternative Setup: Docker

  If you have Docker and Docker Compose installed, cd to the `Scrapple`
  directory and run:
  
  `docker-compose up`

## Data API 

  To retrieve listings between a given date range

  http:// <host> :5555/listings/get?dfrom=<str_from>&dto=<str_dto>&pagesize=<pagesize>

  dfrom and dto describe the date range if dto is omitted it defaults to the current date

  Two date formats are supported YYY-MM-DD and MM/DD/YYYY

  pagesize gives the number of records to be returned starting with the oldest record if there are more records in the range  than pagesize then only the first pagesize number of records will be returned.
  If pagesize is omitted it defaults to systems configurable page_maximum which is the supplied config file sets to 500.
  If pagesize exceeds page_maximum it's reset to page_maximum.

  Example valid URIs:
    <p>http://localhost:5555/listings/get?dfrom=2017-01-01&dto=2018-01-01&pagesize=400</p>
    <p>http://localhost:5555/listings/get?dfrom=2017-01-01</p>

