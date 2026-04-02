import streamlit as st
import bcrypt
import mysql.connector
import os

# Créer un nouvel utilisateur
def create_user(username, password, role, cursor):
    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    cursor.execute(
        "INSERT INTO users (nom_user, password, role) VALUES (%s, %s, %s)",
        (username, hashed, role)
    )


def get_users(cursor):
    cursor.execute("SELECT nom_user, role FROM users WHERE nom_user <> 'admin'")
    return cursor.fetchall()

def delete_user(username, cursor):
    cursor.execute("DELETE FROM users WHERE nom_user = %s", (username,))