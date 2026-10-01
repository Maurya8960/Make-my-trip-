import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="MakeMyTrip Issue Analyzer", layout="wide")
st.title("🏨 MakeMyTrip Booking Cancellation & Guest Issue Analyzer")

# 1. Load Data
@st.cache_data
def load_data():
    bookings = pd.read_csv("hotel_bookings.csv")
    cancellations = pd.read_excel("cancellations.xlsx")
    customers = pd.read_csv("customers.csv")
    hotels = pd.read_csv("hotels.csv")
    support = pd.read_csv("support_tickets.csv")
    refunds = pd.read_excel("refund_requests.xlsx")
    with open("guest_complaints.json", "r") as f:
        complaints = json.load(f)
    return bookings, cancellations, customers, hotels, support, refunds, complaints

try:
    bookings, cancellations, customers, hotels, support, refunds, complaints = load_data()
    st.success("All datasets loaded successfully!")

    # 2. Key Metrics Row
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Bookings", len(bookings))
    col2.metric("Total Cancellations", len(cancellations))
    col3.metric("Support Tickets", len(support))

    # 3. Data Preview Tabs
    tab1, tab2, tab3 = st.tabs(["Bookings Data", "Cancellations", "Support Tickets"])
    with tab1:
        st.subheader("Hotel Bookings")
        st.dataframe(bookings.head(50))
    with tab2:
        st.subheader("Cancellations Overview")
        st.dataframe(cancellations.head(50))
    with tab3:
        st.subheader("Support Tickets Overview")
        st.dataframe(support.head(50))

except Exception as e:
    st.error(f"Error loading datasets: {e}")
    
