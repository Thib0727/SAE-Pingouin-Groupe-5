import streamlit as st
from vues.page_login import login, check_auth
from vues.page_accueil import accueil
from vues.page_import_bdd import import_bdd
from vues.page_admin import gestion_user
from fonctions.connexion_sql import get_connection_db_tdb, connexion_mysql_root, base_existe
from fonctions.requetes_sql import *
import pandas as pd

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

if st.sidebar.button("Actualiser les KPI"):
    # 1 vérifier que la bdd existe avant de tenter d'actualiser les kpi
    conn = connexion_mysql_root()
    cursor = conn.cursor()

    nom_base = "exploit"
    if not base_existe(cursor, nom_base):
        st.error(f"La base de données n'a pas été importée/connectée")
        cursor.close()
        conn.close()
    else:

        cursor.close()
        conn.close()

        conn = get_connection_db_tdb()
        cursor = conn.cursor()
        # Vérifier si la base existe

        df_conso_air_comprime = data_conso_air_comprime(cursor)
        df_conso_air_proche_moyenne = data_conso_air_proche_moyenne(cursor)
        df_conso_electrique = data_conso_electrique(cursor)
        df_taux_remplissage_buffer = data_taux_remplissage_buffer(cursor)
        df_pieces_erreur = data_pieces_erreur(cursor)
        df_duree_finstep = data_duree_finstep(cursor)
        df_taux_conformite = data_taux_conformite(cursor)
        df_temps_machine = data_temps_machine(cursor)
        df_stock_mp = data_stock_mp(cursor)
        df_temps_rotation = data_temps_rotation(cursor)
        df_buffer_parts = data_buffer_parts(cursor)
        df_temps_moyen_commande = data_temps_moyen_commande(cursor)
        df_produits_finis_7j = data_produits_finis_7j(cursor)
        df_ratio_commandes_heure = data_ratio_commandes_heure(cursor)

        cursor.close()
        conn.close()

st.sidebar.markdown("---")

if st.sidebar.button("Se déconnecter"):
    st.session_state.clear()
    st.rerun()

# --- Affichage dynamique selon la page active ---
if st.session_state.page_active == "Accueil":
    accueil()
elif st.session_state.page_active == "Importer la base de données":
    import_bdd()
elif st.session_state.page_active == "Gestion des utilisateurs":
    gestion_user()