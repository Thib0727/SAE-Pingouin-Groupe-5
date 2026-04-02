"""
Dashboard J'EléFan - Application Streamlit
Groupe 5 QLIO - Dashboard industriel connecté à la BDD exploit (mes4)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import hashlib

# ─────────────────────────────────────────────
#  Configuration de la page
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="J'EléFan – Dashboard",
    page_icon="🍐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS Global (thème maquette)
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Palette ─────────────────────────── */
:root {
    --bg-main:     #1e1c35;
    --bg-sidebar:  #2a2845;
    --bg-card:     #38365a;
    --bg-card2:    #302e52;
    --accent-cyan: #26c6da;
    --accent-yellow: #fdd835;
    --accent-green:  #43a047;
    --accent-red:    #e53935;
    --accent-orange: #fb8c00;
    --text-light:  #e8e6ff;
    --text-muted:  #9e9cbf;
    --border:      #4a4870;
}

/* ── Fond principal ───────────────────── */
[data-testid="stAppViewContainer"] {
    background-color: var(--bg-main);
    color: var(--text-light);
}
[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar);
    border-right: 1px solid var(--border);
}
[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }

/* ── Titres ───────────────────────────── */
h1, h2, h3, h4 { color: var(--text-light) !important; }

/* ── Onglets navigation ───────────────── */
[data-testid="stTabs"] [role="tab"] {
    background-color: var(--bg-card2);
    color: var(--text-muted);
    border-radius: 6px 6px 0 0;
    font-weight: 600;
    padding: 8px 20px;
    border: 1px solid var(--border);
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background-color: var(--bg-card);
    color: var(--text-light) !important;
    border-bottom: 2px solid var(--accent-cyan);
}

/* ── Cartes KPI ───────────────────────── */
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 22px;
    text-align: center;
    margin-bottom: 12px;
}
.kpi-label { color: var(--text-muted); font-size: 0.85rem; margin-bottom: 6px; }
.kpi-value { color: var(--text-light); font-size: 1.6rem; font-weight: 700; }

/* ── Inputs sidebar ───────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stDateInput"] input {
    background-color: var(--bg-card) !important;
    color: var(--text-light) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
}
[data-testid="stSelectbox"] > div > div {
    background-color: var(--bg-card) !important;
    color: var(--text-light) !important;
    border: 1px solid var(--border) !important;
}

/* ── Boutons ──────────────────────────── */
[data-testid="stButton"] button {
    background-color: var(--accent-green);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 20px;
}
[data-testid="stButton"] button:hover { opacity: 0.85; }
.btn-logout button {
    background-color: var(--accent-red) !important;
}

/* ── Dernière MAJ sidebar ─────────────── */
.update-box {
    background-color: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 0.82rem;
    color: var(--text-muted);
    margin-bottom: 14px;
}

/* ── Séparateur ───────────────────────── */
hr { border-color: var(--border); }

/* ── Page de connexion ────────────────── */
.auth-container {
    max-width: 480px;
    margin: 40px auto;
    background: #f5f5f5;
    border-radius: 12px;
    padding: 32px 36px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.auth-tab-active   { font-weight: 700; color: #333; }
.auth-tab-inactive { color: #888; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Configuration BDD  ← MODIFIER ICI
# ─────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",   # ou IP du serveur
    "port":     3306,
    "database": "exploit",
    "user":     "root",        # ← à adapter
    "password": "password",    # ← à adapter
}

# Compte admin par défaut (hash SHA-256)
DEFAULT_USERS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
}


# ─────────────────────────────────────────────
#  Connexion MySQL
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_connection():
    """Retourne une connexion MySQL persistante."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        st.error(f"❌ Impossible de se connecter à la BDD : {e}")
        return None


def run_query(sql: str, params=None) -> pd.DataFrame:
    """Exécute une requête SELECT et retourne un DataFrame."""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        if not conn.is_connected():
            conn.reconnect(attempts=3, delay=1)
        df = pd.read_sql(sql, conn, params=params)
        return df
    except Exception as e:
        st.warning(f"⚠️ Erreur requête : {e}")
        return pd.DataFrame()


