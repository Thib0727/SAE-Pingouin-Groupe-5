import mysql.connector
import os

def get_connection_users():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password=os.getenv("MYSQL_ROOT_PASSWORD"),
        database="users"
    )

def get_connection_db_tdb():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password=os.getenv("MYSQL_ROOT_PASSWORD"),
        database="exploit"
    )