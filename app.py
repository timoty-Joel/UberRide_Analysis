import streamlit as st 
import pandas as pd
import plotly.express as px 

# --- Set the Page Title ---
st.set_page_config(page_title='Uber Analysis Visualization')

# --- Load Data from CSV File ---
@st.cache_data()
def load_data():
    try:
        df = pd.read_csv("data/uber_cleaned.csv")
    except:
        st.error()
        return 0
    
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce').dt.time
    df['Day'] = df['Date'].dt.day_name()
    df['Month'] = df['Date'].dt.month_name()
    
    return df

df = load_data()

# ------------
# Sidebar Part
# ------------

sidebar = st.sidebar.header("Filters")

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['Date'].min(), df['Date'].max()]
)

vehicle_types = st.sidebar.multiselect(
    "Select Vehicle Type",
    options=df['Vehicle Type'].unique(),
    default=df['Vehicle Type'].unique()
)

df_filtered = df[
    (df['Date'].between(date_range[0], date_range[1])) &
    (df['Vehicle Type'].isin(vehicle_types))
]

# -----------------
# KPI Visualization
# -----------------

st.title("Uber Rides Analytic Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Rides: ", len(df_filtered['is_Completed']))