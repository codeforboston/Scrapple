# DataFactory.py
import psycopg2
import json
from datetime import datetime
# TODO support verbosity levels 1,2,3 suppress all print statements for 3

class DataFactory:
    def __init__(self):
        #self._df_config_path = "data_factory_config.json"
        self._df_config_path = "Database/data_factory_config.json"
        self._df_config = self.get_data_factory_conf(self._df_config_path)
        print("Data Factory started")
        self.db_conn = self.postgres_connect(self._df_config["pg_config"])
        if self.db_conn:
            print("Connected to db: ")
            print(self.db_conn)

    def postgres_connect(self, conn_conf):
        print("Try to connect to postgres db")
        # Connect to the postgres database
        # Define our connection string
        conn_string = "host=" + conn_conf["host"]
        conn_string += " port=" + conn_conf["port"]
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

    def format_row_data(self, rows, colnames):
        lrows = []
        for row in rows:
            drow = dict(zip(colnames, row))
            lrows.append(drow)
        return lrows

    def sql_execute(self, sql_string, fetch, fetchall=None):
        # Open a cursor to perform database operations
        cur = self.db_conn.cursor()
        # Psycopg sql execute
        cur.execute(sql_string)
        if fetch:
            if fetchall:
                rows = cur.fetchall()
                colnames = [desc[0] for desc in cur.description]
                x = self.format_row_data(rows, colnames)
            else:
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

    # validation helper methods
    def valid_pagesize(self, pagesize, pmax):
        if pagesize:
            if not (pagesize > 0 and pagesize <= pmax):
                pagesize = pmax
        else:
            pagesize = pmax
        return pagesize

    def dt_str_2_dt(self, sdate):
        # convert string date inputs to datetime formats
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
        # check the parameters are invalid ranges
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
        # TODO verify parameters in valid range
        emsg = "Bad Request"
        if rid:
            sql_string = "SELECT * FROM listings WHERE id = {};".format(rid)
            data = self.sql_execute(sql_string, True)
        else:
            # dfrom must exist and be <= to now
            pmax = self._df_config["pg_config"]["pagesize_max"]
            (valid, dfrom, dto, pagesize) = self.valid_parm_rang(dfrom, dto, pagesize, pmax)
            if valid:
                # exiqut (dfrom, dto, pagesize)
                sql_string = "SELECT * FROM listings "
                sql_string += "WHERE date_posted >= '{}' and date_posted <= '{}' "
                sql_string += "ORDER BY date_posted ASC LIMIT {};"
                sql_string = sql_string.format(dfrom, dto, pagesize)
                print (sql_string)
                data = self.sql_execute(sql_string, True, fetchall=True)
                for row in data:
                    row["date_posted"] = row["date_posted"].__str__()
                    row["date_created"] = row["date_created"].__str__()
            else:
                data = emsg
        return data

    def get_data_factory_conf(self, file_name):
        with open(file_name) as data_file:
            dict_from_json = json.load(data_file)
        return dict_from_json

#dataFactory = DataFactory()


# data = {"date_posted": '01/12/2018 14:54',
#         "listing_title": "some title",
#         "price": "6.66",
#         "money": "some title",
#         "latitude": "78.87",
#         "longitude": "7.87",
#         "address": "some address",
#         "desciption": "some desciption",
#         "link": "some url",
#         "listing_id": "some listing_id"}

# #dataFactory.listings_setter(data)
# lrows = dataFactory.listings_getter(rid=None,dfrom='01/23/2016', dto=None, pagesize=None) # dfrom='01/23/2016'  rid=2

# print(json.dumps(lrows))

# # print("dt_str_2_dt:",dataFactory.dt_str_2_dt('01/23/20c16'))
# # print("valid_dfrom:",dataFactory.valid_dfrom('01/23/20c16'))
# # print("valid_parm_rang:",dataFactory.valid_parm_rang('01/23/20c16', '12/23/2017', 4, 23))

