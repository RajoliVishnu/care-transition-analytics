import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Care Transition Efficiency Analytics",
    layout="wide"
)

# Load data
df = pd.read_csv("HHS_Unaccompanied_Alien_Children_Program.csv")

# Clean column name
df.rename(columns={
    'Children apprehended and placed in CBP custody*':
    'Children apprehended and placed in CBP custody'
}, inplace=True)

# Date conversion
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.sort_values('Date')

# Numeric cleaning
numeric_cols = [
    'Children apprehended and placed in CBP custody',
    'Children in CBP custody',
    'Children transferred out of CBP custody',
    'Children in HHS Care',
    'Children discharged from HHS Care'
]

for col in numeric_cols:
    df[col] = (
        df[col].astype(str)
        .str.replace(',', '')
        .str.strip()
    )
    df[col] = pd.to_numeric(df[col], errors='coerce')

df[numeric_cols] = df[numeric_cols].fillna(0)

# KPI calculations
df['Transfer_Efficiency'] = (
    df['Children transferred out of CBP custody'] /
    df['Children in CBP custody']
)

df['Discharge_Effectiveness'] = (
    df['Children discharged from HHS Care'] /
    df['Children in HHS Care']
)

df['Pipeline_Throughput'] = (
    df['Children discharged from HHS Care'] /
    df['Children apprehended and placed in CBP custody']
)

df['Backlog_Rate'] = (
    df['Children apprehended and placed in CBP custody'] -
    df['Children discharged from HHS Care']
)

df.replace([np.inf, -np.inf], 0, inplace=True)

# Sidebar
st.sidebar.title("Filters")
start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [df['Date'].min(), df['Date'].max()]
)

filtered_df = df[
    (df['Date'] >= pd.to_datetime(start_date)) &
    (df['Date'] <= pd.to_datetime(end_date))
]

# Dashboard Title
st.title("Care Transition Efficiency & Placement Outcome Analytics")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Transfer Efficiency",
    round(filtered_df['Transfer_Efficiency'].mean(), 2)
)

col2.metric(
    "Discharge Effectiveness",
    round(filtered_df['Discharge_Effectiveness'].mean(), 2)
)

col3.metric(
    "Pipeline Throughput",
    round(filtered_df['Pipeline_Throughput'].mean(), 2)
)

col4.metric(
    "Avg Backlog",
    int(filtered_df['Backlog_Rate'].mean())
)

# Charts
st.subheader("Efficiency Trends")

st.line_chart(
    filtered_df.set_index('Date')[
        ['Transfer_Efficiency', 'Discharge_Effectiveness']
    ]
)

st.subheader("Backlog Trend")
st.line_chart(
    filtered_df.set_index('Date')['Backlog_Rate']
)

# Bottleneck Alert
if filtered_df['Transfer_Efficiency'].mean() < 0.3:
    st.warning("⚠️ CBP → HHS Transfer Bottleneck Detected")

st.success("Dashboard Loaded Successfully")
