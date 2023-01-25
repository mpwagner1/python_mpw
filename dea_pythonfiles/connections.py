from pymongo import MongoClient
import pyodbc as sql
import urllib.parse
import sqlalchemy as sa
import pandas as pd

uri_prod = "mongodb://PRDMngDEA:xsruS)n5PAZ1@PRDCH3MONGO11.coyotelogistics.local:27017,PRDCH3MONGO12.coyotelogistics.local:27017,PRDCH3MONGO13.coyotelogistics.local:27017/?replicaSet=PRDMONGOREPL&readPreference=secondary&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1"
uri_staging = "mongodb://STGMngDEA:kVlB(jwbX2VelW@STGCH3MONGO11.coyotelogistics.local:27017/?connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1"
uri_fastlane = "mongodb://FSLMngDEA:PMyly0x3N8)00a4@fslch3mongo11:27017/admin?replicaSet=FSLMONGOREPL&serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1&3t.uriVersion=3&3t.connection.name=FastLane&3t.databases=admin"


def get_collection(database, collection):
    # mongodb uri string for replica set secondary reads
    uri = uri_prod
    client = MongoClient(uri)
    database = client[database]
    collection = database[collection]
    return client, collection


def get_sql_database_engine(server, database):
    connection_string = "DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={};DATABASE={};Trusted_Connection=yes;Encrypt=yes".format(
        server, database
    )
    quoted = urllib.parse.quote_plus(connection_string)
    engine = sa.create_engine("mssql+pyodbc:///?odbc_connect={}".format(quoted))
    engine.connect()
    return engine


def SQL_Run_Query(server, database, query):
    """Loads query into dataframe"""
    conn = sql.connect(
        "Driver=ODBC Driver 17 for SQL Server;"
        "Server={};"
        "Database={};"
        "Trusted_Connection=yes;Encrypt=yes".format(server, database)
    )

    table = pd.read_sql(query, conn)
    return table


def get_fast_sql_database_engine(server, database):
    """Creates an Engine to Insert Data in SQL. This is Faster but Will fail with boolean or Datetime2"""
    connection_string = "DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={};DATABASE={};Trusted_Connection=yes;Encrypt=yes".format(
        server, database
    )
    quoted = urllib.parse.quote_plus(connection_string)
    engine = sa.create_engine(
        "mssql+pyodbc:///?odbc_connect={}".format(quoted), fast_executemany=True
    )
    engine.connect()
    return engine
