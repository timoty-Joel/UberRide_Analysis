import streamlit as st 
import pandas as pd
import plotly.express as px 
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Set the Page Title ---
st.set_page_config(page_title='Uber Analysis Visualization')

def convertTimeRange(Hour):
    if Hour >= 5 and Hour <= 12:
        return 'Morning'
    elif Hour > 12 and Hour <= 17:
        return 'Afternoon'
    elif Hour >= 18 and Hour <= 24: # This will correctly capture 18:00 - 23:59
        return 'Evenings'
    elif Hour >= 0 and Hour < 5:
        return 'LateNights'

# --- Load Data from CSV File ---
@st.cache_data()
def load_data():
    try:
        df = pd.read_csv("data/uber_cleaned.csv")
    except:
        st.error()
        return 0
    
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce')
    df['Hour'] = df['Time'].dt.hour
    df['Day'] = df['Date'].dt.day_name()
    df['Month'] = df['Date'].dt.month_name()
    df['time_range'] = df['Hour'].apply(convertTimeRange)
    
    df_completed = df[df['Booking Status'] == 'Completed'].copy()
    
    return df, df_completed

df, df_completed = load_data()

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
        fig_vehicle.update_layout(
            xaxis=dict(title="Vehicle Type"), # Using 'xaxis'
            yaxis=dict(title="Total Number of Rides")
        )
        st.plotly_chart(fig_vehicle, use_container_width=True)
        
with tab2:
    st.header("Temporal Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Rides by Hour of The Day")
        hourly_counts = df_completed['Hour'].value_counts().sort_index()
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
        daily_counts = df['Day'].value_counts()
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
        
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Rides by Month")
        
        month_counts = df_completed['Month'].value_counts()
        month_order = ["January", "February", "March", "April", "May", "June", "July", "August",
                       "September", "October", "November", "December"]
        
        month_counts = month_counts.reindex(month_order)
        fig_month = px.bar(
            month_counts,
            x=month_counts.index,
            y=month_counts.values,
            title="Total Rides per Month",
            labels={'x':'Month', 'y':'Number of Rides'}
        )
        st.plotly_chart(fig_month, use_container_width=True)
    
    with col4:
        st.subheader("Rides by Time Range")
        timerange_counts = df_completed['time_range'].value_counts()
        timerange_order = ['Morning', 'Afternoon', 'Evenings', 'LateNights']
        timerange_counts = timerange_counts.reindex(timerange_order)
        
        fig_timerange = px.bar(
            timerange_counts,
            x=timerange_counts.index,
            y=timerange_counts.values,
            title="Total Rides by Time Range",
            labels={'x':'Time Range', 'y':'Number of Rides'}
        )
        st.plotly_chart(fig_timerange, use_container_width=True)

    st.divider()
    st.subheader("Successful Rides and Success Rate by Hour of Day")

    # --- Data Prep (from your code) ---
    # 1. Successful Bookings
    hourly_bookings = (
        df_completed.groupby('Hour')
        .size()
        .reset_index(name='Successful Bookings')
    )
    # Ensure all 24 hours are present
    all_hours_df = pd.DataFrame({'Hour': range(24)})
    hourly_bookings = pd.merge(all_hours_df, hourly_bookings, on='Hour', how='left').fillna(0)

    # 2. Success Rate
    success_by_hour = (
        df.groupby(['Hour', 'Booking Status'])
        .size()
        .reset_index(name='Count')
    )
    success_pivot = success_by_hour.pivot(index='Hour', columns='Booking Status', values='Count').fillna(0)
    # Ensure all 24 hours are in the index
    success_pivot = success_pivot.reindex(range(24), fill_value=0)

    if 'Completed' in success_pivot.columns and not success_pivot.sum(axis=1).eq(0).all():
        # Calculate rate, handle division by zero (where sum is 0) by resulting in NaN
        success_pivot['Success Rate (%)'] = (success_pivot['Completed'] / success_pivot.sum(axis=1)) * 100
    else:
        success_pivot['Success Rate (%)'] = 0
        
    # Convert any NaN (from 0/0) or Inf to 0
    success_pivot['Success Rate (%)'] = success_pivot['Success Rate (%)'].fillna(0)

    # 3. Merge
    merged_df = pd.merge(
        hourly_bookings, 
        success_pivot[['Success Rate (%)']], 
        left_on='Hour', 
        right_index=True, 
        how='outer'
    ).fillna(0)

    fig_combo_plotly = make_subplots(specs=[[{"secondary_y": True}]])

    fig_combo_plotly.add_trace(
        go.Bar(
            x=merged_df['Hour'],
            y=merged_df['Successful Bookings'],
            name='Successful Bookings',  # This name appears in the legend
            marker_color='royalblue'
        ),
        secondary_y=False,  # This is the primary y-axis
    )

    fig_combo_plotly.add_trace(
        go.Scatter(
            x=merged_df['Hour'],
            y=merged_df['Success Rate (%)'],
            name='Success Rate (%)',  # This name appears in the legend
            mode='lines+markers',
            line=dict(color='green', width=2.5),
            marker=dict(color='green')
        ),
        secondary_y=True,  # This is the secondary y-axis
    )

    fig_combo_plotly.update_layout(
        title_text='📊 Successful Rides and Success Rate by Hour of Day',
        title_font_size=20,
        xaxis=dict(
            title='Hour of Day (0-23)',
            tickmode='linear',  # Show all 24 hour ticks
            dtick=1
        ),
        yaxis=dict(
            title='Number of Successful Bookings',
            titlefont=dict(color='royalblue'),
            tickfont=dict(color='royalblue')
        ),
        yaxis2=dict(
            title='Success Rate (%)',
            titlefont=dict(color='green'),
            tickfont=dict(color='green'),
            range=[0, 100]  # Set range for percentage
        ),
        legend=dict(x=0, y=1.1, orientation='h'), # Move legend to the top
    )

    st.plotly_chart(fig_combo_plotly, use_container_width=True)

        
