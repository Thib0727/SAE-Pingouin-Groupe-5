import streamlit as st
import bcrypt
import pandas as pd
from fonctions.connexion_sql import get_connection_users
from fonctions.gestion_user import create_user, get_users, delete_user

def gestion_user():

    st.title("Gestion des comptes utilisateurs")

    tab1, tab2 = st.tabs(["➕ Ajouter", "🗑️ Supprimer"])

    with tab1:
        st.title("Ajouter un utilisateur")

        with st.form("user_form"):
                
            role = st.radio(
            "Rôle",
            ["admin", "standard"],
            horizontal=True
        )
            username = st.text_input("Nom d'utilisateur")
            password1 = st.text_input("Mot de passe", type="password")
            password2 = st.text_input("Confirmer le mot de passe", type="password")

            submit = st.form_submit_button("Créer l'utilisateur")
        
        if submit:

            if password1 != password2 :
                st.error("Les deux mots de passe doivent être identiques")
            else :
                password = password1
        
                if username and password:
                    try:
                        conn = get_connection_users()
                        cursor = conn.cursor()

                        create_user(username, password1, role, cursor)

                        conn.commit()

                        st.success(f"Utilisateur '{username}' créé avec succès ✅")

                    except Exception as e:
                        st.error(f"Erreur lors de la création : {e}")

                    finally:
                        cursor.close()
                        conn.close()

                else:
                    st.error("Veuillez remplir tous les champs")

    with tab2:
        st.title("Supprimer un utilisateur")

        conn = get_connection_users()
        cursor = conn.cursor()

        users = get_users(cursor)

        df = pd.DataFrame(users, columns=["Nom", "Rôle"])

        # 🔍 Barre de recherche
        search = st.text_input("Rechercher un utilisateur")

        if search:
            df = df[df["Nom"].str.contains(search, case=False)]

        # 🧾 Table avec sélection
        selected_user = st.selectbox(
            "Sélectionner un utilisateur",
            df["Nom"].tolist()
        )

        st.dataframe(df, use_container_width=True)

        # ⚠️ Confirmation
        confirm = st.checkbox("Confirmer la suppression")

        if st.button("Supprimer"):
            if not selected_user:
                st.warning("Veuillez sélectionner un utilisateur")

            elif not confirm:
                st.warning("Veuillez confirmer la suppression")

            elif selected_user != "admin":
                try:
                    delete_user(selected_user, cursor)
                    conn.commit()

                    st.success(f"Utilisateur '{selected_user}' supprimé ✅")

                except Exception as e:
                    st.error(f"Erreur : {e}")
            else :
                st.error("Vous ne pouvez pas supprimer le compte administrateur par défaut")

        cursor.close()
        conn.close()