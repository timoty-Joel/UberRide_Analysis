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
    
    df_completed = df[df['Booking Status'] == 'Completed'].copy()
    
    return df, df_completed

df, df_completed = load_data()

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

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview & KPIs",
    "Temporal Analysis (Time)",
    "Location & Vehicle Analysis",
    "Service Quality",
    "Financial & Ride Details"
])

with tab1:
    st.header("Overall Service Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Rides/Orders: ", len(df))
    col2.metric("Completed Rides/Orders: ", len(df_completed))
    
    completion_rate = (df_completed.shape[0] / df.shape[0]) * 100
    col3.metric("Completion Rate ", f"{completion_rate:.2f}%")
    
    avg_rating = df_completed['Driver Ratings'].mean()
    col4.metric("Average Driver Ratings: ", f"{avg_rating:.2f}★")
    
    st.divider()
    
    # Charts for Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Booking Status Distribution")
        status_count = df['Booking Status'].value_counts()
        fig_status = px.pie(
            status_count,
            values=status_count.values,
            names=status_count.index,
            title="Proportion of All Booking Status",
            hole=0.3
        )
        
        fig_status.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_status, use_container_width=True)
        
    with col2:
        st.subheader("Vehicle Type Popularity")
        vehicle_counts = df['Vehicle Type'].value_counts()
        fig_vehicle = px.bar(
            vehicle_counts,
            x=vehicle_counts.index,
            y=vehicle_counts.values,
            title="Total Bookings by Vehicle Type",
            labels={'x':'Vehicle Type', 'y':'Number of Rides'}
        )
        fig_vehicle.update_layout(axis={'categoryorder':'total descending'})
        st.plotly_chart(fig_vehicle, use_container_width=True)
        
with tab2:
    st.header("Temporal Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Rides by Hour of The Day")
        hourly_counts = df['Hour'].value_counts().sort_index()
        fig_hourly = px.bar(
            hourly_counts,
            x=hourly_counts.index,
            y=hourly_counts.values,
            title="Peak Booking Hours",
            labels={'x':'Hour of Day (0-23)', 'y':'Number of Rides'}
        )
        st.plotly_chart(fig_hourly, use_container_width=True)
        
        
    with col2:
        st.subheader("Rides of The Week")
        daily_counts = df['day'].value_counts()
        week_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        daily_counts = daily_counts.reindex(week_order)
        fig_daily = px.bar(
            daily_counts,
            x=daily_counts.index,
            y=daily_counts.values,
            title="Peak Booking Days",
            labels={'x':'Days of Week', 'y':'Number of Rides'}
        )
        st.plotly_chart(fig_daily, use_container_width=True)
        
    with tab3:
        st.header("Location and Vehicle Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 10 Pickup Locations")
            top_drops = df['Drop Location'].value_counts().nlargest(10).sort_values(ascending=True)
            