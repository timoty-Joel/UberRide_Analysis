# 🚖 Uber Ride Analytics Dashboard

📍 **Live Dashboard:** https://uberride-analysis.streamlit.app/  
📊 **Dataset:** https://www.kaggle.com/datasets/yashdevladdha/uber-ride-analytics-dashboard

---

## 📌 Project Overview

This project focuses on analyzing Uber ride data to uncover insights related to **demand & supply**, **revenue performance**, **customer behavior**, and **ride outcomes**.  
The results are visualized through an interactive **web-based analytics dashboard** built using **Streamlit**.

The dashboard helps answer key business questions, including:

- When and where is ride demand the highest?  
- Which vehicle types generate the most revenue?  
- What routes contribute the most to revenue?  
- How does ride distance correlate with booking value and cancellations?  
- What do customer and driver ratings reveal about service quality?

---

## 📊 Dashboard Features

### **1. Key Performance Indicators (KPIs)**
- Total rides  
- Percentage of completed rides  
- Average booking value  
- Total revenue  
- Average ride distance  
- Average customer rating  

---

### **2. Demand & Supply Insights**
- Ride trends over time (line chart)  
- Ride distribution by vehicle type  
- Day-of-week and hourly demand heatmap  

---

### **3. Revenue & Growth Analysis**
- Boxplot of booking value by vehicle type  
- Top 10 revenue-generating routes  
- Scatter relationship: ride distance vs booking value  

---

### **4. Customer & Driver Insights**
- Customer rating distribution  
- Driver rating distribution  
- Top cancellation reasons (pie chart)  

---

## 🛠️ Tech Stack

- **Python**
- **Pandas** for preprocessing
- **Plotly** for interactive visualizations
- **Streamlit** for dashboard development
- **Matplotlib / Seaborn** (optional for EDA)
- **Kaggle Dataset** as the data source

---

## 🗂️ Dataset Description

The dataset includes key fields such as:

- `Date`, `Time`
- `Vehicle Type`
- `Pickup Location`, `Drop Location`
- `Ride Distance`
- `Booking Value`
- `Customer Rating`, `Driver Ratings`
- `Booking Status`
- Cancellation reasons (from both customer and driver)

---

## 🚀 Live Dashboard

You can explore the deployed dashboard here:

👉 **https://uberride-analysis.streamlit.app/**

The dashboard includes interactive filters for:

- Date range  
- Vehicle type  
- Booking status  
- Payment method  

Allowing users to explore the data dynamically and intuitively.

---
