import streamlit as st
from vues.page_login import login, check_auth
from vues.page_accueil import accueil
from vues.page_import_bdd import import_bdd
from vues.page_admin import gestion_user
from fonctions.connexion_sql import get_connection_db_tdb, connexion_mysql_root, base_existe
from fonctions.requetes_sql import *
from fonctions.exec_requetes import load_all_kpi_data
import pandas as pd
from vues.visu_Production import dashboard_visu_Production
from vues.visu_Qualité_Logistique import dashboard_visu_Qualité_Logistique
from vues.visu_Gestion_des_Stocks_Robotique import dashboard_visu_Gestion_des_Stocks_Robotique

# Pour rendre le login obligatoire
if not check_auth(): 
    login()
    st.stop()

# --- Sidebar ---
st.sidebar.title("Navigation")

# --- Dans app.py ---
st.markdown("""
    <style>
    /* Fond de l'application */
    .stApp { background-color: #2d2942; }
    
    /* Titre st.title en blanc pur */
    .stApp h1 { 
        color: white !important; 
        font-weight: bold !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }

    /* Style des cartes KPI */
    [data-testid="stMetric"] {
        background-color: #413d58;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #5d587a;
    }

    /* Labels des KPI (Gris clair mais lisible) */
    [data-testid="stMetricLabel"] > div {
        color: #e0e0e0 !important;
    }
    
    /* Valeurs des KPI (Blanc pur) */
    [data-testid="stMetricValue"] > div {
        color: white !important;
        font-weight: bold !important;
    }

    /* Correction du texte général : On enlève l'opacité 0.9 qui grisait tout */
    .stMarkdown div p {
        color: white !important;
    }
    .block-container {
    padding-top: 3rem !important;
    padding-bottom: 1rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 98% !important; /* Force l'utilisation de la quasi-totalité de la largeur */
    }
    </style>
""", unsafe_allow_html=True)




# Liste des pages accessibles selon le rôle
pages = ["Importer la base de données", "Production", "Qualité & Logistique", "Gestion des Stocks & Robotique"]


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

if st.sidebar.button("Actualiser les KPI"):
    # On vide le cache pour forcer la lecture SQL
    st.cache_data.clear()
    
    resultats = load_all_kpi_data()
    
    if resultats is None:
        st.error("La base de données n'a pas été importée/connectée")
    else:
        # Tu peux stocker les données dans le session_state pour les utiliser ailleurs
        st.session_state['all_data'] = resultats
        st.success("Données actualisées !")

st.sidebar.markdown("---")

if st.sidebar.button("Se déconnecter"):
    st.session_state.clear()
    st.rerun()

# --- Affichage dynamique selon la page active ---
if st.session_state.page_active == "Importer la base de données":
    import_bdd()
elif st.session_state.page_active == "Gestion des utilisateurs":
    gestion_user()
elif st.session_state.page_active == "Production":
    dashboard_visu_Production()
elif st.session_state.page_active == "Qualité & Logistique":
    dashboard_visu_Qualité_Logistique()
elif st.session_state.page_active == "Gestion des Stocks & Robotique":
    dashboard_visu_Gestion_des_Stocks_Robotique()

