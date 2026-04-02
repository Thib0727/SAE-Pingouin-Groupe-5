import streamlit as st
import pandas as pd
import plotly.express as px

def get_data_visu3():
    """
    Simule les données pour les stocks et le robot.
    À relier à tes requêtes SQL réelles.
    """
    # Données pour la distance du robot (Jaune sur la maquette)
    df_robot = pd.DataFrame({
        'Jour': ['Jour 1', 'Jour 2', 'Jour 3', 'Jour 4', 'Jour 5'],
        'Distance': [18, 10, 15, 25, 13]
    })
    return df_robot

def dashboard_visu_Gestion_des_Stocks_Robotique():
    # Titre de la page
    st.markdown("<h1 style='text-align: center; color: white; margin-bottom: 30px;'>Gestion des Stocks & Robotique</h1>", unsafe_allow_html=True)
    
    df_robot = get_data_visu3()

    # --- PARTIE HAUTE : KPI Stock ---
    # On divise l'écran en deux grandes colonnes pour les KPI du haut
    col_top_left, col_top_right = st.columns([1, 2])

    with col_top_left:
        # Deux KPI verticaux à gauche
        st.metric("Taux remplissage moyen magasin MP", "94%")
        st.write("") # Espace
        st.metric("Taux remplissage moyen magasin PF", "94%")

    with col_top_right:
        # Deux larges KPI à droite
        st.metric("Valeur stock MP :", "42 000 euros")
        st.write("") # Espace
        st.metric("Valeur stock PF :", "42 000 euros")

    st.write("---") # Séparateur

    # --- PARTIE BASSE : Graphique central entouré de KPI ---
    col_bot_1, col_bot_2, col_bot_3 = st.columns([1, 2, 1])

    with col_bot_1:
        # KPI en bas à gauche
        st.metric("Taux remplissage magasin MP", "94%")

    with col_bot_2:
        # Titre du graphique en blanc éclatant
        st.markdown("<p style='color: white; font-size: 20px; font-weight: bold; text-align: center;'>Distance parcourue par le robot</p>", unsafe_allow_html=True)
        
        fig = px.line(df_robot, x='Jour', y='Distance')
        # Ligne jaune et marqueurs comme sur la maquette
        fig.update_traces(line_color='#FFFF00', line_width=4, mode='lines+markers', marker=dict(size=10))
        
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Distance (m)",
            xaxis_title="",
            font=dict(color="white"),
            margin=dict(t=20, b=20)
        )
        # Affichage sans thème Streamlit pour garder le jaune pétant
        st.plotly_chart(fig, use_container_width=True, theme=None)

    with col_bot_3:
        # KPI en bas à droite
        st.metric("Taux remplissage magasin PF", "94%")

if __name__ == "__main__":
    dashboard_visu_Gestion_des_Stocks_Robotique()
