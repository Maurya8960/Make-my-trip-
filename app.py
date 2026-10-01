import pandas as pd
import json

# Data loading paths
df_bookings = pd.read_csv("hotel_bookings.csv")
df_cancellations = pd.read_excel("cancellations.xlsx") # Ensure openpyxl is installed
df_customers = pd.read_csv("customers.csv")
df_hotels = pd.read_csv("hotels.csv")
df_support = pd.read_csv("support_tickets.csv")
df_refunds = pd.read_excel("refund_requests.xlsx")

with open("guest_complaints.json", "r") as f:
    guest_complaints = json.load(f)