# ─────────────────────────────────────────────
#  Requêtes SQL adaptées à la BDD exploit/mes4
#  ─────────────────────────────────────────────
#  Les noms de colonnes ci-dessous sont basés
#  sur la structure typique des tables MES.
#  Ajustez-les selon votre schéma réel.
# ─────────────────────────────────────────────

def get_last_update() -> str:
    df = run_query("SELECT MAX(TimeStamp) AS last FROM tblmachinereport")
    if not df.empty and df["last"].iloc[0]:
        return pd.to_datetime(df["last"].iloc[0]).strftime("%d/%m/%Y %H:%M")
    return datetime.now().strftime("%d/%m/%Y %H:%M")


# ── Onglet 1 : Performance industrielle ──────

def get_rotation_time() -> float:
    """Temps de rotation moyen en secondes (tblfinstep)."""
    df = run_query("""
        SELECT AVG(Duration) AS avg_duration
        FROM tblfinstep
        WHERE Duration IS NOT NULL
    """)
    if not df.empty:
        val = df["avg_duration"].iloc[0]
        return round(float(val), 1) if val else 0.0
    return 465.0   # valeur démo


def get_lead_time() -> str:
    """Lead Time moyen (tblorder : différence CreationDate / CompletionDate)."""
    df = run_query("""
        SELECT AVG(TIMESTAMPDIFF(MINUTE, CreationDate, CompletionDate)) AS avg_lt
        FROM tblorder
        WHERE CompletionDate IS NOT NULL AND CreationDate IS NOT NULL
    """)
    if not df.empty and df["avg_lt"].iloc[0]:
        minutes = int(df["avg_lt"].iloc[0])
        return f"{minutes // 60}h {minutes % 60:02d}"
    return "1h 30"   # valeur démo


def get_machine_report_series(metric_col: str) -> pd.DataFrame:
    """
    Récupère une métrique journalière depuis tblmachinereport.
    metric_col : nom de la colonne à agréger (ex: ElectricityKWh, AirM3, RobotArmMinutes...)
    """
    sql = f"""
        SELECT
            DATE(TimeStamp) AS jour,
            AVG(`{metric_col}`) AS valeur
        FROM tblmachinereport
        WHERE `{metric_col}` IS NOT NULL
        GROUP BY DATE(TimeStamp)
        ORDER BY jour
        LIMIT 5
    """
    df = run_query(sql)
    if df.empty:
        # Données démo si la colonne n'existe pas
        import random, math
        days = [f"Jour {i+1}" for i in range(5)]
        vals = [18 + math.sin(i)*6 + random.uniform(-2, 2) for i in range(5)]
        df = pd.DataFrame({"jour": days, "valeur": vals})
    else:
        df["jour"] = ["Jour " + str(i+1) for i in range(len(df))]
    return df


def get_assembly_time_series() -> pd.DataFrame:
    """Temps d'assemblage moyen par jour (tblfinstep)."""
    sql = """
        SELECT
            DATE(StartTime) AS jour,
            AVG(Duration)/60 AS valeur
        FROM tblfinstep
        WHERE Duration IS NOT NULL
        GROUP BY DATE(StartTime)
        ORDER BY jour
        LIMIT 5
    """
    df = run_query(sql)
    if df.empty:
        import math, random
        days = [f"Jour {i+1}" for i in range(5)]
        vals = [19 + math.sin(i*0.8)*7 + random.uniform(-1, 2) for i in range(5)]
        df = pd.DataFrame({"jour": days, "valeur": vals})
    else:
        df["jour"] = ["Jour " + str(i+1) for i in range(len(df))]
    return df


# ── Onglet 2 : Qualité production & service ──

