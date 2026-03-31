import streamlit as st
import subprocess
import os
import tempfile

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

# --- Interface Streamlit ---
st.title("Importateur de Base de Données Festo")

uploaded_file = st.file_uploader("Glissez votre fichier .sql ici", type="sql")

if uploaded_file:
    if st.button("Lancer l'importation"):
        with st.spinner("Traitement et importation en cours..."):
            # 1. Lecture et modification du nom de la BDD
            raw_content = uploaded_file.getvalue().decode("utf-8")
            
            # On remplace toutes les occurrences de MES4 par mes4
            # (Plus sûr pour les CREATE/USE et les tables)
            clean_content = raw_content.replace("`MES4`", "`mes4`").replace("if it\'s still not working", "if it s still not working").replace("hole data but can\'t change anything", "hole data but can t change anything")
            # 2. Création d'un fichier temporaire sur le disque du conteneur
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False, encoding='utf-8') as tmp:
                tmp.write(clean_content)
                tmp_path = tmp.name

            # 3. Importation du premier fichier (le fichier uploadé)
            success, message = exec_import_natif(tmp_path)

            # 4. Nettoyage du fichier temporaire
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

            if success:
                # --- AJOUT ICI : Exécution du deuxième script local ---
                # On définit le chemin vers votre script stocké dans le dossier
                chemin_script_local = "db/bdd_tbd.sql" 
                
                with st.spinner("Exécution du script de post-traitement..."):
                    success_2, message_2 = exec_import_natif(chemin_script_local)
                
                if success_2:
                    st.success("Importation et post-traitement réussis !")
                else:
                    st.error(f"Premier import OK, mais erreur sur le second : {message_2}")
                # ------------------------------------------------------
            else:
                st.error(message)