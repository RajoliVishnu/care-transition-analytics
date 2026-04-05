# Care Transition Efficiency & Placement Outcome Analytics

This is my data analyst internship project built using Streamlit.

I worked on operational analysis of the UAC pipeline:

`CBP Custody -> HHS Care -> Sponsor Placement`

The goal is simple: understand movement through the pipeline, check where delays happen, and suggest practical actions.

## Problem Statement

In this system, intake can grow faster than discharge. When this happens, backlog increases and operations become difficult.

So I built a dashboard to answer:

- Are transfers from CBP to HHS happening efficiently?
- Is discharge from HHS keeping up with intake?
- Is backlog increasing or reducing over time?
- Which periods show high pressure?

## Dataset

- `HHS_Unaccompanied_Alien_Children_Program.csv`

Main fields used:

- `Date`
- `Children apprehended and placed in CBP custody`
- `Children in CBP custody`
- `Children transferred out of CBP custody`
- `Children in HHS Care`
- `Children discharged from HHS Care`

## KPI Logic Used

1. Transfer Efficiency  
`Children transferred out of CBP custody / Children in CBP custody`

2. Discharge Effectiveness  
`Children discharged from HHS Care / Children in HHS Care`

3. Pipeline Throughput  
`Children discharged from HHS Care / Children apprehended and placed in CBP custody`

4. Backlog Rate  
`Children apprehended and placed in CBP custody - Children discharged from HHS Care`

## What I Built

- Custom Streamlit dashboard UI with themed cards and sections
- Date-range filter from sidebar
- KPI cards + summary cards
- Trend charts for efficiency and backlog
- Intake vs discharge comparison
- Monitor tab with threshold-based alerts
- Interactive Plotly charts for drill-down
- Risk score section (estimate-based)
- About section with method and limitations
- Download options for filtered CSV and project summary

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Plotly

## Performance

- Used `@st.cache_data` for dataset loading

## Key Challenges I Faced

- Some numeric values had commas and mixed formatting
- Needed date cleaning and sorting for proper time-series charts
- Had to keep charts readable with many sections in one app
- Added clear notes wherever a metric is estimate-based

## Limitations

- Dataset does not contain patient-level readmission events
- Dataset does not contain true individual stay-duration records
- Because of this, readmission risk and stay duration are shown as proxy/estimated metrics only

## How to Run

```powershell
cd "c:\Users\vishn\OneDrive\Desktop\care-transition-analytics-main"
python -m pip install -r requirements.txt
streamlit run app.py
```

## Project Files

- `app.py` - Main Streamlit dashboard
- `HHS_Unaccompanied_Alien_Children_Program.csv` - Dataset
- `requirements.txt` - Dependencies
- `HOW_IT_WORKS.md` - Internal flow explanation

## Author

RAJOLI VISHNU VARDAN REDY  
B.Tech Final Year Internship Project  
Unified Mentor Internship Program
