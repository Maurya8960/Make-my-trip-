import streamlit as st
import pandas as pd
import json

# Page Configuration
st.set_page_config(page_title="MakeMyTrip Issue Analyzer", layout="wide")
st.title("🏨 MakeMyTrip Booking Cancellation & Guest Issue Analyzer")

# 1. Load Data
@st.cache_data
def load_data():
    bookings = pd.read_csv("hotel_bookings.csv")
    cancellations = pd.read_excel("cancellations.xlsx")
    support = pd.read_csv("support_tickets.csv")
    return bookings, cancellations, support

try:
    bookings, cancellations, support = load_data()
    st.sidebar.success("All datasets loaded successfully!")

    # 2. Sidebar Filters
    st.sidebar.header("🔍 Filter Data")
    hotel_list = ["All Hotels"] + list(bookings['hotel_id'].unique())
    selected_hotel = st.sidebar.selectbox("Select Hotel ID", hotel_list)

    # Apply Filter
    if selected_hotel != "All Hotels":
        bookings = bookings[bookings['hotel_id'] == selected_hotel]
        # Assuming cancellations might also have hotel_id
        if 'hotel_id' in cancellations.columns:
            cancellations = cancellations[cancellations['hotel_id'] == selected_hotel]

    # 3. Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Bookings", len(bookings))
    col2.metric("Total Cancellations", len(cancellations))
    col3.metric("Support Tickets", len(support))
    col4.metric("Total Revenue (INR)", f"₹ {bookings['booking_amount'].sum():,.2f}")

    # 4. Tabs for Charts and Data
    tab1, tab2 = st.tabs(["📊 Analytics & Charts", "📂 View Raw Data"])

    with tab1:
        st.subheader("📈 Daily Booking Trends")
        # Count bookings per date and plot line chart
        daily_bookings = bookings['booking_date'].value_counts().sort_index()
        st.line_chart(daily_bookings)

        st.markdown("---")
        
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            st.subheader("🏨 Top 5 Hotels by Bookings")
            top_hotels = bookings['hotel_id'].value_counts().head(5)
            st.bar_chart(top_hotels)
            
        with col_chart2:
            st.subheader("💰 Revenue by Top Hotels")
            hotel_revenue = bookings.groupby('hotel_id')['booking_amount'].sum().sort_values(ascending=False).head(5)
            st.bar_chart(hotel_revenue)

    with tab2:
        st.subheader("Hotel Bookings Data")
        st.dataframe(bookings)
        
        st.subheader("Cancellations Data")
        st.dataframe(cancellations)

except Exception as e:
    st.error(f"Error loading datasets: {e}")
    
