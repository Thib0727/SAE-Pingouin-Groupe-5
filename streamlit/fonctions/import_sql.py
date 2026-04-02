# Fonction connexion bdd root
import os
import mysql.connector
import re
import subprocess   

def exec_import_natif(chemin_fichier):
    try:
        db_host = "mysql" 
        db_user = "root"
        db_password = os.getenv("MYSQL_ROOT_PASSWORD")
        # On ne récupère pas MYSQL_DATABASE ici pour la commande

        # COMMANDE MODIFIÉE : On enlève {db_name} à la fin
        commande = (
            f"mysql -h {db_host} -u {db_user} -p'{db_password}' "
            f"--ssl=OFF < {chemin_fichier}"
        )

        process = subprocess.run(   
            commande, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        return True, "Base de données créée et importée avec succès !"
    
    except subprocess.CalledProcessError as e:
        return False, f"Erreur MySQL : {e.stderr}"