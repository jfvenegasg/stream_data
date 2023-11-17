from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql

# initialize Connector object
connector = Connector()

# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "",
        "pymysql",
        user="postgres",
        password="",
        db="stream_data"
    )
    return conn

# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)