import pandas as pd

# Nommage : data_nom_du_KPI
# Simplement modifier la requete pour que ce soit les données correspondant au KPI

def data_conso_air_comprime(cursor):
    query = "SELECT CompressedAirCalc, count(*) FROM `tblfinstep` group by CompressedAirCalc;"
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=["conso", "nb"]) # toujours return un df exploitable avec les bonne colonnes