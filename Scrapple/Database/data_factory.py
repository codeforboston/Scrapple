# DataFactory.py
import json
import os
from datetime import datetime
import psycopg2


# TODO support verbosity levels 1,2,3 suppress all print statements for 3

class DataFactory:
    def __init__(self):
        self._df_app_path = "Database/"
        #self._df_app_path = ""
        self._sql_create_path = self._df_app_path + "create_listings.sql"
        self._df_config_path = self._df_app_path + "data_factory_config.json"
        self._df_config = self.get_data_factory_conf(self._df_config_path)
        self.item_names = ("date", "title", "link", "price",
                                   "beds", "size", "craigId", "baths", "latitude",
                                   "longitude", "content")
        self.db_names = ("date_posted", "listing_title", "link", "price", 
                                 "beds", "size", "listing_id", "baths", "latitude",
                                 "longitude", "desciption")
        print("Data Factory started")
        self.db_conn = self.postgres_connect(self._df_config["pg_config"])
        if self.db_conn:
            print("Connected to db: ")
            print(self.db_conn)
            self.db_conn.close()

    def postgres_connect(self, conn_defaults):
        #print("Try to connect to postgres db")
        # Connect to the postgres database
        # Define our connection string
        conn_string = os.environ.get("POSTGRES_URI")

        if not conn_string:
            conn_defaults.setdefault("password", conn_defaults.get("pw"))
            conn_string = " ".join(
                k + "=" + conn_defaults[k]
                for k in ("host", "port", "dbname", "user", "password")
            )
        #print("Connecting to database: " + conn_string)
        # Get a connection
        try:
            db_conn = psycopg2.connect(conn_string)
        except psycopg2.Error as e:
            print(e)
            db_conn = None
        return db_conn

    def format_a_row(self, row, colnames):
        drow = dict(zip(colnames, row))
        drow["date_posted"] = drow["date_posted"].__str__()
        drow["date_created"] = drow["date_created"].__str__()
        return drow

    def format_row_data(self, rows, colnames):
        return (self.format_a_row(row, colnames) for row in rows)

    def sql_execute(self, sql_string, sql_data, fetch, fetchall=None):        
        # Open a connection
        self.db_conn = self.postgres_connect(self._df_config["pg_config"])
        # Open a cursor to perform database operations
        cur = self.db_conn.cursor()
        # Psycopg sql execute
        cur.execute(sql_string, sql_data)
        colnames = [desc[0] for desc in cur.description]        
        if fetch:
            if fetchall:
                rows = cur.fetchall()
                emit = self.format_row_data(rows, colnames)
            else:
                row = cur.fetchone()
                emit = self.format_a_row(row, colnames)
        else:
            emit = None
            # Make the changes to the database persistent
            self.db_conn.commit()
        # Close communication with the database
        cur.close()
        self.db_conn.close()
        return emit

    def listings_setter(self, row_item):        
        # Set up SQL insert string
        # Built from two sets expected item attributes and expected database fields
        sql_data = []
        for k in self.item_names:
            sql_data.append( row_item.get(k, None) )
        sql_str = "INSERT INTO listings (" + ", ".join( self.db_names ) + ") "
        sql_str += "VALUES (" + ", ".join ( ["%s"]*len(self.db_names) ) + ") " 
        # print("Sql INSERT: " + sql_str)
        # print("sql_data", sql_data,"\n")
        data = self.sql_execute(sql_str, sql_data, False)

    # validation helper methods
    def valid_pagesize(self, pagesize, pmax):
        if pagesize:
            if not (pagesize > 0 and pagesize <= pmax):
                pagesize = pmax
        else:
            pagesize = pmax
        return pagesize

    def dt_str_2_dt(self, sdate):
        # Convert string date inputs to datetime formats
        # Set to none if not convertible
        # Supports only two formats '%Y-%m-%d' postgras native and
        # '%m/%d/%Y' US local
        emsg = None
        try:
            dt = datetime.strptime(sdate, '%Y-%m-%d')
        except ValueError:
            try:
                dt = datetime.strptime(sdate, '%m/%d/%Y')
            except ValueError:
                emit = emsg
            else:
                emit = dt
        else:
            emit = dt
        return emit

    def valid_dfrom(self, dfrom):
        emit = None
        dtfrom = self.dt_str_2_dt(dfrom)
        if not dtfrom is None:
            if datetime.now() >= dtfrom:
                emit = dtfrom
        return emit

    def valid_dto(self, dto, dtfrom):
        emit = None
        dtto = self.dt_str_2_dt(dto)
        if not dtto is None:
            if dtto >= dtfrom:
                emit = dtto
        return emit

    def valid_parm_rang(self, dfrom, dto, pagesize, pmax):
        # Check the parameters are invalid ranges
        # And reset values that are blank to defaults
        valid = False
        emit_dfrom, emit_dto = (None, None)
        if dfrom:
            dtfrom = self.valid_dfrom(dfrom)
            if not dtfrom is None:  # if good
                if dto is None:
                    dto = datetime.now().strftime("%Y-%m-%d")
                dtto = self.valid_dto(dto, dtfrom)
                if not dtto is None:   # if good
                    pagesize = self.valid_pagesize(pagesize, pmax)
                    valid = True
                    emit_dfrom = dtfrom.__str__()
                    emit_dto = dtto.__str__()
        return (valid, emit_dfrom, emit_dto, pagesize)

    def listings_getter(self, rid=None, dfrom=None, dto=None, pagesize=None):
        emsg = "Bad Request"
        if rid:
            # Set up sql_str and sql_data
            sql_string = "SELECT * FROM listings WHERE id = %s;"
            data = list(self.sql_execute(sql_string, [rid], True))
        else:
            # dfrom must exist and be <= to now
            pmax = self._df_config["pg_config"]["pagesize_max"]
            (valid, dfrom, dto, pagesize) = self.valid_parm_rang(dfrom, dto, pagesize, pmax)
            if valid:
                # Set up sql_str and sql_data
                sql_str = "SELECT * FROM listings "
                sql_str += "WHERE date_posted >= %s and date_posted <= %s "
                sql_str += "ORDER BY date_posted ASC LIMIT %s;"
                sql_data = [dfrom, dto, pagesize]
                # print (sql_string)
                data = self.sql_execute(sql_str, sql_data, True, fetchall=True)                
            else:
                data = emsg
        return data

    def listings_create(self):
        with open(self._sql_create_path, "r") as sql_statment:
            sql_str = ""
            for sql_ln in sql_statment:
                sql_str += sql_ln
        return sql_str
    #self.sql_execute(sql_str, None, False)

    def get_data_factory_conf(self, file_name):
        with open(file_name) as data_file:
            dict_from_json = json.load(data_file)
        return dict_from_json


#dataFactory = DataFactory()

# item = {"date": '02/12/2017 12:00',
#         "title": "some'o title",
#         "price": "6.66",
#         "beds": "3",
#         "size": "1270",
#         "baths": "1",
#         "latitude": "78.87",
#         "longitude": "7.87",
#         "content": "some desciption",
#         "link": "some url",
#         "craigId": "1666976"}

# dataFactory.listings_setter(item)
#lrows = dataFactory.listings_getter(rid=None,dfrom='2018-02-10', dto=None, pagesize=None) # dfrom='01/23/2016'  rid=2
# lrows = dataFactory.listings_getter(rid=719,dfrom=None, dto=None, pagesize=None)
# print("json.dumps",json.dumps(lrows))
# SELECT * FROM listings WHERE date_posted >= '2018-02-09 14:00:00' and date_posted <= '2018-02-10 00:00:00' ORDER BY date_posted ASC LIMIT 1000;
#print(dataFactory.listings_create())