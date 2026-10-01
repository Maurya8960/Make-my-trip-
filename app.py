import streamlit as st
import pandas as pd
import numpy as np
import json
import time
import os

# ==========================================
# 1. PAGE CONFIG & FAVICON
# ==========================================
st.set_page_config(
    page_title="MMT CX Operations Hub",
    page_icon="✈️",
    layout="wide"
)

# ==========================================
# 2. macOS GLASSMORPHISM CSS INJECTION
# ==========================================
glass_css = """
<style>
/* Background gradient */
.stApp {
    background: radial-gradient(circle at 15% 20%, #1a1e2e 0%, #0d0f18 100%) !important;
    color: #e2e8f0;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", sans-serif;
}

/* Glass Cards for Metrics */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.04) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 16px 20px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
}

/* Glass Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(18, 22, 34, 0.6) !important;
    backdrop-filter: blur(25px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

/* Glass Tabs Container */
div[data-baseweb="tab-list"] {
    background: rgba(255, 255, 255, 0.03) !important;
    backdrop-filter: blur(16px) !important;
    border-radius: 14px !important;
    padding: 4px !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
}

/* Glass Buttons */
button[kind="primary"], div.stButton > button {
    background: rgba(255, 255, 255, 0.07) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
    transition: all 0.25s ease !important;
}

button[kind="primary"]:hover, div.stButton > button:hover {
    background: rgba(255, 255, 255, 0.15) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
}

/* macOS Window Bar Simulation */
.mac-window-bar {
    display: flex;
    gap: 8px;
    padding-bottom: 12px;
}
.mac-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    display: inline-block;
}
.dot-red { background: #ff5f56; }
.dot-yellow { background: #ffbd2e; }
.dot-green { background: #27c93f; }
</style>
"""
st.markdown(glass_css, unsafe_allow_html=True)

