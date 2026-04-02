import streamlit as st
from fonctions.requetes_sql import *
from fonctions.connexion_sql import get_connection_db_tdb
import pandas as pd
from fonctions.connexion_sql import get_connection_db_tdb, connexion_mysql_root, base_existe
from fonctions.requetes_sql import *

@st.cache_data(show_spinner="Actualisation des données...")
def load_all_kpi_data():
    """Charge l'ensemble des données depuis la base de données."""
    # 1. Vérification de l'existence de la base
    conn_root = connexion_mysql_root()
    cursor_root = conn_root.cursor()
    nom_base = "exploit"
    
    if not base_existe(cursor_root, nom_base):
        cursor_root.close()
        conn_root.close()
        return None
    
    cursor_root.close()
    conn_root.close()

    # 2. Récupération des données
    conn = get_connection_db_tdb()
    cursor = conn.cursor()
    
    try:
        data = {
            "df_conso_air_comprime": data_conso_air_comprime(cursor),
            "df_conso_air_proche_moyenne": data_conso_air_proche_moyenne(cursor),
            "df_conso_electrique": data_conso_electrique(cursor),
            "df_taux_remplissage_buffer": data_taux_remplissage_buffer(cursor),
            "df_pieces_erreur": data_pieces_erreur(cursor),
            "df_duree_finstep": data_duree_finstep(cursor),
            "df_taux_conformite": data_taux_conformite(cursor),
            "df_temps_machine": data_temps_machine(cursor),
            "df_stock_mp": data_stock_mp(cursor),
            "df_temps_rotation": data_temps_rotation(cursor),
            "df_buffer_parts": data_buffer_parts(cursor),
            "df_temps_moyen_commande": data_temps_moyen_commande(cursor),
            "df_produits_finis_7j": data_produits_finis_7j(cursor),
            "df_ratio_commandes_heure": data_ratio_commandes_heure(cursor),
            "df_temps_assemblage_moyen": data_temps_assemblage_moyen(cursor),
            "df_conformite_assemblage" : data_conformite_assemblage(cursor),
            "df_verif_visuelle" : data_conformite_visuelle(cursor),
            "df_pieces_manquantes" : data_pieces_manquantes_pbl(cursor),
            "df_otif" : data_otif_par_jour(cursor)
        }
    finally:
        cursor.close()
        conn.close()
        
    return data
