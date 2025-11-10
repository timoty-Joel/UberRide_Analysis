import streamlit as st 
import pandas as pd
import plotly.express as px 

# --- Set the Page Title ---
st.set_page_config(page_title='Uber Analysis Visualization')

# --- Load Data from CSV File ---
@st.cache_data()
def load_data():
    df = pd.read_csv('/data/uber_cleaned.csv')
    df['date'] = pd.to_datetime('datetime')
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