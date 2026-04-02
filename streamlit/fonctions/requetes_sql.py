import pandas as pd


def data_conso_air_comprime(cursor):
    query = """
    SELECT CompressedAirCalc, COUNT(*) AS nb
    FROM tblfinstep
    GROUP BY CompressedAirCalc;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=["conso", "nb"])


def data_conso_air_proche_moyenne(cursor):
    query = """
    SELECT *
    FROM tblfinstep
    WHERE  CompressedAirCalc > (SELECT AVG(CompressedAirCalc) - 1 FROM tblfinstep);
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result)


def data_conso_electrique(cursor):
    query = """
    SELECT
        resourceid,
        `start`,
        `end`,
        electricenergyreal AS puissance_watt,
        TIMESTAMPDIFF(SECOND, `start`, `end`) / 3600 AS duree_heures,
        (electricenergyreal * (TIMESTAMPDIFF(SECOND, `start`, `end`) / 3600)) / 1000 AS consommation_kwh
    FROM tblfinstep;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=[
        "resourceid", "start", "end",
        "puissance_watt", "duree_heures", "consommation_kwh"
    ])


def data_taux_remplissage_buffer(cursor):
    query = """
    SELECT
        pno,
        Quantity,
        QuantityMax,
        Quantity / NULLIF(QuantityMax, 0) AS taux_remplissage
    FROM tblbufferpos
    WHERE QuantityMax IS NOT NULL;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=[
        "pno", "quantity", "quantity_max", "taux_remplissage"
    ])


def data_pieces_erreur(cursor):
    query = """
    SELECT *
    FROM tblpartsreport
    WHERE ErrorID <> 0;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result)


def data_duree_finstep(cursor):
    query = """
    SELECT
        TIMESTAMPDIFF(SECOND, `start`, `end`) AS duree_sec
    FROM tblfinstep;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=["duree_sec"])


def data_taux_conformite(cursor):
    query = """
    SELECT
        pno,
        SUM(CASE WHEN errorid = 0 THEN 1 ELSE 0 END) AS qt_conforme,
        COUNT(*) AS qt_total,
        SUM(CASE WHEN errorid = 0 THEN 1 ELSE 0 END) / COUNT(*) AS taux_conformite
    FROM tblpartsreport
    GROUP BY pno;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=[
        "pno", "qt_conforme", "qt_total", "taux_conformite"
    ])


def data_temps_machine(cursor):
    query = """
    SELECT
        SUM(busy) AS tps_busy_sec,
        SUM(automaticmode) AS tps_auto_sec,
        SUM(manualmode) AS tps_manuel_sec,
        SUM(busy) + SUM(automaticmode) + SUM(manualmode) AS tps_total_sec
    FROM tblmachinereport;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=[
        "tps_busy_sec", "tps_auto_sec", "tps_manuel_sec", "tps_total_sec"
    ])


def data_stock_mp(cursor):
    query = """
    SELECT
        b.pnogroup,
        p.pno,
        p.type,
        SUM(b.quantity) AS stock_mp,
        MAX(b.quantitymax) AS stock_max,
        SUM(b.quantity) / NULLIF(MAX(b.quantitymax), 0) AS taux_remplissage_mp
    FROM tblbufferpos b
    JOIN tblparts p ON p.pno = b.pno
    WHERE b.pnogroup = 'MP'
    GROUP BY b.pnogroup, p.pno, p.type;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=[
        "pnogroup", "pno", "type", "stock_mp", "stock_max", "taux_remplissage_mp"
    ])


def data_temps_rotation(cursor):
    query = """
    SELECT
        AVG(TIMESTAMPDIFF(SECOND, `start`, `end`)) AS temps_rotation_sec
    FROM tblfinstep;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=["temps_rotation_sec"])


def data_buffer_parts(cursor):
    query = """
    SELECT
        b.pno,
        p.type,
        b.quantity
    FROM tblbufferpos b
    LEFT JOIN tblparts p ON b.pno = p.pno;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=["pno", "type", "quantity"])


def data_temps_moyen_commande(cursor):
    query = """
    SELECT
        AVG(TIMESTAMPDIFF(SECOND, PlannedStart, PlannedEnd)) AS temps_moyen_commande_sec
    FROM tblorder;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=["temps_moyen_commande_sec"])


def data_produits_finis_7j(cursor):
    query = """
    SELECT
        COUNT(*) AS produits_finis_7j
    FROM tblorder
    WHERE `End` BETWEEN NOW() - INTERVAL 7 DAY AND NOW();
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=["produits_finis_7j"])


def data_ratio_commandes_heure(cursor):
    query = """
    SELECT
        SUM(CASE WHEN `End` <= PlannedEnd THEN 1 ELSE 0 END) AS commandes_a_l_heure,
        SUM(CASE WHEN PlannedEnd IS NOT NULL AND `End` IS NOT NULL THEN 1 ELSE 0 END) AS commandes_totales,
        SUM(CASE WHEN `End` <= PlannedEnd THEN 1 ELSE 0 END)
          / NULLIF(SUM(CASE WHEN PlannedEnd IS NOT NULL AND `End` IS NOT NULL THEN 1 ELSE 0 END), 0) AS ratio
    FROM tblorder;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=[
        "commandes_a_l_heure", "commandes_totales", "ratio"
    ])
