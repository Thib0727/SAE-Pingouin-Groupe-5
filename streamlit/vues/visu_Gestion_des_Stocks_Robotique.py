import streamlit as st
import pandas as pd
import plotly.express as px


def dashboard_visu_Gestion_des_Stocks_Robotique():
    st.markdown(
        "<h1 style='text-align: center; color: white; margin-bottom: 30px;'>"
        "Gestion des Stocks & Robotique</h1>",
        unsafe_allow_html=True,
    )

    if "all_data" not in st.session_state:
        st.warning("Les données ne sont pas encore chargées.")
        return

    data = st.session_state["all_data"]

    df_stock_mp         = data["df_stock_mp"]              # pnogroup, pno, type, stock_mp, stock_max, taux_remplissage_mp
    df_taux_remplissage = data["df_taux_remplissage_buffer"]  # pno, quantity, quantity_max, taux_remplissage
    df_temps_rotation   = data["df_temps_rotation"]        # temps_rotation_sec  (scalaire)
    df_buffer_parts     = data["df_buffer_parts"]          # pno, type, quantity

    # ------------------------------------------------------------------ #
    #  Calcul des KPI scalaires                                           #
    # ------------------------------------------------------------------ #

    # Taux remplissage moyen magasin MP
    taux_mp_moyen = df_stock_mp["taux_remplissage_mp"].mean()
    taux_mp_moyen_str = f"{taux_mp_moyen * 100:.1f} %" if pd.notna(taux_mp_moyen) else "N/A"

    # Taux remplissage moyen buffer global
    taux_buffer_moyen = df_taux_remplissage["taux_remplissage"].mean()
    taux_buffer_moyen_str = f"{taux_buffer_moyen * 100:.1f} %" if pd.notna(taux_buffer_moyen) else "N/A"

    # Quantité totale stock MP
    qt_stock_mp = df_stock_mp["stock_mp"].sum()
    qt_stock_mp_str = f"{int(qt_stock_mp)} pièces" if pd.notna(qt_stock_mp) else "N/A"

    # Quantité totale buffer (tous types)
    qt_buffer = df_buffer_parts["quantity"].sum()
    qt_buffer_str = f"{int(qt_buffer)} pièces" if pd.notna(qt_buffer) else "N/A"

    # Temps de rotation moyen robot
    temps_rotation = df_temps_rotation["temps_rotation_sec"].iloc[0]
    if pd.notna(temps_rotation):
        minutes = int(temps_rotation // 60)
        secondes = int(temps_rotation % 60)
        temps_rotation_str = f"{minutes}m {secondes:02d}s"
    else:
        temps_rotation_str = "N/A"

    # Taux remplissage instantané (dernière position MP enregistrée)
    taux_mp_inst = df_stock_mp["taux_remplissage_mp"].iloc[-1]
    taux_mp_inst_str = f"{taux_mp_inst * 100:.1f} %" if pd.notna(taux_mp_inst) else "N/A"

    # ------------------------------------------------------------------ #
    #  PARTIE HAUTE : KPI Stock                                           #
    # ------------------------------------------------------------------ #
    col_top_left, col_top_right = st.columns([1, 2])

    with col_top_left:
        st.metric("Taux remplissage moyen magasin MP", taux_mp_moyen_str)
        st.write("")
        st.metric("Taux remplissage moyen buffer", taux_buffer_moyen_str)

    with col_top_right:
        st.metric("Quantité stock MP", qt_stock_mp_str)
        st.write("")
        st.metric("Quantité buffer (tous types)", qt_buffer_str)

    st.write("---")

    # ------------------------------------------------------------------ #
    #  PARTIE BASSE : Bar chart taux remplissage MP + KPI robot           #
    # ------------------------------------------------------------------ #
    col_bot_1, col_bot_2, col_bot_3 = st.columns([1, 2, 1])

    with col_bot_1:
        st.metric("Taux remplissage MP (dernier)", taux_mp_inst_str)

    with col_bot_2:
        st.markdown(
            "<p style='color: white; font-size: 20px; font-weight: bold; text-align: center;'>"
            "Taux de remplissage par référence MP</p>",
            unsafe_allow_html=True,
        )

        df_chart = df_stock_mp[["pno", "taux_remplissage_mp"]].copy()
        df_chart["taux_remplissage_mp"] = df_chart["taux_remplissage_mp"] * 100

        fig = px.bar(
            df_chart,
            x="pno",
            y="taux_remplissage_mp",
            labels={"pno": "Référence", "taux_remplissage_mp": "Taux remplissage (%)"},
            text_auto=".1f",
        )
        fig.update_traces(
            marker_color="#FFFF00",
            marker_line_color="#FFFF00",
            marker_line_width=1.5,
            opacity=0.85,
        )
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(range=[0, 110], title="Taux (%)"),
            xaxis_title="",
            font=dict(color="white"),
            margin=dict(t=20, b=20),
        )
        st.plotly_chart(fig, use_container_width=True, theme=None)

    with col_bot_3:
        st.metric("Temps rotation moyen robot", temps_rotation_str)