def get_conformity(module_col: str) -> dict:
    """
    Taux de conformité depuis tblpartsreport.
    module_col : colonne booléenne ou statut (IsConform, Status, etc.)
    """
    sql = f"""
        SELECT
            SUM(CASE WHEN `{module_col}` = 1 THEN 1 ELSE 0 END) AS conforme,
            SUM(CASE WHEN `{module_col}` = 0 THEN 1 ELSE 0 END) AS non_conforme
        FROM tblpartsreport
    """
    df = run_query(sql)
    if not df.empty and (df["conforme"].iloc[0] or 0) + (df["non_conforme"].iloc[0] or 0) > 0:
        c  = int(df["conforme"].iloc[0] or 0)
        nc = int(df["non_conforme"].iloc[0] or 0)
        total = c + nc
        return {"conforme": round(c/total*100, 1), "non_conforme": round(nc/total*100, 1)}
    return {"conforme": 90.9, "non_conforme": 9.1}   # démo


def get_missing_parts_series() -> pd.DataFrame:
    """Pièces manquantes dans le module pick-by-light (tblbufferpos)."""
    sql = """
        SELECT
            DATE(TimeStamp) AS jour,
            SUM(CASE WHEN Quantity = 0 THEN 1 ELSE 0 END) AS valeur
        FROM tblbufferpos
        GROUP BY DATE(TimeStamp)
        ORDER BY jour
        LIMIT 5
    """
    df = run_query(sql)
    if df.empty:
        df = pd.DataFrame({
            "jour": [f"Jour {i+1}" for i in range(5)],
            "valeur": [0, 0, 2, 0, 1]
        })
    else:
        df["jour"] = ["Jour " + str(i+1) for i in range(len(df))]
    return df


def get_otif_series() -> pd.DataFrame:
    """OTIF : On Time / Late par jour (tblorder)."""
    sql = """
        SELECT
            DATE(CompletionDate) AS jour,
            SUM(CASE WHEN CompletionDate <= DueDate THEN 1 ELSE 0 END) AS on_time,
            SUM(CASE WHEN CompletionDate >  DueDate THEN 1 ELSE 0 END) AS late
        FROM tblorder
        WHERE CompletionDate IS NOT NULL
        GROUP BY DATE(CompletionDate)
        ORDER BY jour
        LIMIT 3
    """
    df = run_query(sql)
    if df.empty:
        df = pd.DataFrame({
            "jour": ["J1", "J2", "J3"],
            "on_time": [95, 90, 145],
            "late": [5, 12, 15],
        })
    else:
        df["jour"] = ["J" + str(i+1) for i in range(len(df))]
    return df


# ── Onglet 3 : Logistique flux & stock ───────

def get_stock_stats() -> dict:
    """Taux de remplissage et valeurs des magasins MP et PF."""
    # Magasin MP (Matières Premières) → tblbufferpos
    df_mp = run_query("""
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN Quantity > 0 THEN 1 ELSE 0 END) AS filled
        FROM tblbufferpos
    """)
    # Magasin PF (Produits Finis) → tblpalletpos
    df_pf = run_query("""
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN PalletID IS NOT NULL THEN 1 ELSE 0 END) AS filled
        FROM tblpalletpos
    """)

    def pct(df):
        if not df.empty and df["total"].iloc[0]:
            return round(df["filled"].iloc[0] / df["total"].iloc[0] * 100, 1)
        return 94.0

    # Valeurs stock : SUM(Quantity * Price) via jointure tblparts
    df_val_mp = run_query("""
        SELECT ROUND(SUM(bp.Quantity * p.Price), 0) AS valeur
        FROM tblbufferpos bp
        JOIN tblparts p ON bp.PNo = p.PNo
    """)
    df_val_pf = run_query("""
        SELECT ROUND(COUNT(*) * 120, 0) AS valeur
        FROM tblpalletpos
        WHERE PalletID IS NOT NULL
    """)

    def euro(df):
        if not df.empty and df["valeur"].iloc[0]:
            return int(df["valeur"].iloc[0])
        return 42000

    return {
        "tx_mp":  pct(df_mp),
        "tx_pf":  pct(df_pf),
        "val_mp": euro(df_val_mp),
        "val_pf": euro(df_val_pf),
    }


