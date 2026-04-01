import streamlit as st
import bcrypt
import mysql.connector
import os

# Créer un nouvel utilisateur
def create_user(username, password):
    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, hashed)
    )

