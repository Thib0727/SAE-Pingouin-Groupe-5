import streamlit as st
from vues.page_login import login, check_auth
from vues.page_accueil import accueil
from vues.page_import_bdd import import_bdd
from vues.page_admin import gestion_user

# Pour rendre le login obligatoire
if not check_auth(): 
    login()
    st.stop()

# --- Sidebar ---
st.sidebar.title("Navigation")

# Liste des pages accessibles selon le rôle
pages = ["Accueil", "Importer la base de données"]

# Ajouter la page admin si rôle = "admin"
if st.session_state.role == "admin":
    pages.append("Gestion des utilisateurs")

# Initialisation de la page active
if "page_active" not in st.session_state:
    st.session_state.page_active = pages[0]  # par défaut la première page accessible

# Radio lié directement à session_state
st.sidebar.radio(
    "Aller à :",
    pages,
    key="page_active"  # modifie st.session_state.page_active automatiquement
)

# --- Affichage dynamique selon la page active ---
if st.session_state.page_active == "Accueil":
    accueil()
elif st.session_state.page_active == "Importer la base de données":
    import_bdd()
elif st.session_state.page_active == "Gestion des utilisateurs":
    gestion_user()