with tab3:
    st.header("Location and Vehicle Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Pickup Locations")
        top_pickup = df_completed['Pickup Location'].value_counts().nlargest(10).sort_values(ascending=True)
        fig_pickup = px.bar(
            top_pickup,
            y=top_pickup.index,
            x=top_pickup.values,
            orientation='h',
            title='Top 10 Pickup Locations',
            labels={'x':'Location', 'y':'Number of Rides'}
        )
        st.plotly_chart(fig_pickup, use_container_width=True)
        
    with col2:
        st.subheader("Top 10 Drop Locations")
        top_drops = df_completed['Drop Location'].value_counts().nlargest(10).sort_values(ascending=True)
        fig_drops = px.bar(
            top_drops,
            y=top_drops.index,
            x=top_drops.values,
            orientation='h',
            title="Top 10 Drop Location",
            labels={'x':'Location', 'y':'Number of Rides'}
        )
        st.plotly_chart(fig_drops, use_container_width=True)           
    
    st.divider()
    st.subheader("Booking Value Analysis by Vehicle")
    fig_box = px.box(
        df_completed,
        x='Vehicle Type',
        y='Booking Value',
        title="Distribution of Booking Value",
        labels={'x':'Vehicle Type', 'y':'Booking Value'}
    )
    st.plotly_chart(fig_box, use_container_width=True)
        
        
with tab4:
    st.header("Cancellation & Ratings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Driver Cancellation Reason")
        driver_cancel = df[df['Driver Cancellation Reason'] != 'Not Applicable']
        driver_cancel_counts = driver_cancel['Driver Cancellation Reason'].value_counts()
        
        fig_cancel_driver = px.bar(
            driver_cancel_counts,
            x=driver_cancel_counts.index,
            y=driver_cancel_counts.values,
            title="Top Reason for Driver Cancellation",
            labels={'x': 'Reason', 'y':'Counts'}
        )
        st.plotly_chart(fig_cancel_driver, use_container_width=True)
        
        
    with col2:
        st.subheader("Customer Cancellation Reason")
        cust_cancel = df[df['Reason for cancelling by Customer'] != 'Not Applicable']
        cust_cancel_counts = df['Reason for cancelling by Customer'].value_counts()
        
        fig_cancel_cust = px.bar(
            cust_cancel_counts,
            x=cust_cancel_counts.index,
            y=cust_cancel_counts.values,
            title="Top Reason for Customer Cancellation",
            labels={'x': 'Reason', 'y': 'Count'}
        )
        st.plotly_chart(fig_cancel_cust, use_container_width=True)
    
    st.divider()
    st.subheader("Rating Distributions (for Completed Rides)")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_driver_rating = px.histogram(
            df_completed,
            x='Driver Ratings',
            nbins=10,
            title="Driver Rating Distribution"
        )
        st.plotly_chart(fig_driver_rating, use_container_width=True)
        
    with col2:
        fig_cust_rating = px.histogram(
            df_completed,
            x='Customer Rating',
            nbins=10,
            title="Customer Rating Distribution"
        )
        st.plotly_chart(fig_cust_rating, use_container_width=True)
            
with tab5:
    st.header("Financial & Ride Details")
    
    st.subheader("Ride Distance vs. Booking Value")
    
    # Add a filter for this chart
    vehicle_choice = st.selectbox(
        "Filter by Vehicle Type:",
        options=['All'] + list(df_completed['Vehicle Type'].unique()),
        index=0
    )
    
    # Filter dataframe based on choice
    if vehicle_choice == 'All':
        plot_df = df_completed
    else:
        plot_df = df_completed[df_completed['Vehicle Type'] == vehicle_choice]
    
    # Scatter plot
    fig_scatter = px.scatter(
        plot_df,
        x='Ride Distance',
        y='Booking Value',
        title=f"Ride Distance vs. Booking Value for {vehicle_choice} Rides",
        labels={'x': 'Ride Distance (km)', 'y': 'Booking Value ($)'},
        hover_data=['Booking ID', 'Vehicle Type']
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.divider()
    st.subheader("Payment Method Usage")
    
    # Filter out "Not Applicable" for payment analysis
    payment_df = df[df['Payment Method'] != 'Not Applicable']
    payment_counts = payment_df['Payment Method'].value_counts()
    
    fig_payment = px.pie(
        payment_counts, 
        values=payment_counts.values, 
        names=payment_counts.index,
        title="Payment Method Popularity",
        hole=0.3
    )
    st.plotly_chart(fig_payment, use_container_width=True)