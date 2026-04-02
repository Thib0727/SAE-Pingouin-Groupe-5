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

def connexion_mysql_root():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password=os.getenv("MYSQL_ROOT_PASSWORD"),
    )

def base_existe(cursor, nom_base):
    cursor.execute("SHOW DATABASES LIKE %s;", (nom_base,))
    return cursor.fetchone() is not None