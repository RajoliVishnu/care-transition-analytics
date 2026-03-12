# Care Transition Efficiency & Placement Outcome Analytics

This project is a Streamlit-based analytics dashboard developed as a B.Tech final year internship project. It analyzes the movement of children through the UAC care pipeline:

`CBP Custody -> HHS Care -> Sponsor Placement`

The dashboard focuses on operational efficiency, discharge outcomes, and backlog behavior using the dataset `HHS_Unaccompanied_Alien_Children_Program.csv`.

## Project Objective

The main objective of this project is to study how efficiently children move through the care transition pipeline and identify possible bottlenecks or delays.

This dashboard helps answer questions such as:

- How efficiently are children transferred from CBP custody to HHS care?
- How effective is the discharge process from HHS care?
- Is backlog increasing or decreasing over time?
- How does intake compare with discharge volume?

## Dataset Used

File:

- `HHS_Unaccompanied_Alien_Children_Program.csv`

Main columns:

- `Date`
- `Children apprehended and placed in CBP custody`
- `Children in CBP custody`
- `Children transferred out of CBP custody`
- `Children in HHS Care`
- `Children discharged from HHS Care`

## Features Available in the Dashboard

- Sidebar date range filter
- Dataset overview cards
- KPI cards
- Efficiency trend chart
- Backlog trend chart
- Intake vs discharge comparison chart
- Pipeline flow section
- Insights section
- Bottleneck alert panel
- Download filtered CSV button

## KPI Definitions

### 1. Transfer Efficiency

Measures how efficiently children move from CBP custody into HHS care.

Formula:

```text
Children transferred out of CBP custody / Children in CBP custody
```

### 2. Discharge Effectiveness

Measures how effectively children are discharged from HHS care.

Formula:

```text
Children discharged from HHS Care / Children in HHS Care
```

### 3. Pipeline Throughput

Measures overall movement from intake to final discharge.

Formula:

```text
Children discharged from HHS Care / Children apprehended and placed in CBP custody
```

### 4. Backlog Rate

Measures the difference between intake and discharge.

Formula:

```text
Children apprehended and placed in CBP custody - Children discharged from HHS Care
```

## Project Workflow

The project follows this flow:

### Step 1. Load Data

The CSV file is loaded into a pandas DataFrame.

### Step 2. Clean Data

The project performs:

- column renaming
- date conversion
- numeric conversion
- comma removal
- missing value handling

### Step 3. Calculate KPIs

The project computes Transfer Efficiency, Discharge Effectiveness, Pipeline Throughput, and Backlog Rate.

Division-by-zero cases are handled safely.

### Step 4. Apply Filters

The sidebar date filter allows users to analyze a selected period only.

### Step 5. Render Dashboard

The app displays:

- project header
- summary metric cards
- KPI cards
- visual trend charts
- comparison chart
- pipeline flow
- insights and alerts

## Project Structure

Files in this project:

- `app.py`
  Main Streamlit dashboard application

- `HHS_Unaccompanied_Alien_Children_Program.csv`
  Dataset used in the dashboard

- `requirements.txt`
  Python dependencies required to run the project

- `care_transition_analytics.ipynb`
  Notebook version used during project exploration or development

- `UAC_Project_With_Details.pptx`
  Presentation file related to the project

## Main Functions in `app.py`

### `load_data()`

Loads the CSV dataset.

### `clean_data()`

Cleans column names, converts types, and handles missing values.

### `calculate_kpis()`

Calculates all KPIs used in the dashboard.

### `build_dashboard()`

Builds the complete Streamlit dashboard UI.

## How to Run the Project

### Step 1. Open the project folder

Open terminal in:

```powershell
c:\Users\vishn\OneDrive\Desktop\care-transition-analytics-main
```

### Step 2. Install required packages

```powershell
pip install -r requirements.txt
```

### Step 3. Run the Streamlit app

```powershell
streamlit run app.py
```

### Step 4. Open the browser

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib

## Project Use Case

This dashboard can be useful for:

- operational monitoring
- trend analysis
- identifying transfer bottlenecks
- understanding discharge and placement performance
- backlog tracking

## GitHub Notes

If someone opens this repository, they should start with:

1. `README.md` for project understanding
2. `app.py` for the main code
3. `requirements.txt` for dependencies
4. `HHS_Unaccompanied_Alien_Children_Program.csv` for the dataset

## Author

RAJOLI VISHNU VARDAN REDY  
B.Tech Final Year Internship Project  
Unified Mentor Internship Program
