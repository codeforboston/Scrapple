-- create_listings.sql

CREATE TABLE IF NOT EXISTS public.listings
(
	id serial NOT NULL,
    date_posted TIMESTAMP NOT NULL,
    date_created TIMESTAMP NOT NULL DEFAULT now(),
    listing_title VARCHAR (255) COLLATE pg_catalog."default",
    price MONEY,
    beds INTEGER,
    size INTEGER,
    baths INTEGER,
    latitude REAL,
    longitude REAL,
    desciption TEXT COLLATE pg_catalog."default",
    link VARCHAR (255) COLLATE pg_catalog."default",
    listing_id VARCHAR (30) COLLATE pg_catalog."default",
    CONSTRAINT listings_pkey PRIMARY KEY (id)
);
