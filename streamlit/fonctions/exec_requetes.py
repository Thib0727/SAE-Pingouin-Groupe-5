from fonctions.requetes_sql import *
from fonctions.connexion_sql import get_connection_db_tdb
import pandas as pd

conn = get_connection_db_tdb()
cursor = conn.cursor()

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

