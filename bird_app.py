import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Bird Migration Exploratory Analysis App", layout="centered")

st.title("Bird Migration Exploratory Analysis App")
st.write(
    "Bu uygulama, kuş göçü veri seti üzerinden türlerin uçuş mesafelerini, hava koşullarını ve göç nedenlerini görselleştirir."
)

@st.cache_data
def load_data():
    return pd.read_csv("bird_migration_data.csv")

try:
    df = load_data()
    st.subheader("Veri Seti On Izleme")
    st.dataframe(df.head())

    st.subheader("Gorsellestirme Paneli")
    chart_type = st.selectbox(
        "Grafik Turunu Seciniz",
        ["Tur Ortalama Ucus Mesafesi", "Goc Nedenleri Dagilimi", "Sicaklik ve Ucus Mesafesi Iliskisi"]
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    if chart_type == "Tur Ortalama Ucus Mesafesi":
        sns.barplot(
            x="Species",
            y="Flight_Distance_km",
            data=df,
            palette="muted",
            estimator="mean",
            hue="Species",
            legend=False,
            ax=ax
        )
        ax.set_title("Average Flight Distance by Bird Species", fontsize=14, fontweight="bold")
        ax.set_xlabel("Species", fontsize=12)
        ax.set_ylabel("Average Flight Distance (km)", fontsize=12)
        plt.setp(ax.get_xticklabels(), rotation=45)
    elif chart_type == "Goc Nedenleri Dagilimi":
        sns.countplot(
            x="Migration_Reason",
            data=df,
            palette="Set2",
            order=df["Migration_Reason"].value_counts().index,
            ax=ax
        )
        ax.set_title("Distribution of Migration Reasons", fontsize=14, fontweight="bold")
        ax.set_xlabel("Migration Reason", fontsize=12)
        ax.set_ylabel("Count", fontsize=12)
        plt.setp(ax.get_xticklabels(), rotation=45)
    elif chart_type == "Sicaklik ve Ucus Mesafesi Iliskisi":
        sns.scatterplot(
            x="Temperature_C",
            y="Flight_Distance_km",
            hue="Weather_Condition",
            data=df.sample(500) if len(df) >= 500 else df,
            alpha=0.7,
            palette="tab10",
            ax=ax
        )
        ax.set_title("Temperature vs Flight Distance by Weather Condition", fontsize=14, fontweight="bold")
        ax.set_xlabel("Temperature (°C)", fontsize=12)
        ax.set_ylabel("Flight Distance (km)", fontsize=12)
        ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

    st.pyplot(fig)
except Exception as e:
    st.error(f"Veri yuklenirken veya gorsellestirilirken bir hata olustu: {e}")