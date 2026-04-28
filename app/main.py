import streamlit as st
import plotly.express as px
from datetime import datetime
import os
import sys

curr_dir = os.path.dirname(os.path.abspath(__file__))
if curr_dir not in sys.path:
    sys.path.insert(0, curr_dir)

from utils import load_data, summary_table, top_regions, run_anova, daily_average,monthly_average, filter_by_year

# Page config
st.set_page_config(page_title="Climate Dashboard", layout="wide")

st.title("🌍 Climate Data Dashboard")
st.markdown("Interactive analysis of temperature, precipitation, and humidity.")

# Sidebar
with st.sidebar:
    st.header("Configuration")

    selected_countries = st.multiselect(
        "Select Countries",
        ["Tanzania", "Kenya", "Sudan","Ethiopia","Nigeria"],
        default=["Tanzania", "Kenya", "Sudan","Ethiopia","Nigeria"]
    )

    selected_metric = st.selectbox(
        "Select Variable",
        ["Temperature", "Precipitation", "Humidity"]
    )


# Guard
if not selected_countries:
    st.warning("Select at least one country")
    st.stop()

# Load data
df = load_data(selected_countries)

if df.empty:
    st.error("No data found.")
    st.stop()

# ✅ NOW df exists → safe to use
min_year = df["Timestamp"].dt.year.min()
max_year = df["Timestamp"].dt.year.max()

year_range = st.slider(
    "Select Year Range",
    min_value=int(min_year),
    max_value=int(max_year),
    value=(int(min_year), int(max_year))
)

# Filter AFTER slider
df = filter_by_year(df, year_range[0], year_range[1])

# KPIs
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Average", f"{df[selected_metric].mean():.2f}")
col2.metric("Max", f"{df[selected_metric].max():.2f}")
col3.metric("Records", f"{len(df)}")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Summary",
    "Temperature Trend",
    "Precipitation Distribution",
    "Ranking"
])

# SUMMARY
with tab1:
    st.subheader("Statistics")
    stats = summary_table(df, ["Temperature", "Precipitation", "Humidity"])
    st.dataframe(stats)

    st.subheader("ANOVA Test")
    anova = run_anova(df, selected_metric)
    st.write(anova)

# TEMPERATURE TREND (REQUIRED)
with tab2:
    st.subheader("Temperature Trend")

    # df_temp = daily_average(df, "Temperature")

    # fig = px.line(
    #     df_temp,
    #     x="Timestamp",
    #     y="Temperature",
    #     color="Country"
    # )

    df_temp = monthly_average(df, "Temperature")

    fig = px.line(
        df_temp,
        x="Month",
        y="Temperature",
        color="Country"
    )
st.plotly_chart(fig, use_container_width=True)

# PRECIPITATION BOXPLOT (REQUIRED)
with tab3:
    st.subheader("Precipitation Distribution")

    fig = px.box(
        df,
        x="Country",
        y="Precipitation",
        color="Country"
    )

    st.plotly_chart(fig, use_container_width=True)

# RANKING
with tab4:
    st.subheader("Top Countries")

    ranking = top_regions(df, selected_metric)
    st.dataframe(ranking)

    fig = px.bar(ranking, x="Country", y=ranking.columns[1], color="Country")
    st.plotly_chart(fig, use_container_width=True)

st.caption("Built with Streamlit · 10 Academy Week 0")