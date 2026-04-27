import pandas as pd
import numpy as np
from scipy import stats
import os
import streamlit as st

@st.cache_data
def load_data(countries: list[str], data_dir: str = None, sample_only: bool = True, sample_rows: int = 10000) -> pd.DataFrame:
  
  
    if data_dir is None:
      
      
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        data_dir = os.path.join(project_root, "data")
        
    file_map = {
        "Benin": os.path.join(data_dir, "benin_clean.csv"),
        "Sierra Leone": os.path.join(data_dir, "sierraleone_clean.csv"),
        "Togo": os.path.join(data_dir, "togo_clean.csv"),
    }
    
    # Only load columns required for the dashboard
    core_cols = ["Timestamp", "GHI", "DNI", "DHI", "Tamb"]
    dtype_dict = {col: "float32" for col in core_cols if col != "Timestamp"}

    frames = []
    for country in countries:
        path = file_map.get(country)
        if path:
            # Prefer Parquet if available (faster & smaller on disk)
            parquet_path = os.path.splitext(path)[0] + ".parquet"
            if os.path.exists(parquet_path):
                df = pd.read_parquet(parquet_path)
                # ensure required cols
                df = df[[c for c in core_cols if c in df.columns]]
                df["Country"] = country
                frames.append(df)
                continue

            if os.path.exists(path):
                # usecols significantly reduces initial load memory
                # sample_only loads only the first `sample_rows` to speed startup
                if sample_only:
                    df = pd.read_csv(path, usecols=core_cols, parse_dates=["Timestamp"], dtype=dtype_dict, nrows=sample_rows)
                else:
                    df = pd.read_csv(path, usecols=core_cols, parse_dates=["Timestamp"], dtype=dtype_dict)
                df["Country"] = country
                frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def daily_average(df: pd.DataFrame, metric: str) -> pd.DataFrame:
 
 
    if df.empty:
        return pd.DataFrame()
    
    # Process only relevant subset of data
    daily = (
        df[['Timestamp', 'Country', metric]]
        .set_index("Timestamp")
        .groupby("Country")[metric]
        .resample("D")
        .mean()
        .reset_index()
    )
    return daily


def summary_table(df: pd.DataFrame, metrics: list[str]) -> pd.DataFrame:
    """Return a summary table with mean, median, and std per country."""
    agg = df.groupby("Country")[metrics].agg(["mean", "median", "std"]).round(2)
    agg.columns = [f"{col}_{stat}" for col, stat in agg.columns]
    return agg


def top_regions(df: pd.DataFrame, metric: str = "GHI", top_n: int = 3) -> pd.DataFrame:
    """Return countries ranked by average of the given metric."""
    ranked = (
        df.groupby("Country")[metric]
        .mean()
        .round(2)
        .sort_values(ascending=False)
        .reset_index()
    )
    ranked.columns = ["Country", f"Average {metric} (W/m²)"]
    return ranked.head(top_n)


def run_anova(df: pd.DataFrame, metric: str = "GHI") -> dict:

    if df.empty:
        return {"f_stat": 0, "p_value": 1.0}
    
    groups = []
    unique_countries = df["Country"].unique()
    
    for country in unique_countries:
        country_data = df[df["Country"] == country][metric].dropna()
        # Sample if data is too large (over 100k points is overkill for ANOVA)
        if len(country_data) > 100000:
            country_data = country_data.sample(100000, random_state=42)
        groups.append(country_data.values)
    
    if len(groups) < 2:
        return {"f_stat": 0, "p_value": 1.0}
        
    f_stat, p_value = stats.f_oneway(*groups)
    return {"f_stat": round(f_stat, 4), "p_value": p_value}




def filter_by_date(df: pd.DataFrame, start_date, end_date) -> pd.DataFrame:
    """Filter the dataframe by a date range."""
    if df.empty:
        return df
    mask = (df["Timestamp"].dt.date >= start_date) & (df["Timestamp"].dt.date <= end_date)
    return df.loc[mask]