def get_robot_distance_series() -> pd.DataFrame:
    """Distance journalière parcourue par le robot (tblmachinereport)."""
    sql = """
        SELECT
            DATE(TimeStamp) AS jour,
            SUM(RobotDistance) AS valeur
        FROM tblmachinereport
        WHERE RobotDistance IS NOT NULL
        GROUP BY DATE(TimeStamp)
        ORDER BY jour
        LIMIT 5
    """
    df = run_query(sql)
    if df.empty:
        df = pd.DataFrame({
            "jour": [f"Jour {i+1}" for i in range(5)],
            "valeur": [19, 14, 10, 25, 13]
        })
    else:
        df["jour"] = ["Jour " + str(i+1) for i in range(len(df))]
    return df


# ─────────────────────────────────────────────
#  Helpers graphiques Plotly
# ─────────────────────────────────────────────
PLOT_BG    = "#2a2845"
PAPER_BG   = "#2a2845"
FONT_COLOR = "#e8e6ff"
GRID_COLOR = "#3a3860"


def line_chart(df: pd.DataFrame, x: str, y: str, title: str,
               color: str = "#26c6da", y_label: str = "") -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x], y=df[y],
        mode="lines+markers",
        line=dict(color=color, width=2),
        marker=dict(color=color, size=7),
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(color=FONT_COLOR, size=14), x=0.5),
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR),
        xaxis=dict(gridcolor=GRID_COLOR, title=""),
        yaxis=dict(gridcolor=GRID_COLOR, title=y_label, rangemode="tozero"),
        margin=dict(l=40, r=20, t=50, b=30),
        height=260,
    )
    return fig


def pie_chart(conforme: float, non_conforme: float, title: str) -> go.Figure:
    fig = go.Figure(go.Pie(
        labels=["Conforme", "Non conforme"],
        values=[conforme, non_conforme],
        marker=dict(colors=["#26c6da", "#fb8c00"]),
        textinfo="label+percent",
        textfont=dict(color=FONT_COLOR, size=12),
        hole=0.0,
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(color=FONT_COLOR, size=14), x=0.5),
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR),
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
        height=280,
    )
    return fig


def bar_chart_otif(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(name="On time", x=df["jour"], y=df["on_time"],
                         marker_color="#26c6da"))
    fig.add_trace(go.Bar(name="Late",    x=df["jour"], y=df["late"],
                         marker_color="#fdd835"))
    fig.update_layout(
        title=dict(text="OTIF", font=dict(color=FONT_COLOR, size=14), x=0.5),
        barmode="group",
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR),
        xaxis=dict(gridcolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, rangemode="tozero"),
        legend=dict(font=dict(color=FONT_COLOR)),
        margin=dict(l=40, r=20, t=50, b=30),
        height=280,
    )
    return fig


# ─────────────────────────────────────────────
#  Authentification (Session State)
# ─────────────────────────────────────────────
def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


