import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------
# Streamlit Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Care Transition Efficiency Analytics",
    layout="wide"
)

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("HHS_Unaccompanied_Alien_Children_Program.csv")

    df.rename(columns={
        'Children apprehended and placed in CBP custody*':
        'Children apprehended and placed in CBP custody'
    }, inplace=True)

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.sort_values('Date')

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

    return df


df = load_data()

# ---------------------------------------------------
# KPI Calculations (with division safety)
# ---------------------------------------------------
def calculate_kpis(df):

    df['Transfer_Efficiency'] = np.where(
        df['Children in CBP custody'] == 0,
        0,
        df['Children transferred out of CBP custody'] /
        df['Children in CBP custody']
    )

    df['Discharge_Effectiveness'] = np.where(
        df['Children in HHS Care'] == 0,
        0,
        df['Children discharged from HHS Care'] /
        df['Children in HHS Care']
    )

    df['Pipeline_Throughput'] = np.where(
        df['Children apprehended and placed in CBP custody'] == 0,
        0,
        df['Children discharged from HHS Care'] /
        df['Children apprehended and placed in CBP custody']
    )

    df['Backlog_Rate'] = (
        df['Children apprehended and placed in CBP custody'] -
        df['Children discharged from HHS Care']
    )

    return df


df = calculate_kpis(df)

# ---------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------
st.sidebar.title("Filters")

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [df['Date'].min(), df['Date'].max()]
)

filtered_df = df[
    (df['Date'] >= pd.to_datetime(start_date)) &
    (df['Date'] <= pd.to_datetime(end_date))
]

# ---------------------------------------------------
# Dashboard Title
# ---------------------------------------------------
st.title("Care Transition Efficiency & Placement Outcome Analytics")

st.markdown("""
This dashboard evaluates the efficiency of the UAC care pipeline by monitoring
transfer performance, discharge outcomes, and backlog accumulation across the system.
""")

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------
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

# ---------------------------------------------------
# Efficiency Trends
# ---------------------------------------------------
st.subheader("Efficiency Trends")

st.line_chart(
    filtered_df.set_index('Date')[
        ['Transfer_Efficiency', 'Discharge_Effectiveness']
    ]
)

st.markdown("""
**Business Interpretation**

Transfer efficiency reflects how quickly children move from CBP custody to HHS care.
Discharge effectiveness measures the rate at which children are successfully placed
with sponsors. Persistent gaps between these indicators may signal capacity or
processing bottlenecks in the care pipeline.
""")

# ---------------------------------------------------
# Backlog Trend
# ---------------------------------------------------
st.subheader("Backlog Trend")

st.line_chart(
    filtered_df.set_index('Date')['Backlog_Rate']
)

st.markdown("""
**Business Interpretation**

Backlog represents the difference between daily intake and successful placements.
Rising backlog values indicate that inflows exceed discharges, suggesting system
stress and potential delays in sponsor placement workflows.
""")

# ---------------------------------------------------
# Bottleneck Detection
# ---------------------------------------------------
if filtered_df['Transfer_Efficiency'].mean() < 0.3:
    st.warning("⚠️ CBP → HHS Transfer Bottleneck Detected")

# ---------------------------------------------------
# Dashboard Status
# ---------------------------------------------------
st.success("Dashboard Loaded Successfully")
