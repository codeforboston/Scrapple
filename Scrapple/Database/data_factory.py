# DataFactory.py
import psycopg2
import json


class DataFactory:
    def __init__(self):
        self._df_config_path = "data_factory_config.json"
        self._df_config = self.get_data_factory_conf(self._df_config_path)
        print("Data Factory started")
        self.db_conn = self.postgres_connect(self._df_config["pg_config"])
        if self.db_conn:
            print("Connected to db: ")
            print(self.db_conn)

    def postgres_connect(self, conn_conf):
        print("Try to connect to postgres db")
        # Connect to an existing database
        # Define our connection string
        conn_string = "host=" + conn_conf["host"]
        conn_string += " dbname=" + conn_conf["dbname"]
        conn_string += " user=" + conn_conf["user"]
        conn_string += " password=" + conn_conf["pw"]
        #print("Connecting to database: " + conn_string)
        # get a connection
        try:
            db_conn = psycopg2.connect(conn_string)
        except psycopg2.Error as e:
            print(e)
            db_conn = None
        return db_conn

    def sql_execute(self, sql_string, fetch):
        # Open a cursor to perform database operations
        cur = self.db_conn.cursor()
        # Psycopg sql execute
        cur.execute(sql_string)
        if fetch:
            x = cur.fetchone()
        else:
            x = None
        # Make the changes to the database persistent
        self.db_conn.commit()
        # Close communication with the database
        cur.close()
        self.db_conn.close()
        return x

    def listings_setter(self, row_data):
        sql_string = "INSERT INTO listings (date_posted ,listing_title, price, "
        sql_string += "latitude, longitude , address , desciption, "
        sql_string += "link , listing_id) "
        sql_string += "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'"
        sql_string += ")"
        sql_string = sql_string.format(row_data["date_posted"],
                                       row_data["listing_title"],
                                       row_data["price"],
                                       row_data["latitude"],
                                       row_data["longitude"],
                                       row_data["address"],
                                       row_data["desciption"],
                                       row_data["link"],
                                       row_data["listing_id"])
        # print("Sql INSERT: " + sql_string)
        data = self.sql_execute(sql_string, False)

    def listings_getter(self, rid):
        sql_string = "SELECT * FROM listings WHERE id = {};".format(rid)
        data = self.sql_execute(sql_string, True)
        return data

    def get_data_factory_conf(self, file_name):
        with open(file_name) as data_file:
            dict_from_json = json.load(data_file)
        return dict_from_json

dataFactory = DataFactory()


data = {"date_posted": '01/23/2017 14:54',
        "listing_title": "some title",
        "price": "6.66",
        "money": "some title",
        "latitude": "78.87",
        "longitude": "7.87",
        "address": "some address",
        "desciption": "some desciption",
        "link": "some url",
        "listing_id": "some listing_id"}

#dataFactory.listings_setter(data)
print(dataFactory.listings_getter(4))