def login_page():
    """Affiche la page de connexion / inscription."""
    # Centrage via colonnes
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div style='text-align:center; margin-bottom:24px;'>
            <span style='font-size:3rem;'>🍐</span>
            <h2 style='color:#e8e6ff; margin:0;'>J'EléFan</h2>
        </div>
        """, unsafe_allow_html=True)

        tab_conn, tab_insc = st.tabs(["🔑 Connexion", "📝 Inscription"])

        with tab_conn:
            username = st.text_input("Nom d'utilisateur", key="login_user")
            password = st.text_input("Mot de passe", type="password", key="login_pw")
            if st.button("Valider", key="btn_login"):
                users = st.session_state.get("users", DEFAULT_USERS)
                if username in users and users[username] == hash_pw(password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Identifiant ou mot de passe incorrect.")

        with tab_insc:
            new_user = st.text_input("Nom d'utilisateur", key="reg_user")
            new_pw   = st.text_input("Mot de passe", type="password", key="reg_pw")
            new_pw2  = st.text_input("Confirmer le mot de passe", type="password", key="reg_pw2")
            if st.button("Valider", key="btn_register"):
                if not new_user or not new_pw:
                    st.warning("Remplissez tous les champs.")
                elif new_pw != new_pw2:
                    st.error("Les mots de passe ne correspondent pas.")
                else:
                    users = st.session_state.get("users", dict(DEFAULT_USERS))
                    if new_user in users:
                        st.warning("Cet utilisateur existe déjà.")
                    else:
                        users[new_user] = hash_pw(new_pw)
                        st.session_state.users = users
                        st.success(f"Compte « {new_user} » créé ! Connectez-vous.")


# ─────────────────────────────────────────────
#  Dashboard principal
# ─────────────────────────────────────────────
def dashboard():
    # ── Sidebar ──────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding:10px 0 20px;'>
            <span style='font-size:2.5rem;'>🍐</span>
            <div style='color:#e8e6ff; font-size:1.1rem; font-weight:700;'>J'EléFan</div>
        </div>
        """, unsafe_allow_html=True)

        last_update = get_last_update()
        st.markdown(f"""
        <div class='update-box'>
            <b>Dernière actualisation des données :</b><br>
            {last_update}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Filtres**")
        filtre1 = st.selectbox("Filtre 1 :", ["Tous", "Ligne A", "Ligne B", "Ligne C"], key="f1")
        filtre2 = st.selectbox("Filtre 2 :", ["Tous", "Équipe Matin", "Équipe Après-midi"], key="f2")

        st.markdown("**Période**")
        col_d, col_f = st.columns(2)
        with col_d:
            date_debut = st.date_input("De", value=datetime.now() - timedelta(days=7),
                                       label_visibility="visible", key="date_from")
        with col_f:
            date_fin = st.date_input("À", value=datetime.now(),
                                     label_visibility="visible", key="date_to")

        st.markdown("---")
        st.markdown(f"👤 **{st.session_state.get('username', 'Utilisateur')}**")
        if st.button("🚪 Se déconnecter", key="logout"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.rerun()

    # ── Navigation (3 onglets) ────────────────
    tab1, tab2, tab3 = st.tabs([
        "🏭  Performance industrielle",
        "✅  Qualité production & service",
        "📦  Logistique flux & stock",
    ])

    # ════════════════════════════════════════
    # TAB 1 : Performance industrielle
    # ════════════════════════════════════════
    with tab1:
        rot = get_rotation_time()
        lt  = get_lead_time()

        k1, k2, _ = st.columns([1, 1, 2])
        with k1:
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-label'>Temps de rotation moyen</div>
                <div class='kpi-value'>{rot} secondes</div>
            </div>
            """, unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-label'>Lead Time moyen</div>
                <div class='kpi-value'>{lt}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")
        col_a, col_b = st.columns(2)

        with col_a:
            df_air = get_machine_report_series("AirM3")
            st.plotly_chart(
                line_chart(df_air, "jour", "valeur",
                           "Consommation d'air comprimé", "#26c6da"),
                use_container_width=True, key="chart_air"
            )
        with col_b:
            df_asm = get_assembly_time_series()
            st.plotly_chart(
                line_chart(df_asm, "jour", "valeur",
                           "Temps d'assemblage moyen", "#26c6da", "Minutes"),
                use_container_width=True, key="chart_asm"
            )

        col_c, col_d = st.columns(2)
        with col_c:
            df_elec = get_machine_report_series("ElectricityKWh")
            st.plotly_chart(
                line_chart(df_elec, "jour", "valeur",
                           "Consommation d'électricité", "#fdd835", "Kwh"),
                use_container_width=True, key="chart_elec"
            )
        with col_d:
            df_robot = get_machine_report_series("RobotArmMinutes")
            st.plotly_chart(
                line_chart(df_robot, "jour", "valeur",
                           "Temps d'utilisation du bras robotisé", "#26c6da", "Minutes"),
                use_container_width=True, key="chart_robot"
            )

    # ════════════════════════════════════════
    # TAB 2 : Qualité production & service
    # ════════════════════════════════════════
    with tab2:
        col_a, col_b = st.columns(2)

        with col_a:
            # Conformité module d'assemblage
            c_asm = get_conformity("IsAssemblyConform")
            st.plotly_chart(
                pie_chart(c_asm["conforme"], c_asm["non_conforme"],
                          "Conformité module d'assemblage"),
                use_container_width=True, key="pie_asm"
            )
        with col_b:
            # Nombre pièces manquantes pick-by-light
            df_miss = get_missing_parts_series()
            st.plotly_chart(
                line_chart(df_miss, "jour", "valeur",
                           "Nombre pièces manquantes mod pick by light",
                           "#26c6da", "Minutes"),
                use_container_width=True, key="chart_miss"
            )

        col_c, col_d = st.columns(2)
        with col_c:
            # Conformité module vérification visuelle
            c_vis = get_conformity("IsVisualConform")
            st.plotly_chart(
                pie_chart(c_vis["conforme"], c_vis["non_conforme"],
                          "Conformité module vérification visuelle"),
                use_container_width=True, key="pie_vis"
            )
        with col_d:
            df_otif = get_otif_series()
            st.plotly_chart(
                bar_chart_otif(df_otif),
                use_container_width=True, key="chart_otif"
            )

    # ════════════════════════════════════════
    # TAB 3 : Logistique flux & stock
    # ════════════════════════════════════════
    with tab3:
        stats = get_stock_stats()

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-label'>Taux remplissage moyen magasin MP</div>
                <div class='kpi-value'>{stats['tx_mp']}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-label'>Taux remplissage moyen magasin PF</div>
                <div class='kpi-value'>{stats['tx_pf']}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-label'>Valeur stock MP</div>
                <div class='kpi-value'>{stats['val_mp']:,} €</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-label'>Valeur stock PF</div>
                <div class='kpi-value'>{stats['val_pf']:,} €</div>
            </div>
            """, unsafe_allow_html=True)

        # Row 2 : jauges circulaires + graphique distance robot
        col_c, col_d, col_e = st.columns([1, 2, 1])

        with col_c:
            fig_gauge_mp = go.Figure(go.Indicator(
                mode="gauge+number",
                value=stats["tx_mp"],
                title={"text": "Taux remplissage<br>magasin MP", "font": {"color": FONT_COLOR}},
                number={"suffix": "%", "font": {"color": FONT_COLOR}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": FONT_COLOR},
                    "bar":  {"color": "#26c6da"},
                    "bgcolor": PLOT_BG,
                    "bordercolor": GRID_COLOR,
                },
            ))
            fig_gauge_mp.update_layout(
                paper_bgcolor=PAPER_BG, font=dict(color=FONT_COLOR),
                height=230, margin=dict(l=20, r=20, t=50, b=10)
            )
            st.plotly_chart(fig_gauge_mp, use_container_width=True, key="gauge_mp")

        with col_d:
            df_dist = get_robot_distance_series()
            st.plotly_chart(
                line_chart(df_dist, "jour", "valeur",
                           "Distance parcourue par le robot", "#fdd835", "Distance (m)"),
                use_container_width=True, key="chart_dist"
            )

        with col_e:
            fig_gauge_pf = go.Figure(go.Indicator(
                mode="gauge+number",
                value=stats["tx_pf"],
                title={"text": "Taux remplissage<br>magasin PF", "font": {"color": FONT_COLOR}},
                number={"suffix": "%", "font": {"color": FONT_COLOR}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": FONT_COLOR},
                    "bar":  {"color": "#26c6da"},
                    "bgcolor": PLOT_BG,
                    "bordercolor": GRID_COLOR,
                },
            ))
            fig_gauge_pf.update_layout(
                paper_bgcolor=PAPER_BG, font=dict(color=FONT_COLOR),
                height=230, margin=dict(l=20, r=20, t=50, b=10)
            )
            st.plotly_chart(fig_gauge_pf, use_container_width=True, key="gauge_pf")


# ─────────────────────────────────────────────
#  Point d'entrée principal
# ─────────────────────────────────────────────
def main():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "users" not in st.session_state:
        st.session_state.users = dict(DEFAULT_USERS)

    if st.session_state.authenticated:
        dashboard()
    else:
        login_page()


if __name__ == "__main__":
    main()
