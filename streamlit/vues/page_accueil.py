import streamlit as st

def accueil():
    st.title("Accueil")
    st.write(f"Connecté : {st.session_state.user}")