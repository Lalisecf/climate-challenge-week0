import streamlit as st


HAS_MPL = False
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_MPL = True
except Exception:
    plt = None
    sns = None
    st.warning("Matplotlib/Seaborn unavailable — falling back to Plotly for charts.")
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd
import sys
import os


curr_dir = os.path.dirname(os.path.abspath(__file__))
if curr_dir not in sys.path:
    sys.path.insert(0, curr_dir)

from utils import load_data, summary_table, top_regions, run_anova, daily_average, filter_by_date

# Page configuration
st.set_page_config(
    page_title="Solar Farm Analytics | MoonLight Energy",
    layout="wide",
    initial_sidebar_state="expanded"
)

#  Custom CSS for better Look 
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
        color: #6c757d !important;
        font-weight: 600;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #212529 !important;
    }
    div[data-testid="stExpander"] {
        border: none !important;
        box-shadow: none !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent !important;
        border-radius: 4px 4px 0px 0px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        border-bottom: 2px solid #007bff !important;
        color: #007bff !important;
    }
    </style>
    """, unsafe_allow_html=True)

#  Global color Settings
COLORS = {"Benin": "#636EFA", "Sierra Leone": "#EF553B", "Togo": "#00CC96"}

# ── Header ───────────────────────────────────────────────────────────────────
col_title, col_logo = st.columns([4, 1])
with col_title:
    st.title("MoonLight Solar Potential Dashboard")
    st.markdown(
        "Welcome to the **Interactive Solar Analysis Hub**. Filter, explore, and compare "
        "solar irradiation data across West African territories."
    )

st.divider()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Dashboard Configuration")
    
    st.subheader("Region Selection")
    selected_countries = st.multiselect(
        "Select Countries to compare",
        options=["Benin", "Sierra Leone", "Togo"],
        default=["Benin", "Sierra Leone", "Togo"],
    )

    st.subheader("Metric Selection")
    selected_metric = st.selectbox(
        "Choose primary solar variable",
        options=["GHI", "DNI", "DHI"],
        index=0,
        help="GHI: Global Horizontal Irradiance, DNI: Direct Normal Irradiance, DHI: Diffuse Horizontal Irradiance"
    )

    st.subheader("Time Horizon")
    # Date range default based on data inspection (Aug 2021 - Aug 2022)
    start_init = datetime(2021, 8, 9)
    end_init = datetime(2022, 8, 9)
    
    date_range = st.slider(
        "Period Range",
        min_value=start_init,
        max_value=end_init,
        value=(start_init, end_init),
        format="MMM YYYY"
    )

    # Control how much data to load on startup. Loading full CSVs can be slow on cloud.
    full_load = st.checkbox("Load full dataset (may be slow on deployment)", value=False)

    st.divider()

#  Guard Logic 
if not selected_countries:
    st.error(" Please select at least one country to begin analysis.")
    st.stop()

#  Data Loading & Processing ────────────────────────────────────────────────
with st.spinner(" Harvesting solar data..."):
    try:
        # If `full_load` is False we only load a sampled subset for fast startup on cloud.
        df_raw = load_data(selected_countries, sample_only=not full_load)
        
        if df_raw.empty:
            st.error("The data pantry is empty! No files were found for the selected countries.")
            # Diagnostic info for debugging
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            data_dir = os.path.join(project_root, "data")
            st.write(f"**Diagnostic Path:** `{data_dir}`")
            if os.path.exists(data_dir):
                st.write(f"**Files found:** {os.listdir(data_dir)}")
            else:
                st.error("The `data/` directory does not even exist at that path!")
            st.stop()
            
        df = filter_by_date(df_raw, date_range[0].date(), date_range[1].date())
        # Reduced sampling for browser-side performance (prevents charts from getting 'stuck')
        df_viz_sample = df.sample(min(10000, len(df)), random_state=42) if len(df) > 10000 else df
    except Exception as e:
        st.error(f" **App Crash Report**: {e}")
        st.exception(e)
        st.stop()

# ── KPI Section ──────────────────────────────────────────────────────────────
st.subheader("Key Performance Indicators")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

avg_val = df[selected_metric].mean()
max_val = df[selected_metric].max()
count_rec = len(df)
top_country = df.groupby("Country")[selected_metric].mean().idxmax() if not df.empty else "N/A"

kpi1.metric(f"Avg {selected_metric}", f"{avg_val:.2f} W/m²")
kpi2.metric(f"Max {selected_metric}", f"{max_val:.1f} W/m²")
kpi3.metric("Data Points", f"{count_rec:,}")
kpi4.metric("Optimal Region", top_country)

# ── Main Dashboard Layout ────────────────────────────────────────────────────
tab_summary, tab_charts, tab_dist, tab_rankings = st.tabs([
    "Summary & Stats", "Time Series Explorer", "Distribution Analysis", "Regional Rankings"
])

# -- TAB 1: SUMMARY --
with tab_summary:
    st.markdown("### Descriptive Statistics")
    m_cols = ["GHI", "DNI", "DHI", "Tamb"]
    # Add Tamb if it exists
    cols_to_use = [c for c in m_cols if c in df.columns]
    stats = summary_table(df, cols_to_use)
    st.dataframe(stats)

    st.divider()
    col_anova, col_info = st.columns([1, 1])
    with col_anova:
        st.markdown(f"### ANOVA Test Results ({selected_metric})")
        anova = run_anova(df, selected_metric)
        c1, c2 = st.columns(2)
        c1.metric("F-Statistic", anova["f_stat"])
        c2.metric("p-value", f"{anova['p_value']:.4e}")
        
        if anova["p_value"] < 0.05:
            st.success(" **Significant Variance Detected**: Country choice significantly impacts solar harvest potential.")
        else:
            st.warning(" **No Significant Variance**: Solar potential is relatively uniform across selected regions.")
    
    with col_info:
        st.info("""
        **Methodology Note**: 
        - ANOVA (Analysis of Variance) tests if the means of different countries are significantly different.
        - P-value < 0.05 indicates we reject the null hypothesis of equal means.
        """)

# -- TAB 2: TIME SERIES --
with tab_charts:
    st.markdown(f"### Daily Average {selected_metric} Trend")
    daily = daily_average(df, selected_metric)
    
    fig_line = px.line(
        daily, 
        x="Timestamp", 
        y=selected_metric, 
        color="Country",
        color_discrete_map=COLORS,
        template="plotly_white",
        labels={"Timestamp": "Date", selected_metric: f"{selected_metric} (W/m²)"}
    )
    fig_line.update_layout(hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_line, use_container_width=True)

# -- TAB 3: DISTRIBUTION --
with tab_dist:
    st.markdown(f"### Variance & Distribution of {selected_metric}")
    
    col_box, col_hist = st.columns(2)
    
    with col_box:
        fig_box = px.box(
            df_viz_sample, 
            x="Country", 
            y=selected_metric, 
            color="Country",
            color_discrete_map=COLORS,
            template="plotly_white",
            points=False # Hide outliers for cleaner look
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col_hist:
        fig_hist = px.histogram(
            df_viz_sample, 
            x=selected_metric, 
            color="Country", 
            barmode="overlay",
            color_discrete_map=COLORS,
            template="plotly_white",
            nbins=50
        )
        st.plotly_chart(fig_hist, use_container_width=True)

# -- TAB 4: RANKINGS --
with tab_rankings:
    st.markdown(f"### Top Performing Regions for {selected_metric}")
    ranking = top_regions(df, metric=selected_metric, top_n=len(selected_countries))
    
    col_table, col_bar = st.columns([1, 2])
    
    with col_table:
        st.table(ranking)
        
    with col_bar:
        fig_bar = px.bar(
            ranking,
            x="Country",
            y=f"Average {selected_metric} (W/m²)",
            color="Country",
            text_auto='.1f',
            color_discrete_map=COLORS,
            template="plotly_white"
        )
        fig_bar.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(fig_bar, use_container_width=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.caption("Built with Streamlit · MoonLight Energy Solutions · 10 Academy Week 0")
