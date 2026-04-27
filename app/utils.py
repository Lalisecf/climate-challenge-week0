import pandas as pd
from scipy import stats
import os
import streamlit as st


@st.cache_data
def load_data(countries, sample_only=True, sample_rows=10000):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_dir = os.path.join(project_root, "data")

    file_map = {
        "Tanzania": os.path.join(data_dir, "tanzania_clean.csv"),
        "Kenya": os.path.join(data_dir, "kenya_clean.csv"),
        "Sudan": os.path.join(data_dir, "sudan_clean.csv"),
        "Ethiopia": os.path.join(data_dir, "ethiopia_clean.csv"),
        "Nigeria": os.path.join(data_dir, "nigeria_clean.csv"),
    }

    frames = []

    for country in countries:
        path = file_map.get(country)

        if path and os.path.exists(path):
            df = pd.read_csv(path, nrows=sample_rows if sample_only else None)

            # ✅ Standardize columns
            df = df.rename(columns={
                "Date": "Timestamp",
                "T2M": "Temperature",
                "PRECTOTCORR": "Precipitation",
                "RH2M": "Humidity"
            })

            df["Timestamp"] = pd.to_datetime(df["Timestamp"])
            df["Country"] = country

            frames.append(df)

    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def daily_average(df, metric):
    if df.empty:
        return pd.DataFrame()

    return (
        df.groupby(["Timestamp", "Country"])[metric]
        .mean()
        .reset_index()
    )


def summary_table(df, metrics):
    agg = df.groupby("Country")[metrics].agg(["mean", "median", "std"]).round(2)
    agg.columns = [f"{col}_{stat}" for col, stat in agg.columns]
    return agg


def top_regions(df, metric="Temperature", top_n=3):
    ranked = (
        df.groupby("Country")[metric]
        .mean()
        .round(2)
        .sort_values(ascending=False)
        .reset_index()
    )
    ranked.columns = ["Country", f"Average {metric}"]
    return ranked.head(top_n)


def run_anova(df, metric="Temperature"):
    if df.empty:
        return {"f_stat": 0, "p_value": 1.0}

    groups = [df[df["Country"] == c][metric].dropna() for c in df["Country"].unique()]

    if len(groups) < 2:
        return {"f_stat": 0, "p_value": 1.0}

    f_stat, p_value = stats.f_oneway(*groups)
    return {"f_stat": round(f_stat, 4), "p_value": p_value}


def filter_by_year(df, start_year, end_year):
    if df.empty:
        return df

    return df[
        (df["Timestamp"].dt.year >= start_year) &
        (df["Timestamp"].dt.year <= end_year)
    ]