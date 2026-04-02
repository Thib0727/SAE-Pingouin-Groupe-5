import streamlit as st
import pandas as pd
import plotly.express as px

# --- RÉCUPÉRATION DES DONNÉES ---
def get_data_visu2():
    """
    Simule les données pour la Qualité et la Logistique.
    Structure corrigée pour éviter l'erreur 'All arrays must be of the same length'.
    """
    # 1. Données pour les Camemberts (Pie Charts)
    df_ass = pd.DataFrame({'Status': ['Conforme', 'Non conforme'], 'Value': [90.9, 9.1]})
    df_vis = pd.DataFrame({'Status': ['Conforme', 'Non conforme'], 'Value': [93.8, 6.2]})
    
    # 2. Données pour la Courbe (Pièces manquantes)
    df_missing = pd.DataFrame({
        'Jour': ['Jour 1', 'Jour 2', 'Jour 3', 'Jour 4', 'Jour 5'],
        'Value': [0, 0, 2, 0, 1]
    })
    
    # 3. Données pour l'OTIF (Barres groupées) - CORRIGÉ : 6 éléments partout
    df_otif = pd.DataFrame({
        'Jour': ['J1', 'J1', 'J2', 'J2', 'J3', 'J3'],
        'Type': ['On time', 'Late', 'On time', 'Late', 'On time', 'Late'],
        'Count': [100, 8, 95, 15, 145, 20]
    })
    
    return df_ass, df_vis, df_missing, df_otif

# --- FONCTION PRINCIPALE ---
def dashboard_visu_Qualité_Logistique():
    # Titre de la page
    st.markdown("<h1 style='text-align: center; color: white;'>Indicateurs Qualité & Logistique</h1>", unsafe_allow_html=True)
    
    # Récupération des données corrigées
    df_ass, df_vis, df_missing, df_otif = get_data_visu2()
    
    if 'all_data' in st.session_state:
        df_ass = st.session_state['all_data']['df_conformite_assemblage']
        df_vis = st.session_state['all_data']['df_verif_visuelle']
        df_missing = st.session_state['all_data']['df_pieces_manquantes']
        df_otif = st.session_state['all_data']['df_otif']
        
        

    

        # --- LIGNE 1 : CAMEMBERT & COURBE ---
        col1, col2 = st.columns(2)
        st.write("---")

        with col1:
            # Titre HTML pour éviter le voile gris
            st.markdown("<h3 style='color: white; text-align: center; font-family: sans-serif;'>CONFORMITÉ MODULE D'ASSEMBLAGE</h3>", unsafe_allow_html=True)
            
            fig1 = px.pie(df_ass, values='Value', names='Status', 
                        color='Status', color_discrete_map={'Conforme':'#4296d1', 'Non conforme':'#ffb71c'})
            fig1.update_traces(textinfo='percent+label', textposition='outside')
            fig1.update_layout(
                template="plotly_dark", 
                paper_bgcolor='rgba(0,0,0,0)', 
                font=dict(color="white"),
                showlegend=False, 
                margin=dict(t=30, b=30)
            )
            st.plotly_chart(fig1, use_container_width=True, theme=None)

        with col2:
            st.markdown("<h3 style='color: white; text-align: center; font-family: sans-serif;'>PIÈCES MANQUANTES (PICK BY LIGHT)</h3>", unsafe_allow_html=True)
            
            fig2 = px.line(df_missing, x='Jour', y='Value')
            fig2.update_traces(line_color='#70e0e8', line_width=4, mode='lines+markers')
            fig2.update_layout(
                template="plotly_dark", 
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_title="Nombre", 
                font=dict(color="white")
            )
            st.plotly_chart(fig2, use_container_width=True, theme=None)

        # --- LIGNE 2 : CAMEMBERT & OTIF ---
        col3, col4 = st.columns(2)

        with col3:
            st.markdown("<h3 style='color: white; text-align: center; font-family: sans-serif;'>CONFORMITÉ VÉRIFICATION VISUELLE</h3>", unsafe_allow_html=True)
            
            fig3 = px.pie(df_vis, values='Value', names='Status', 
                        color='Status', color_discrete_map={'Conforme':'#4296d1', 'Non conforme':'#ffb71c'})
            fig3.update_traces(textinfo='percent+label', textposition='outside')
            fig3.update_layout(
                template="plotly_dark", 
                paper_bgcolor='rgba(0,0,0,0)', 
                font=dict(color="white"),
                showlegend=False, 
                margin=dict(t=30, b=30)
            )
            st.plotly_chart(fig3, use_container_width=True, theme=None)

        with col4:
            # Titre en VERT FLUO pour celui-là, comme tu aimais sur la visu1
            st.markdown("<h3 style='color: white; text-align: center; font-family: sans-serif;'>OTIF (DELIVERY PERFORMANCE)</h3>", unsafe_allow_html=True)
            
            fig4 = px.bar(df_otif, x='Jour', y='Count', color='Type', barmode='group',
                        color_discrete_map={'On time':'#70e0e8', 'Late':'#ffb71c'})
            fig4.update_layout(
                template="plotly_dark", 
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="white"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig4, use_container_width=True, theme=None)
