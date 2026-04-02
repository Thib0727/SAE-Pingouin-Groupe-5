import streamlit as st
import pandas as pd
import plotly.express as px


def dashboard_visu_Production():
    # 1. On force le titre principal en blanc
    st.markdown("<h1 style='text-align: center; color: white;'>Tableau de bord de production</h1>", unsafe_allow_html=True)
    
    if 'all_data' in st.session_state:
        df_air = st.session_state['all_data']['df_conso_air_comprime']
        df_tmps_ass_moyen = st.session_state['all_data']['df_temps_assemblage_moyen']
        df_elec = st.session_state['all_data']['df_conso_electrique']
        df_machine = st.session_state['all_data']['df_temps_machine']
        df_rotation = st.session_state['all_data']['df_temps_rotation']
        df_lead_time_moyen = st.session_state['all_data']['df_lead_time_moyen']

        # --- LIGNE 1 : KPI ---
        col_kpi1, col_kpi2, _ = st.columns([1, 1, 2])
        with col_kpi1:
            # On extrait la valeur (en supposant qu'il n'y a qu'une ligne)
            valeur_rotation = df_rotation['Moyenne temps rotation'].iloc[0]

            # On l'affiche dans le metric en formatant pour ne pas avoir trop de décimales
            st.metric("Temps de rotation moyen", f"{valeur_rotation:.0f} secondes")
        with col_kpi2:
            # 1. Vérifier d'abord si le DataFrame n'est pas vide
            if df_lead_time_moyen.empty or pd.isna(df_lead_time_moyen['lead_time_moyen'].iloc[0]):
                st.metric("Lead time moyen", "Pas de données")
            else:
                # 2. Récupérer la valeur
                valeur_lead_time = df_lead_time_moyen['lead_time_moyen'].iloc[0]
                
                # 3. Affichage (conversion en int pour supprimer les .0)
                st.metric("Lead time moyen", f"{int(valeur_lead_time)} secondes")

        st.write("---")

        # --- LIGNE 2 : GRAPHIQUES ---
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h3 style='color: white; text-align: center; font-family: sans-serif;'>CONSOMMATION D'AIR COMPRIMÉ</h3>", unsafe_allow_html=True)

            fig_air = px.line(df_air, x='Date-heure', y='Air comprimé')
            fig_air.update_traces(line_color='#00f2ff', line_width=4, mode='lines+markers')
            fig_air.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=20), font=dict(color="white"))

            st.plotly_chart(fig_air, use_container_width=True, theme=None)

        with col2:
            st.markdown("<h3 style='color: white; text-align: center; font-family: sans-serif;'>TEMPS D'ASSEMBLAGE MOYEN DE LA DERNIERE JOURNEE DE PRODUCTION</h3>", unsafe_allow_html=True)

            # Création du Bar Chart
            # Note : J'ajoute color_discrete_sequence pour appliquer ta couleur directement
            fig_ass = px.bar(
                df_tmps_ass_moyen, 
                x='Etape', 
                y='Temps moyen en secondes',
                text_auto='.1f' # Affiche la valeur au-dessus des barres (optionnel)
            )

            # Style des barres
            fig_ass.update_traces(
                marker_color='#00f2ff', 
                marker_line_color='#00f2ff',
                marker_line_width=1.5, 
                opacity=0.8
            )

            # Layout (Conservation de ton style sombre et transparent)
            fig_ass.update_layout(
                template="plotly_dark", 
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)', 
                margin=dict(t=20), 
                font=dict(color="white"),
                xaxis={'categoryorder':'total descending'} # Trie automatiquement les barres de la plus grande à la plus petite
            )

            st.plotly_chart(fig_ass, use_container_width=True, theme=None)

        # --- LIGNE 3 ---
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("<h3 style='color: white; text-align: center; font-family: sans-serif;'>CONSOMMATION D'ÉLECTRICITÉ</h3>", unsafe_allow_html=True)
            fig_elec = px.line(df_elec, x='Date-heure', y='Consommation (mWs)')
            fig_elec.update_traces(line_color='#ffff00', line_width=4, mode='lines+markers')
            fig_elec.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=20), font=dict(color="white"))
            st.plotly_chart(fig_elec, use_container_width=True, theme=None)

        with col4:
            st.markdown("<h3 style='color: white; text-align: center; font-family: sans-serif;'>UTILISATION DU BRAS ROBOTISÉ</h3>", unsafe_allow_html=True)

            fig_bras = px.pie(
                names=['Temps occupé', 'Temps libre'],
                values=[df_machine['Temps occupé'].iloc[0], df_machine['Temps libre'].iloc[0]],
                hole=0.6,
                color_discrete_sequence=['#00f2ff', '#333333']
)

            # Style et cosmétique
            fig_bras.update_traces(
                textposition='inside', 
                textinfo='percent',
                hoverinfo='label+value',
                marker=dict(line=dict(color='#00f2ff', width=1))
            )

            fig_bras.update_layout(
                template="plotly_dark", 
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)', 
                margin=dict(t=30, b=0, l=0, r=0), 
                font=dict(color="white"),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
            )

            st.plotly_chart(fig_bras, use_container_width=True, theme=None)
