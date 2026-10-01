import streamlit as st
import pandas as pd
import json
import plotly.express as px
from datetime import datetime

# --- Page Configuration & UI Styling ---
st.set_page_config(page_title="MakeMyTrip Issue Analyzer", page_icon="🏨", layout="wide")

# Custom CSS for better aesthetics
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    h1 { color: #FF5A5F; font-family: 'Arial', sans-serif; }
    h2, h3 { color: #E0E0E0; }
    .stMetric { background-color: #1E2127; padding: 15px; border-radius: 10px; border-left: 5px solid #FF5A5F; box-shadow: 2px 2px 10px rgba(0,0,0,0.5); }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #1E2127; border-radius: 5px 5px 0px 0px; padding: 10px 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏨 MakeMyTrip Booking Cancellation & Guest Issue Analyzer")
st.markdown("Analyze booking trends, track operational bottlenecks, and monitor guest satisfaction in real-time.")
st.markdown("---")

# --- 1. Load Data ---
@st.cache_data
def load_data():
    bookings = pd.read_csv("hotel_bookings.csv")
    cancellations = pd.read_excel("cancellations.xlsx")
    support = pd.read_csv("support_tickets.csv")
    
    # Ensuring date columns are datetime objects for filtering
    if 'booking_date' in bookings.columns:
        bookings['booking_date'] = pd.to_datetime(bookings['booking_date'])
        
    with open("guest_complaints.json", "r") as f:
        complaints = json.load(f)
    return bookings, cancellations, support, complaints

try:
    bookings, cancellations, support, complaints = load_data()

    # --- 2. Advanced Sidebar Filters ---
    st.sidebar.header("🔍 Interactive Filters")
    
    # Hotel Filter
    hotel_list = ["All Hotels"] + list(bookings['hotel_id'].unique())
    selected_hotel = st.sidebar.selectbox("🏢 Select Hotel ID", hotel_list)

    # Date Range Filter
    if 'booking_date' in bookings.columns:
        min_date = bookings['booking_date'].min().date()
        max_date = bookings['booking_date'].max().date()
        date_range = st.sidebar.slider(
            "📅 Select Booking Date Range",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date)
        )

    # --- Apply Filters ---
    filtered_bookings = bookings.copy()
    if selected_hotel != "All Hotels":
        filtered_bookings = filtered_bookings[filtered_bookings['hotel_id'] == selected_hotel]
    if 'booking_date' in bookings.columns:
         mask = (filtered_bookings['booking_date'].dt.date >= date_range[0]) & (filtered_bookings['booking_date'].dt.date <= date_range[1])
         filtered_bookings = filtered_bookings.loc[mask]
    
    # Filter cancellations based on bookings (Assuming booking_id links them)
    filtered_cancellations = cancellations[cancellations['booking_id'].isin(filtered_bookings['booking_id'])] if 'booking_id' in cancellations.columns else cancellations

    # --- 3. Advanced KPIs (Key Performance Indicators) ---
    st.subheader("📊 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    total_bookings = len(filtered_bookings)
    total_cancellations = len(filtered_cancellations)
    
    # KPI Logic
    cancellation_rate = (total_cancellations / total_bookings * 100) if total_bookings > 0 else 0
    total_revenue = filtered_bookings['booking_amount'].sum() if 'booking_amount' in filtered_bookings.columns else 0
    # Dummy calculation for revenue lost (assuming average ticket size if exact amount isn't in cancellations)
    avg_booking_val = total_revenue / total_bookings if total_bookings > 0 else 0
    revenue_lost = total_cancellations * avg_booking_val

    col1.metric("Total Bookings", f"{total_bookings:,}")
    col2.metric("Total Cancellations", f"{total_cancellations:,}", f"{cancellation_rate:.1f}% Rate", delta_color="inverse")
    col3.metric("Support Tickets", f"{len(support):,}")
    col4.metric("Revenue Lost (Est.)", f"₹ {revenue_lost:,.0f}", "- Impact", delta_color="inverse")

    st.markdown("---")

    # --- 4. Beautiful Tabs for Analysis ---
    tab1, tab2, tab3 = st.tabs(["📈 Trend Analysis", "😠 Guest Complaints (NLP)", "📂 Raw Data Explorer"])

    with tab1:
        st.subheader("Booking vs Cancellation Trends")
        col_chart1, col_chart2 = st.columns([2, 1])
        
        with col_chart1:
            # Monthly/Weekly aggregation for cleaner line chart
            if 'booking_date' in filtered_bookings.columns:
                trend_data = filtered_bookings.set_index('booking_date').resample('M').size().reset_index(name='Bookings')
                fig_line = px.line(trend_data, x='booking_date', y='Bookings', 
                                   title="Monthly Booking Trends", markers=True, 
                                   line_shape='spline', color_discrete_sequence=['#00CC96'])
                fig_line.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
                st.plotly_chart(fig_line, use_container_width=True)
            else:
                st.info("Date column missing for trend analysis.")

        with col_chart2:
            # Top Hotels Bar Chart
            top_hotels = filtered_bookings['hotel_id'].value_counts().head(5).reset_index()
            top_hotels.columns = ['Hotel ID', 'Bookings']
            fig_bar = px.bar(top_hotels, x='Hotel ID', y='Bookings', 
                             title="Top 5 Hotels", color='Bookings', color_continuous_scale='Reds')
            fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
            st.plotly_chart(fig_bar, use_container_width=True)

    with tab2:
        st.subheader("Root Cause Analysis: Why are guests unhappy?")
        
        # NLP/JSON Data Processing
        if complaints and len(complaints) > 0:
            # Extract categories from JSON (Assuming JSON is a list of dicts with a 'category' or 'issue_type' key)
            # If your JSON structure is different, this key might need adjustment
            try:
                # Let's try to find a common key like 'category', 'issue', 'type', or just count occurrences if it's a list of strings
                categories = []
                for c in complaints:
                    if isinstance(c, dict):
                        categories.append(c.get('category') or c.get('issue_type') or c.get('subject') or "Uncategorized")
                    elif isinstance(c, str):
                        # simple heuristic if it's just strings
                        if "clean" in c.lower(): categories.append("Cleanliness")
                        elif "staff" in c.lower(): categories.append("Staff Behavior")
                        elif "ac" in c.lower() or "room" in c.lower(): categories.append("Room Amenities")
                        else: categories.append("Other")
                
                complaint_df = pd.DataFrame(categories, columns=['Issue Type'])
                issue_counts = complaint_df['Issue Type'].value_counts().reset_index()
                issue_counts.columns = ['Issue Category', 'Count']

                col_pie1, col_pie2 = st.columns([1, 1])
                
                with col_pie1:
                    fig_pie = px.pie(issue_counts.head(5), values='Count', names='Issue Category', 
                                     title="Top 5 Complaint Categories", hole=0.4,
                                     color_discrete_sequence=px.colors.sequential.RdBu)
                    fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with col_pie2:
                    st.markdown("### Actionable Insights")
                    st.warning(f"🚨 **{issue_counts.iloc[0]['Issue Category']}** is the highest reported issue.")
                    st.info(f"💡 Reducing issues related to **{issue_counts.iloc[0]['Issue Category']}** could potentially decrease the cancellation rate by a significant margin.")
                    st.dataframe(issue_counts, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Could not parse complaint categories automatically. Please check JSON structure. Error: {e}")
        else:
            st.info("No complaint data available or JSON is empty.")

    with tab3:
        st.subheader("Raw Datasets")
        st.markdown("Explore the filtered data below.")
        st.write("### Bookings")
        st.dataframe(filtered_bookings.head(100), use_container_width=True)
        st.write("### Cancellations")
        st.dataframe(filtered_cancellations.head(100), use_container_width=True)

except Exception as e:
    st.error(f"Critical Error: {e}")
    st.info("Tip: Make sure all CSV, Excel, and JSON files are present in the repository and have the correct column names.")
