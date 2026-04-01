import streamlit as st
import bcrypt
from fonctions.connexion_sql import get_connection_users

def login():
    st.title("Login")

    username = st.text_input("Utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Connexion"):
        conn = get_connection_users()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT nom_user, password, role FROM users WHERE nom_user=%s",
            (username,)
        )

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            user, stored_hash, role = result

            if bcrypt.checkpw(
                password.encode(),
                stored_hash.encode()
            ):
                st.session_state.auth = True
                st.session_state.user = user
                st.session_state.role = role
                st.rerun()

        st.error("Login incorrect")


def check_auth():
    return st.session_state.get("auth", False)