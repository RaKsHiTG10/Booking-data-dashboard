 
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "DataAnalyst_Assesment_Dataset.xlsx"
df = pd.read_excel(file_path, sheet_name="Large_Fake_Bookings_With_Discre")

df["Booking Date"] = pd.to_datetime(df["Booking Date"], errors='coerce')
df["Time Slot"] = pd.to_datetime(df["Time Slot"], format="%H:%M:%S", errors='coerce').dt.time
df["Facility"].fillna("Unknown", inplace=True)
df["Theme"].fillna("None", inplace=True)
df["Subscription Type"].fillna("Not Subscribed", inplace=True)
df["Instructor"].fillna("No Instructor", inplace=True)
df["Class Type"].fillna("Not a Class", inplace=True)
df["Duration (mins)"].fillna(df["Duration (mins)"].median(), inplace=True)
df["Price"].fillna(df["Price"].median(), inplace=True)
df["Time Slot"].fillna(df["Time Slot"].mode()[0], inplace=True)
df["Customer Email"].fillna("Not Provided", inplace=True)
df["Customer Phone"].fillna("Not Provided", inplace=True)
df.drop_duplicates(inplace=True)
df["Booking Month"] = df["Booking Date"].dt.to_period("M")

st.title("Booking Data Analysis Dashboard")

booking_type = st.sidebar.selectbox("Select Booking Type", ["All"] + list(df["Booking Type"].unique()))
date_range = st.sidebar.date_input("Select Date Range", [df["Booking Date"].min(), df["Booking Date"].max()])

filtered_df = df
if booking_type != "All":
    filtered_df = df[df["Booking Type"] == booking_type]

if date_range:
    filtered_df = df[(df["Booking Date"] >= pd.to_datetime(date_range[0])) &
                     (df["Booking Date"] <= pd.to_datetime(date_range[1]))]

st.subheader("Count of Bookings by Type")
fig, ax = plt.subplots(figsize=(10, 5))
sns.countplot(data=filtered_df, x="Booking Type", order=filtered_df["Booking Type"].value_counts().index, palette="viridis")
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("Distribution of Booking Prices")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(filtered_df["Price"], bins=30, kde=True, color="blue")
st.pyplot(fig)

st.subheader("Bookings Trend Over Time")
fig, ax = plt.subplots(figsize=(12, 5))
filtered_df.groupby("Booking Month").size().plot(kind="line", marker="o", color="red", ax=ax)
plt.xlabel("Month")
plt.ylabel("Number of Bookings")
plt.grid()
st.pyplot(fig)

st.subheader("Filtered Data")
st.dataframe(filtered_df)

