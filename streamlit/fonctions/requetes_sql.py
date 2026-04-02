import pandas as pd


def data_conso_air_comprime(cursor):
    query = """
    SELECT End, CompressedAirCalc
    FROM tblfinstep
    WHERE DATE(End) = (
        SELECT DATE(End)
        FROM tblfinstep
        WHERE CompressedAirCalc IS NOT NULL
        ORDER BY End DESC
        LIMIT 1
    )
    AND CompressedAirCalc IS NOT NULL
    ORDER BY End DESC
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=["Date-heure", "Air comprimé"])


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
    SELECT End, ElectricEnergyCalc
    FROM tblfinstep
    WHERE DATE(End) = (
        SELECT DATE(End)
        FROM tblfinstep
        WHERE ElectricEnergyCalc IS NOT NULL
        ORDER BY End DESC
        LIMIT 1
    )
    AND ElectricEnergyCalc IS NOT NULL
    ORDER BY End DESC
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=["Date-heure","Consommation (mWs)"])


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
        AVG(Busy) * 100 AS proportion_busy,
        AVG(1 - Busy) * 100 AS proportion_non_busy
    FROM tblmachinereport
    WHERE DATE(TimeStamp) = (

        SELECT DATE(MAX(TimeStamp))
        FROM tblmachinereport
    );
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=[
        "Temps occupé","Temps libre"
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
    SELECT SUM(temps_moyen_etape) AS temps_rotation_total_secondes
    FROM (
        SELECT 
            Description,
            AVG(TIMESTAMPDIFF(SECOND, Start, End)) AS temps_moyen_etape
        FROM tblfinstep
        WHERE Description IN (
            'feed back cover from magazine',
            'Select PCB Box with content',
            'Select Box with content',
            'store box to target',
            'Select parts to send into ASRS20'
        )
        AND DATE(End) = (
            -- On cible uniquement la dernière journée d'activité
            SELECT DATE(MAX(End)) 
            FROM tblfinstep 
            WHERE End IS NOT NULL
        )
        AND Start IS NOT NULL 
        AND End IS NOT NULL
        GROUP BY Description
    ) AS sous_requete_moyennes;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=["Moyenne temps rotation"])


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

def data_temps_assemblage_moyen(cursor):
    query = """
    SELECT 
        Description,
        AVG(TIMESTAMPDIFF(SECOND, Start, End)) AS temps_moyen_secondes
    FROM tblfinstep
    WHERE DATE(End) = (
        SELECT DATE(MAX(End)) 
        FROM tblfinstep 
        WHERE End IS NOT NULL
    )
    AND Start IS NOT NULL 
    AND End IS NOT NULL
    GROUP BY Description;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=["Etape","Temps moyen en secondes"])

def data_conformite_assemblage(cursor):
    query = """
    SELECT 
        CASE WHEN ErrorID = 0 THEN 'Conforme' ELSE 'Non conforme' END AS Status,
        COUNT(*) AS Value
    FROM tblpartsreport
    WHERE ResourceID = 3  -- Remplacer 3 par le numéro exact de ta station d'assemblage si ce n'est pas ça
    GROUP BY CASE WHEN ErrorID = 0 THEN 'Conforme' ELSE 'Non conforme' END;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=[
        "Status", "Value"
    ])

def data_conformite_visuelle(cursor):
    query = """
    SELECT 
        CASE WHEN ErrorID = 0 THEN 'Conforme' ELSE 'Non conforme' END AS Status,
        COUNT(*) AS Value
    FROM tblpartsreport
    WHERE ResourceID = 5  -- À remplacer par le numéro exact de ta station caméra
    GROUP BY CASE WHEN ErrorID = 0 THEN 'Conforme' ELSE 'Non conforme' END;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=["Status", "Value"])

def data_pieces_manquantes_pbl(cursor):
    query = """
    SELECT 
        DATE(TimeStamp) AS Jour,
        COUNT(*) AS Value
    FROM tblpartsreport
    WHERE ErrorID IN (23, 31, 42)
    GROUP BY DATE(TimeStamp)
    ORDER BY DATE(TimeStamp)
    LIMIT 5;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    # Formatage de la date pour un affichage plus propre (ex: "Jour 1", ou on garde la date SQL)
    df = pd.DataFrame(result, columns=["Jour", "Value"])
    df['Jour'] = df['Jour'].astype(str) # Convertit la date en texte pour Plotly
    return df

def data_otif_par_jour(cursor):
    query = """
    SELECT 
        DATE(`End`) AS Jour, 
        'On time' AS Type, 
        COUNT(*) AS Count
    FROM tblorder 
    WHERE `End` <= PlannedEnd AND `End` IS NOT NULL 
    GROUP BY DATE(`End`)
    
    UNION ALL
    
    SELECT 
        DATE(`End`) AS Jour, 
        'Late' AS Type, 
        COUNT(*) AS Count
    FROM tblorder 
    WHERE `End` > PlannedEnd AND `End` IS NOT NULL 
    GROUP BY DATE(`End`)
    
    ORDER BY Jour, Type;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=["Jour", "Type", "Count"])
    df['Jour'] = df['Jour'].astype(str)
    return df
    )
    AND Start IS NOT NULL 
    AND End IS NOT NULL
    GROUP BY Description;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=["Etape","Temps moyen en secondes"])

def data_lead_time_moyen(cursor):
    query = """
    SELECT 
        SUM(TIMESTAMPDIFF(SECOND, Start, End)) / COUNT(ONo) AS temps_realisation_moyen_secondes
    FROM tblorder
    WHERE DATE(End) = (
        SELECT DATE(MAX(End)) 
        FROM tblorder 
        WHERE End IS NOT NULL
    )
    AND Start IS NOT NULL 
    AND End IS NOT NULL;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=["lead_time_moyen"])
