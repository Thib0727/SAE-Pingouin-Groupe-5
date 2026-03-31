# Fonction connexion bdd root
import os
import mysql.connector
import re

def connexion_mysql_root():
    connexion = mysql.connector.connect(
        host="mysql",
        user="root",
        password=os.getenv("MYSQL_ROOT_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        use_pure=True  # <--- Ajoute ceci pour forcer le driver Python
    )
    return connexion



def prepa_sql_mes4(script_sql_mes4):
    # 1. Supprimer le BOM UTF-8 si présent
    script_sql_mes4 = script_sql_mes4.lstrip('\ufeff')
    
    # 2. Remplacement spécifique du nom de la base
    # On remplace MES4 (majuscule) par mes4 (minuscule)
    script_sql_mes4 = script_sql_mes4.replace("USE `MES4`;", "USE `mes4`;")
    script_sql_mes4 = script_sql_mes4.replace("DATABASE `MES4`", "DATABASE `mes4`")
    script_sql_mes4 = script_sql_mes4.replace("if it\'s still not working","if it s still not working")
    script_sql_mes4 = script_sql_mes4.replace("hole data but can\'t change anything","hole data but can t change anything")
    # 3. Supprimer les commentaires multi-lignes /* ... */ 
    # MAIS on garde les /*! ... */ qui sont des instructions MySQL
    # Cette regex protège les instructions commençant par /*!
    script_sql_mes4 = re.sub(r'/\*(?!!)[^*]*\*+([^/*][^*]*\*+)*/', '', script_sql_mes4)

    # 4. Supprimer les commentaires de ligne commençant par -- ou #
    # On fait attention de ne pas supprimer ce qui est à l'intérieur de quotes
    lines = []
    for line in script_sql_mes4.splitlines():
        # Supprime tout ce qui est après -- ou # si ce n'est pas dans une chaîne
        clean_line = re.sub(r'(--|#).*$', '', line).strip()
        if clean_line:
            lines.append(clean_line)

    return " ".join(lines) # On reconstruit en une seule ligne pour faciliter le split

# Fonction pour inserer un script sql dans mysql
# Si une erreur est faite durant l'execution du script alors le rollback va annuler touts les changements
# dans la bdd induits par le script
# Permet de relever l'erreur
def exec_script_mysql(script_sql, connexion_mysql):
    cursor = connexion_mysql.cursor()
    try:
        # On découpe le script par les points-virgules
        for statement in script_sql.split(';'):
            clean_statement = statement.strip()
            if clean_statement:
                cursor.execute(clean_statement)
        connexion_mysql.commit()
    except Exception as e:
        connexion_mysql.rollback()
        raise e
    finally:
        cursor.close()

import subprocess
import os

def exec_script_mysql_fast(chemin_fichier_sql):
    # Récupération des variables d'environnement
    db_password = os.getenv("rootpassword")
    db_name = "mes4" # On force le nom en minuscule ici
    db_host = "mysql" # Nom du service dans docker-compose

    try:
        # On utilise 'cat' pour lire le fichier et on l'envoie via un 'pipe' (|)
        # au client mysql du conteneur.
        # Note : on utilise --force pour ignorer les erreurs mineures si besoin
        commande = (
            f"cat {chemin_fichier_sql} | "
            f"mysql -h {db_host} -u root -p'{db_password}' {db_name}"
        )
        
        # On exécute la commande système
        resultat = subprocess.run(
            commande, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        
        print("Importation réussie avec succès via le client natif !")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'import : {e.stderr}")
        return False