# ==========================================
# 3. LOGIN AUTHENTICATION
# ==========================================
def check_password():
    def password_entered():
        if st.session_state["password"] == "admin123":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("""
        <div class="mac-window-bar">
            <span class="mac-dot dot-red"></span>
            <span class="mac-dot dot-yellow"></span>
            <span class="mac-dot dot-green"></span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("### 🔒 Ops Hub Authentication")
        st.text_input("Enter Keycard Passcode (hint: admin123)", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown("### 🔒 Ops Hub Authentication")
        st.text_input("Enter Keycard Passcode", type="password", on_change=password_entered, key="password")
        st.error("Invalid credentials.")
        return False
    return True

if not check_password():
    st.stop()

# ==========================================
# 4. HEADER & LOGO
# ==========================================
st.markdown("""
<div class="mac-window-bar">
    <span class="mac-dot dot-red"></span>
    <span class="mac-dot dot-yellow"></span>
    <span class="mac-dot dot-green"></span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
    <h1 style="margin: 0; padding: 0; font-size: 2.2rem; color: white;">✈️ MakeMyTrip CX Recovery Hub</h1>
</div>
""", unsafe_allow_html=True)
st.caption("macOS Frosted Glass Terminal • Guest Intelligence & Escalation Engine")

# ==========================================
# 5. DATA ENGINE (Generate & Process)
# ==========================================
@st.cache_data
def load_and_process():
    # Generate Dummy Data if not exists
    if not os.path.exists('hotel_bookings.csv'):
        pd.DataFrame({
            'booking_id': [f'BKG{str(i).zfill(4)}' for i in range(1, 11)],
            'hotel_id': [f'HTL{np.random.randint(1, 5)}' for _ in range(10)],
            'booking_status': ['Cancelled', 'Confirmed', 'Cancelled', 'Confirmed', 'Cancelled', 'Cancelled', 'Confirmed', 'Cancelled', 'Confirmed', 'Cancelled'],
            'city': ['Goa', 'Mumbai', 'Delhi', 'Goa', 'Jaipur', 'Delhi', 'Goa', 'Mumbai', 'Jaipur', 'Goa'],
            'amount': [5000, 12000, 3000, 25000, 8000, 6000, 15000, 4500, 18000, 9000]
        }).to_csv('hotel_bookings.csv', index=False)
        
        pd.DataFrame({
            'booking_id': ['BKG0001', 'BKG0003', 'BKG0005', 'BKG0006', 'BKG0008', 'BKG0010'],
            'cancelled_by': ['Hotel', 'Guest', 'MMT Ops', 'Payment Partner', 'Guest', 'Hotel'], 
            'cancellation_reason': ['Overbooked', 'Change of plans', 'Fraud check', 'Payment failed', 'Medical', 'Check-in denied']
        }).to_excel('cancellations.xlsx', index=False)
        
        pd.DataFrame({
            'booking_id': ['BKG0001', 'BKG0005', 'BKG0008', 'BKG0010'],
            'refund_status': ['Pending', 'Failed', 'Completed', 'Pending'], 
            'requested_amount': [5000, 8000, 3500, 9000]
        }).to_excel('refund_requests.xlsx', index=False)
        
        with open('guest_complaints.json', 'w') as f:
            json.dump([
                {'complaint_id': 'CMP1', 'booking_id': 'BKG0001', 'sentiment': 'Angry', 'complaint_text': 'Reached hotel, they said no rooms available!'},
                {'complaint_id': 'CMP2', 'booking_id': 'BKG0010', 'sentiment': 'Frustrated', 'complaint_text': 'Where is my money? Check-in denied.'}
            ], f)
            
        pd.DataFrame({
            'booking_id': ['BKG0001', 'BKG0010'],
            'escalation_flag': [False, True]
        }).to_csv('support_tickets.csv', index=False)
        
        pd.DataFrame({'hotel_id': [f'HTL{i}' for i in range(1, 6)], 'hotel_name': ['Sea View', 'Taj', 'Marriott', 'Oyo', 'Hyatt']}).to_csv('hotels.csv', index=False)

    # Load Data
    df_bookings = pd.read_csv('hotel_bookings.csv')
    df_hotels = pd.read_csv('hotels.csv')
    df_cancels = pd.read_excel('cancellations.xlsx')
    df_refunds = pd.read_excel('refund_requests.xlsx')
    df_tickets = pd.read_csv('support_tickets.csv')
    with open('guest_complaints.json', 'r') as f:
        df_complaints = pd.DataFrame(json.load(f))

    # Clean & Aggregate
    df_bookings['booking_status'] = df_bookings['booking_status'].str.lower()
    df_refunds['refund_status'] = df_refunds['refund_status'].str.lower()
    df_cancels['cancelled_by'] = df_cancels['cancelled_by'].str.lower()
    
    complaints_agg = df_complaints.groupby('booking_id').agg(
        is_angry=('sentiment', lambda x: any(x.str.lower().isin(['angry', 'frustrated', 'negative', 'check-in denied']))),
        complaint_desc=('complaint_text', lambda x: " | ".join(x))
    ).reset_index()
    
    tickets_agg = df_tickets.groupby('booking_id').agg(
        is_escalated=('escalation_flag', 'max')
    ).reset_index()

    master = df_bookings.merge(df_hotels[['hotel_id', 'hotel_name']], on='hotel_id', how='left') \
                        .merge(df_cancels[['booking_id', 'cancelled_by', 'cancellation_reason']], on='booking_id', how='left') \
                        .merge(df_refunds[['booking_id', 'refund_status', 'requested_amount']], on='booking_id', how='left') \
                        .merge(complaints_agg, on='booking_id', how='left') \
                        .merge(tickets_agg, on='booking_id', how='left')

    master.fillna({'is_angry': False, 'is_escalated': False, 'refund_status': 'none'}, inplace=True)

    # Priority Scoring Engine
    def score_issue(row):
        score = 0
        reasons = []
        if row['booking_status'] == 'cancelled' and row['cancelled_by'] in ['hotel', 'mmt ops', 'payment partner']:
            score += 3; reasons.append(f"Partner Cancel ({row['cancellation_reason']})")
        if row['refund_status'] in ['pending', 'failed']:
            score += 4; reasons.append(f"Refund {row['refund_status'].title()}")
        if row['is_angry']: score += 3; reasons.append("Severe Guest Complaint")
        if row['is_escalated']: score += 3; reasons.append("Escalated Support Ticket")
        
        if score >= 6: return 'Critical', 'Direct Call & Manual Refund', " | ".join(reasons)
        elif score >= 3: return 'High', 'Hotel Penalty & Priority Tracking', " | ".join(reasons)
        elif row['booking_status'] == 'cancelled': return 'Medium', 'Standard Cancellation', "Routine Cancel"
        return 'Low', 'No Action', 'Normal'

    priority_logic = master.apply(score_issue, axis=1, result_type='expand')
    master['priority'] = priority_logic[0]
    master['recommended_action'] = priority_logic[1]
    master['issue_flags'] = priority_logic[2]
    
    return master[master['priority'].isin(['Critical', 'High', 'Medium'])].copy()

triage_queue = load_and_process()

# ==========================================
# 6. SIDEBAR & KPI GLASS TILES
# ==========================================
st.sidebar.markdown("### 🎛️ Control Center")
filter_priority = st.sidebar.multiselect("Priority Tier:", ['Critical', 'High', 'Medium'], default=['Critical', 'High', 'Medium'])
filter_city = st.sidebar.selectbox("Region Search:", ['All'] + list(triage_queue['city'].dropna().unique()))

filtered_df = triage_queue.copy()
if filter_priority:
    filtered_df = filtered_df[filtered_df['priority'].isin(filter_priority)]
if filter_city != 'All':
    filtered_df = filtered_df[filtered_df['city'] == filter_city]

pending_refunds_df = filtered_df[filtered_df['refund_status'] == 'pending']
financial_risk = pending_refunds_df['amount'].sum()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Critical Guest Issues", (filtered_df['priority'] == 'Critical').sum())
k2.metric("Actionable Cancellations", len(filtered_df))
k3.metric("Pending Refunds", len(pending_refunds_df))
k4.metric("Capital at Risk", f"₹{financial_risk:,.2f}")
st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 7. TABS INTERFACE
# ==========================================
tab1, tab2, tab3 = st.tabs(["⚡ Live CX Triage Queue", "🏨 Hotel Partner Diagnostics", "💬 Guest Resolution AI Hub"])

with tab1:
    st.subheader("Actionable Guest Recovery Registry")
    display_cols = ['booking_id', 'hotel_name', 'city', 'priority', 'issue_flags', 'refund_status', 'recommended_action']
    st.dataframe(filtered_df[display_cols], use_container_width=True, height=360)
    
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Recovery Report (CSV)", data=csv_data, file_name='mmt_cx_triage.csv', mime='text/csv')

with tab2:
    st.subheader("Hotel Partner Friction & Cancelation Zones")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Top Hotels Denying Check-ins / Cancelling**")
        if not filtered_df.empty:
            st.bar_chart(filtered_df['hotel_name'].value_counts().head(5), color="#ff4b4b")
        else:
            st.info("No hotel friction data for current filters.")
    with col2:
        st.markdown("**High-Risk Stay Cities**")
        if not filtered_df.empty:
            st.bar_chart(filtered_df['city'].value_counts().head(5), color="#ffa500")

with tab3:
    st.subheader("Smart Guest Resolution Hub")
    if not filtered_df.empty:
        selected_booking = st.selectbox("Select Target Booking:", filtered_df['booking_id'].tolist()[:40])
        row = filtered_df[filtered_df['booking_id'] == selected_booking].iloc[0]
        
        with st.expander(f"Context Capsule — {selected_booking}", expanded=True):
            st.markdown(f"**Customer Issue Context:** {row.get('complaint_desc', 'None logged')}")
            st.markdown(f"**Trigger Flags:** `{row['issue_flags']}` | **Action:** `{row['recommended_action']}`")
            
            if st.button("📱 Dispatch Emergency Refund & Apology", type="primary"):
                with st.spinner("Dispatching payment gateway payload..."):
                    time.sleep(1.5)
                st.toast(f"Refund prioritized for {selected_booking}", icon="💸")
                st.success("Automated apology and refund tracking link dispatched to guest.")
        
        st.markdown("**Copy Prompt to CX Assistant:**")
        prompt_text = f"Booking ID: {row['booking_id']} | Hotel: {row['hotel_name']} | City: {row['city']}\nIssue: {row['issue_flags']}\nAction taken: {row['recommended_action']}\n\nDraft a highly empathetic hotel cancellation apology email to the guest, assuring them of a priority refund processing."
        st.text_area("Prompt:", value=prompt_text, height=120)
    else:
        st.info("No records match the active filters.")