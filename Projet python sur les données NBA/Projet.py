# =====================================================================
# 📌 DASHBOARD INTERACTIF — ANALYSE DU JEU DE DONNÉES SPORTIF
# Auteur : Cephas 🔥
# Objectif : Explorer les statistiques d'équipes NBA
# =====================================================================

import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

st.set_page_config(page_title="Tableau de Bord Sportif Interactif", layout="wide")

# ============================
# 🔽 Chargement des données
# ============================
df = pd.read_csv("final_data.csv")

# Convertir la colonne MIN (format mm:ss) en minutes float

def convert_min_to_float(x):
    try:
        parts = str(x).split(":")
        minutes = int(parts[0])
        seconds = int(parts[1])
        return minutes + seconds / 60
    except:
        return None

df["MIN"] = df["MIN"].apply(convert_min_to_float)

# ============================
# 🏠 Page d'Accueil
# ============================
st.title("🏀 Tableau de Bord Interactif – Analyse Sportive")

st.write("""
Bienvenue dans ce dashboard interactif conçu pour **explorer les performances sportives**.

Tu peux filtrer, comparer, visualiser et analyser les statistiques en un clic.
""")

st.subheader("🔍 Aperçu du jeu de données brut")
st.dataframe(df.head(20))

st.write(f"📊 Nombre total de lignes : **{df.shape[0]}**")
st.write(f"📈 Nombre total de colonnes : **{df.shape[1]}**")

# ===============================================
# 🎛 FILTRES — saison + équipe
# ===============================================
st.sidebar.title("🎛 Filtres")

saisons = sorted(df["SEASON"].unique())
equipes = sorted(df["TEAM_NAME"].unique())

saison_filter = st.sidebar.selectbox("📅 Choisissez une saison", saisons)
equipe_filter = st.sidebar.selectbox("🏀 Choisissez une équipe", equipes)

# Filtrage
df_filtered = df.copy()
df_filtered = df_filtered[df_filtered["SEASON"] == saison_filter]
df_filtered = df_filtered[df_filtered["TEAM_NAME"] == equipe_filter]

st.subheader("📄 Données filtrées")
st.dataframe(df_filtered)
st.write(f"📊 Nombre de lignes après filtre : **{df_filtered.shape[0]}**")

# Bouton téléchargement CSV
st.download_button(
    label="📥 Télécharger les données filtrées",
    data=df_filtered.to_csv(index=False),
    file_name=f"stats_filtered.csv",
    mime="text/csv"
)

# ==================================================
# 📈 Graphique dynamique — Points par match
# ==================================================
if "PTS" in df_filtered.columns:
    st.subheader("📊 Points par match")
    fig = px.bar(df_filtered,
                 x="GAME_ID",
                 y="PTS",
                 color="TEAM_NAME",
                 title="Points par match",
                 text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# 🌐 Radar Stats — PTS / AST / REB
# ==================================================
if all(col in df_filtered.columns for col in ["PTS", "AST", "REB"]):
    st.subheader("🌐 Radar Stats Globales")

    radar_values = [
        df_filtered["PTS"].mean(),
        df_filtered["AST"].mean(),
        df_filtered["REB"].mean()
    ]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=radar_values,
        theta=["Points", "Assists", "Rebounds"],
        fill='toself',
        name=equipe_filter
    ))
    st.plotly_chart(fig_radar, use_container_width=True)

# ==================================================
# 📦 Répartition des points
# ==================================================
if "PTS" in df_filtered.columns:
    st.subheader("📦 Répartition des points")
    fig_box = px.box(df_filtered,
                     x="TEAM_NAME",
                     y="PTS",
                     color="TEAM_NAME",
                     points="all",
                     title="Distribution des points")
    st.plotly_chart(fig_box, use_container_width=True)

# ==================================================
# 🔥 Heatmap des corrélations
# ==================================================
st.subheader("🔥 Corrélations entre stats")
numeric_cols = df_filtered.select_dtypes(include='number').columns

if len(numeric_cols) >= 2:
    corr = df_filtered[numeric_cols].corr()
    fig_corr, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig_corr)

# ==================================================
# 🧠 Analyse automatique simple (version équipe)
# ==================================================
st.subheader("🧠 Analyse automatique")

if not df_filtered.empty:

    st.write(f"📌 **Moyenne Points : {df_filtered['PTS'].mean():.2f}**")
    st.write(f"📌 **Total Points de l'équipe : {df_filtered['PTS'].sum()}**")
    st.write(f"📌 **Moyenne Assists : {df_filtered['AST'].mean():.2f}**")
    st.write(f"📌 **Moyenne Rebounds : {df_filtered['REB'].mean():.2f}**")

else:
    st.warning("Aucune donnée pour ce filtre.")

# ==================================================
# 🔥 Conclusion
# ==================================================
st.markdown("---")
st.header("📄 Conclusion & Interprétation")

st.write("""
L'analyse met en avant les performances de l'équipe sélectionnée en fonction :
- des points,
- passes,
- rebonds,
- efficacité globale.

Les filtres permettent d'obtenir une vision claire et ciblée.
""")
