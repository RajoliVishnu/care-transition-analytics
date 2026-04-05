import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Care Transition Efficiency & Placement Outcome Analytics",
    page_icon="📊",
    layout="wide",
)


THEME = {
    "primary": "#2F5BEA",
    "secondary": "#2F5BEA",
    "secondary_soft": "#60A5FA",
    "accent": "#0F9D8A",
    "violet": "#4F46E5",
    "warning": "#F59E0B",
    "danger": "#DC2626",
    "background": "#F5F7FB",
    "card": "#FFFFFF",
    "text": "#1F2937",
    "muted": "#555555",
    "border": "#E2E8F0",
}

KPI_DETAILS = [
    {
        "label": "Transfer Efficiency",
        "column": "Transfer_Efficiency",
        "icon": "🚚",
        "color": THEME["secondary"],
        "format": "percent",
        "description": "Average transfer performance in the selected range",
    },
    {
        "label": "Discharge Effectiveness",
        "column": "Discharge_Effectiveness",
        "icon": "🏥",
        "color": THEME["accent"],
        "format": "percent",
        "description": "Average discharge performance in the selected range",
    },
    {
        "label": "Pipeline Throughput",
        "column": "Pipeline_Throughput",
        "icon": "📈",
        "color": THEME["warning"],
        "format": "percent",
        "description": "Overall case movement from intake to discharge",
    },
    {
        "label": "Average Backlog",
        "column": "Backlog_Rate",
        "icon": "📦",
        "color": THEME["danger"],
        "format": "integer",
        "description": "Average difference between intake and discharge",
    },
]


def inject_css():
    st.markdown(
        f"""
        <style>
            :root {{
                --bg-main: linear-gradient(135deg, #DCE8F8 0%, #E7F0FB 34%, #DDEBFF 68%, #D8E6FA 100%);
                --glass-white: rgba(255,255,255,0.74);
                --card-shadow:
                    10px 10px 22px rgba(31, 59, 92, 0.10),
                    -5px -5px 12px rgba(255, 255, 255, 0.96);
            }}

            html, body, [class*="css"] {{
                font-family: "Segoe UI", "Calibri", "Trebuchet MS", sans-serif;
            }}

            .stApp {{
                background:
                    linear-gradient(120deg, rgba(47, 91, 234, 0.10), transparent 22%),
                    linear-gradient(300deg, rgba(15, 157, 138, 0.08), transparent 20%),
                    radial-gradient(circle at top left, rgba(47, 91, 234, 0.12), transparent 24%),
                    radial-gradient(circle at bottom right, rgba(124, 58, 237, 0.10), transparent 20%),
                    var(--bg-main);
                color: {THEME["text"]};
            }}

            [data-testid="stHeader"] {{
                background: var(--bg-main);
            }}

            [data-testid="stDecoration"] {{
                display: none;
            }}

            [data-testid="stAppViewContainer"] {{
                background:
                    linear-gradient(120deg, rgba(47, 91, 234, 0.10), transparent 22%),
                    linear-gradient(300deg, rgba(15, 157, 138, 0.08), transparent 20%),
                    radial-gradient(circle at top left, rgba(47, 91, 234, 0.12), transparent 24%),
                    radial-gradient(circle at bottom right, rgba(124, 58, 237, 0.10), transparent 20%),
                    var(--bg-main);
            }}

            .main .block-container {{
                background: transparent;
            }}

            .block-container {{
                max-width: 1400px;
                padding-top: 1.9rem;
                padding-bottom: 2.8rem;
                padding-left: 2rem;
                padding-right: 2rem;
            }}

            section[data-testid="stSidebar"] {{
                background:
                    radial-gradient(circle at top left, rgba(255,255,255,0.10), transparent 20%),
                    linear-gradient(180deg, #183654 0%, #264E79 62%, #2F5BEA 100%);
                border-right: 1px solid rgba(255,255,255,0.08);
            }}

            section[data-testid="stSidebar"] * {{
                color: #F8FAFC;
            }}

            section[data-testid="stSidebar"] .stDateInput {{
                background: rgba(255,255,255,0.10);
                border: 1px solid rgba(255,255,255,0.16);
                border-radius: 16px;
                padding: 0.45rem 0.6rem;
                box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
            }}

            .sidebar-panel {{
                background: linear-gradient(180deg, rgba(255,255,255,0.16), rgba(255,255,255,0.10));
                border: 1px solid rgba(255,255,255,0.18);
                border-radius: 20px;
                padding: 1.05rem 1.1rem;
                margin-bottom: 1.05rem;
                box-shadow: 0 12px 24px rgba(9, 22, 39, 0.18);
                backdrop-filter: blur(6px);
                transition: transform 0.22s ease, box-shadow 0.22s ease, background 0.22s ease;
            }}

            .sidebar-panel:hover {{
                transform: translateY(-3px);
                box-shadow: 0 14px 26px rgba(9, 22, 39, 0.20);
                background: linear-gradient(180deg, rgba(255,255,255,0.20), rgba(255,255,255,0.12));
            }}

            .sidebar-title {{
                font-size: 0.9rem;
                font-weight: 800;
                margin-bottom: 0.5rem;
                letter-spacing: 0.03em;
                position: relative;
                display: inline-block;
                color: #FFFFFF;
                animation: sidebarTextSlide 7s ease-in-out infinite, sidebarTextColorShift 6s ease-in-out infinite;
            }}

            .filter-panel-title {{
                color: #FFFFFF;
                font-size: 1.5rem;
                font-weight: 800;
                margin-bottom: 0.8rem;
                display: inline-block;
                animation: sidebarTextSlide 7s ease-in-out infinite, sidebarTextColorShift 6s ease-in-out infinite;
                transition: transform 0.3s ease, color 0.3s ease, text-shadow 0.3s ease;
            }}

            .sidebar-divider {{
                height: 1px;
                background: rgba(255,255,255,0.12);
                margin: 0.9rem 0;
            }}

            .stDownloadButton > button {{
                background: linear-gradient(135deg, {THEME["secondary"]}, {THEME["violet"]});
                color: #FFFFFF;
                border: none;
                border-radius: 16px;
                padding: 10px 22px;
                font-weight: 700;
                box-shadow: 0 10px 20px rgba(47, 91, 234, 0.20);
                min-height: 48px;
                letter-spacing: 0.02em;
            }}

            .stDownloadButton > button:hover {{
                background: linear-gradient(135deg, #1D4ED8, #4338CA);
                color: #FFFFFF;
                transform: translateY(-2px);
                box-shadow: 0 8px 18px rgba(37, 99, 235, 0.22);
            }}

            .stDownloadButton > button:focus {{
                color: #FFFFFF;
                border: none;
                box-shadow: 0 0 0 0.2rem rgba(96, 165, 250, 0.28);
            }}

            .stDownloadButton > button:active {{
                transform: translateY(0);
                filter: brightness(0.96);
            }}

            .hero-banner {{
                background:
                    radial-gradient(circle at top right, rgba(255,255,255,0.22), transparent 22%),
                    linear-gradient(135deg, #16324F 0%, #2F5BEA 58%, #7C3AED 100%);
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 20px;
                padding: 2.3rem 2.5rem;
                color: #FFFFFF;
                box-shadow: 0 18px 34px rgba(15, 39, 64, 0.16);
                margin-bottom: 1.8rem;
                position: relative;
                overflow: hidden;
            }}

            .hero-banner::after {{
                content: "";
                position: absolute;
                inset: auto -5% -35% auto;
                width: 320px;
                height: 320px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(255,255,255,0.18), rgba(255,255,255,0.01));
            }}

            .hero-tag {{
                text-transform: uppercase;
                letter-spacing: 0.16em;
                font-size: 0.78rem;
                font-weight: 700;
                opacity: 0.84;
                margin-bottom: 0.55rem;
            }}


            .hero-title {{
                margin: 0;
                font-size: 32px;
                line-height: 1.08;
                font-weight: 800;
                letter-spacing: -0.02em;
                color: #FFFFFF;
                text-shadow:
                    0 1px 0 rgba(255,255,255,0.18),
                    0 4px 10px rgba(8, 18, 34, 0.18),
                    0 10px 22px rgba(8, 18, 34, 0.16);
                position: relative;
                display: inline-block;
                animation: namedTextSlide 7.2s ease-in-out infinite, heroNamedColorShift 7.8s ease-in-out infinite;
                transition: transform 0.35s ease, color 0.35s ease, text-shadow 0.35s ease;
            }}

            .hero-subtitle {{
                margin-top: 0.8rem;
                max-width: 800px;
                font-size: 14px;
                line-height: 1.8;
                color: rgba(255,255,255,0.90);
            }}

            .panel {{
                background: linear-gradient(180deg, rgba(255,255,255,1), rgba(240,247,255,0.98));
                border: 1px solid {THEME["border"]};
                border-radius: 16px;
                padding: 22px;
                box-shadow: var(--card-shadow);
                margin-bottom: 1.55rem;
                transition: transform 0.22s ease, box-shadow 0.22s ease;
                position: relative;
                overflow: hidden;
            }}

            .panel:hover {{
                transform: translateY(-4px);
                box-shadow:
                    12px 12px 20px rgba(0,0,0,0.12),
                    -4px -4px 8px rgba(255,255,255,0.94);
            }}

            .panel::before {{
                content: "";
                position: absolute;
                inset: 0;
                padding: 2px;
                border-radius: 16px;
                background: linear-gradient(90deg, rgba(47,91,234,0.85), rgba(15,157,138,0.55), rgba(124,58,237,0.65), rgba(47,91,234,0.85));
                -webkit-mask:
                    linear-gradient(#fff 0 0) content-box,
                    linear-gradient(#fff 0 0);
                -webkit-mask-composite: xor;
                mask:
                    linear-gradient(#fff 0 0) content-box,
                    linear-gradient(#fff 0 0);
                mask-composite: exclude;
                pointer-events: none;
            }}

            .section-title {{
                color: {THEME["primary"]};
                font-size: 20px;
                font-weight: 600;
                margin-bottom: 0.35rem;
                letter-spacing: -0.01em;
                position: relative;
                display: inline-block;
                padding-right: 1rem;
                animation: namedTextSlide 7.2s ease-in-out infinite, namedTitleColorShift 7.6s ease-in-out infinite;
                transition: transform 0.3s ease, color 0.3s ease, text-shadow 0.3s ease;
            }}

            .section-text {{
                color: {THEME["muted"]};
                font-size: 14px;
                margin-bottom: 1.15rem;
                line-height: 1.7;
            }}

            .overview-grid {{
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 1.1rem;
                margin-bottom: 1.45rem;
            }}

            .overview-card {{
                background: linear-gradient(180deg, var(--metric-bg-start), var(--metric-bg-end));
                border: 1px solid var(--metric-border);
                border-left: 6px solid var(--metric-accent);
                border-radius: 16px;
                padding: 22px;
                margin-bottom: 15px;
                box-shadow:
                    8px 8px 16px rgba(0,0,0,0.12),
                    -4px -4px 8px rgba(255,255,255,0.9);
                transition: transform 0.22s ease, box-shadow 0.22s ease;
                position: relative;
                overflow: hidden;
            }}

            .overview-card::before {{
                content: "";
                position: absolute;
                inset: 0;
                padding: 2px;
                border-radius: 16px;
                background: linear-gradient(90deg, var(--metric-accent), color-mix(in srgb, var(--metric-accent) 45%, white), var(--metric-accent));
                -webkit-mask:
                    linear-gradient(#fff 0 0) content-box,
                    linear-gradient(#fff 0 0);
                -webkit-mask-composite: xor;
                mask:
                    linear-gradient(#fff 0 0) content-box,
                    linear-gradient(#fff 0 0);
                mask-composite: exclude;
                pointer-events: none;
            }}

            .overview-card:hover {{
                transform: translateY(-5px);
                box-shadow:
                    12px 12px 20px rgba(0,0,0,0.14),
                    -4px -4px 8px rgba(255,255,255,0.92);
            }}

            .overview-card:active {{
                transform: translateY(-2px) scale(0.995);
                background: linear-gradient(180deg, color-mix(in srgb, var(--metric-accent) 10%, white), var(--metric-bg-end));
            }}

            .overview-label {{
                color: #425466;
                font-size: 14px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                animation: namedTextSlide 7.8s ease-in-out infinite, namedLabelColorShift 8.2s ease-in-out infinite;
            }}

            .overview-value {{
                color: #1F2937;
                font-size: 32px;
                font-weight: 800;
                margin-top: 0.45rem;
                margin-bottom: 0.35rem;
                letter-spacing: -0.02em;
                animation: namedValueSlide 7.1s ease-in-out infinite, namedValueColorShift 7.8s ease-in-out infinite;
            }}

            .overview-subtext {{
                color: {THEME["muted"]};
                font-size: 13px;
                margin-top: 0.25rem;
            }}

            .kpi-card {{
                background: linear-gradient(180deg, rgba(255,255,255,1) 0%, color-mix(in srgb, var(--accent) 10%, white) 100%);
                border: 1px solid {THEME["border"]};
                border-left: 6px solid var(--accent);
                border-radius: 16px;
                padding: 20px;
                min-height: 176px;
                box-shadow:
                    8px 8px 16px rgba(0,0,0,0.11),
                    -4px -4px 8px rgba(255,255,255,0.92);
                position: relative;
                overflow: hidden;
                transition: transform 0.22s ease, box-shadow 0.22s ease;
            }}

            .kpi-card::after {{
                content: "";
                position: absolute;
                top: -32px;
                right: -24px;
                width: 96px;
                height: 96px;
                background: radial-gradient(circle, color-mix(in srgb, var(--accent) 24%, white), rgba(47,91,234,0));
                border-radius: 50%;
            }}

            .kpi-card::before {{
                content: "";
                position: absolute;
                inset: 0;
                padding: 2px;
                border-radius: 16px;
                background: linear-gradient(90deg, var(--accent), color-mix(in srgb, var(--accent) 45%, white), var(--accent));
                -webkit-mask:
                    linear-gradient(#fff 0 0) content-box,
                    linear-gradient(#fff 0 0);
                -webkit-mask-composite: xor;
                mask:
                    linear-gradient(#fff 0 0) content-box,
                    linear-gradient(#fff 0 0);
                mask-composite: exclude;
                pointer-events: none;
            }}

            .kpi-card:hover {{
                transform: translateY(-5px);
                box-shadow:
                    12px 12px 22px rgba(0,0,0,0.13),
                    -4px -4px 8px rgba(255,255,255,0.94);
            }}

            .kpi-card:active {{
                transform: translateY(-2px) scale(0.995);
                background: linear-gradient(180deg, color-mix(in srgb, var(--accent) 16%, white) 0%, color-mix(in srgb, var(--accent) 10%, white) 100%);
            }}

            .kpi-row {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 0.95rem;
            }}

            .kpi-icon {{
                width: 2.5rem;
                height: 2.5rem;
                border-radius: 14px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(180deg, color-mix(in srgb, var(--accent) 18%, white), rgba(255,255,255,0.96));
                border: 1px solid color-mix(in srgb, var(--accent) 32%, white);
                font-size: 1.15rem;
                box-shadow: 0 8px 16px color-mix(in srgb, var(--accent) 20%, transparent);
                animation: namedValueSlide 7.4s ease-in-out infinite, iconColorShift 8s ease-in-out infinite;
            }}

            .kpi-label {{
                color: {THEME["muted"]};
                font-size: 14px;
                font-weight: 700;
                animation: namedTextSlide 7.6s ease-in-out infinite, namedLabelColorShift 8.2s ease-in-out infinite;
            }}

            .kpi-value {{
                color: {THEME["text"]};
                font-size: 28px;
                font-weight: 800;
                line-height: 1.1;
                letter-spacing: -0.03em;
                margin-top: 0.1rem;
                animation: namedValueSlide 7s ease-in-out infinite, namedValueColorShift 7.6s ease-in-out infinite;
            }}

            .kpi-note {{
                color: {THEME["muted"]};
                font-size: 14px;
                font-weight: 400;
                margin-top: 0.55rem;
                line-height: 1.65;
            }}

            .info-box {{
                border-radius: 18px;
                padding: 20px;
                border: 1px solid rgba(15, 157, 138, 0.18);
                background: linear-gradient(180deg, #FCFFFE 0%, #EAFBF5 100%);
                box-shadow:
                    10px 10px 18px rgba(15,157,138,0.10),
                    -4px -4px 8px rgba(255,255,255,0.94);
                position: relative;
                overflow: hidden;
            }}

            .info-box::before {{
                content: "";
                position: absolute;
                inset: 0;
                padding: 2px;
                border-radius: 18px;
                background: linear-gradient(90deg, rgba(15,157,138,0.85), rgba(110,231,183,0.55), rgba(15,157,138,0.85));
                -webkit-mask:
                    linear-gradient(#fff 0 0) content-box,
                    linear-gradient(#fff 0 0);
                -webkit-mask-composite: xor;
                mask:
                    linear-gradient(#fff 0 0) content-box,
                    linear-gradient(#fff 0 0);
                mask-composite: exclude;
                pointer-events: none;
            }}

            .info-box::after {{
                content: "";
                position: absolute;
                top: -36px;
                right: -28px;
                width: 110px;
                height: 110px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(15,157,138,0.12), rgba(15,157,138,0));
            }}

            .mini-stat {{
                background: linear-gradient(180deg, #FFFFFF 0%, #F8FBFF 100%);
                border: 1px solid {THEME["border"]};
                border-radius: 18px;
                padding: 20px;
                margin-top: 0.9rem;
                box-shadow:
                    10px 10px 18px rgba(0,0,0,0.08),
                    -4px -4px 8px rgba(255,255,255,0.94);
                position: relative;
                overflow: hidden;
            }}

            .mini-stat::before {{
                content: "";
                position: absolute;
                inset: 0 0 auto 0;
                height: 4px;
                background: linear-gradient(90deg, {THEME["secondary"]}, {THEME["secondary_soft"]});
            }}

            .pipeline-flow {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                flex-wrap: wrap;
            }}

            .pipeline-stage {{
                flex: 1 1 190px;
                background: linear-gradient(180deg, #FFFFFF 0%, #EEF5FF 100%);
                border: 1px solid {THEME["border"]};
                border-radius: 16px;
                padding: 20px;
                min-height: 120px;
                box-shadow:
                    8px 8px 16px rgba(0,0,0,0.08),
                    -4px -4px 8px rgba(255,255,255,0.92);
                text-align: center;
                transition: transform 0.22s ease, box-shadow 0.22s ease;
                position: relative;
                overflow: hidden;
            }}

            .pipeline-stage::before {{
                content: "";
                position: absolute;
                inset: 0;
                padding: 2px;
                border-radius: 16px;
                background: linear-gradient(90deg, rgba(47,91,234,0.75), rgba(122,90,248,0.45), rgba(47,91,234,0.75));
                -webkit-mask:
                    linear-gradient(#fff 0 0) content-box,
                    linear-gradient(#fff 0 0);
                -webkit-mask-composite: xor;
                mask:
                    linear-gradient(#fff 0 0) content-box,
                    linear-gradient(#fff 0 0);
                mask-composite: exclude;
                pointer-events: none;
            }}

            .pipeline-stage:hover {{
                transform: translateY(-4px);
                box-shadow:
                    12px 12px 20px rgba(0,0,0,0.10),
                    -4px -4px 8px rgba(255,255,255,0.94);
            }}

            .pipeline-stage:active {{
                transform: translateY(-2px) scale(0.995);
                background: linear-gradient(180deg, #FFFFFF 0%, #E3EEFF 100%);
            }}

            .pipeline-icon {{
                font-size: 1.45rem;
                margin-bottom: 0.55rem;
                animation: namedValueSlide 7.5s ease-in-out infinite, iconColorShift 8.2s ease-in-out infinite;
            }}

            .pipeline-title {{
                color: {THEME["primary"]};
                font-size: 17px;
                font-weight: 800;
                margin-bottom: 0.35rem;
                animation: namedTextSlide 7.3s ease-in-out infinite, namedTitleColorShift 7.9s ease-in-out infinite;
            }}

            .pipeline-text {{
                color: {THEME["muted"]};
                font-size: 14px;
                line-height: 1.55;
            }}

            .pipeline-arrow {{
                color: {THEME["secondary"]};
                font-size: 1.5rem;
                font-weight: 800;
                padding: 0 0.2rem;
            }}

            .insight-item {{
                border-left: 4px solid {THEME["secondary"]};
                background: linear-gradient(180deg, #FFFFFF 0%, #EDF4FF 100%);
                border-radius: 18px;
                padding: 20px;
                margin-bottom: 0.9rem;
                border-top: 1px solid {THEME["border"]};
                border-right: 1px solid {THEME["border"]};
                border-bottom: 1px solid {THEME["border"]};
                box-shadow:
                    10px 10px 18px rgba(47,91,234,0.10),
                    -4px -4px 8px rgba(255,255,255,0.94);
                position: relative;
                overflow: hidden;
            }}

            .insight-item::before {{
                content: "";
                position: absolute;
                inset: 0;
                padding: 2px;
                border-radius: 18px;
                background: linear-gradient(90deg, rgba(47,91,234,0.85), rgba(122,90,248,0.55), rgba(47,91,234,0.85));
                -webkit-mask:
                    linear-gradient(#fff 0 0) content-box,
                    linear-gradient(#fff 0 0);
                -webkit-mask-composite: xor;
                mask:
                    linear-gradient(#fff 0 0) content-box,
                    linear-gradient(#fff 0 0);
                mask-composite: exclude;
                pointer-events: none;
            }}

            .insight-item::after {{
                content: "";
                position: absolute;
                top: -30px;
                right: -24px;
                width: 96px;
                height: 96px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(47,91,234,0.10), rgba(47,91,234,0));
            }}

            .insight-item:hover {{
                transform: translateY(-4px);
                box-shadow:
                    12px 12px 20px rgba(47,91,234,0.12),
                    -4px -4px 8px rgba(255,255,255,0.96);
            }}

            .insight-item:active {{
                transform: translateY(-2px) scale(0.995);
                background: linear-gradient(180deg, #FFFFFF 0%, #E6F0FF 100%);
            }}

            .insight-title {{
                color: {THEME["primary"]};
                font-size: 16px;
                font-weight: 800;
                margin-bottom: 0.4rem;
                letter-spacing: -0.01em;
                animation: namedTextSlide 7.4s ease-in-out infinite, namedTitleColorShift 8s ease-in-out infinite;
                transition: transform 0.3s ease, color 0.3s ease, text-shadow 0.3s ease;
            }}

            .insight-text {{
                color: {THEME["muted"]};
                font-size: 14px;
                line-height: 1.75;
            }}

            .mini-stat-label {{
                color: #425466;
                font-size: 14px;
                font-weight: 700;
                margin-bottom: 0.35rem;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                animation: namedTextSlide 7.6s ease-in-out infinite, namedLabelColorShift 8.2s ease-in-out infinite;
            }}

            .mini-stat-value {{
                color: #1F2937;
                font-size: 24px;
                font-weight: 800;
                letter-spacing: -0.02em;
                animation: namedValueSlide 7s ease-in-out infinite, namedValueColorShift 7.8s ease-in-out infinite;
            }}

            .alert-box {{
                border-radius: 18px;
                padding: 20px;
                border: 1px solid rgba(220, 38, 38, 0.20);
                background: linear-gradient(180deg, rgba(255,250,250,1), rgba(254,238,238,1));
                font-weight: 700;
                box-shadow:
                    10px 10px 18px rgba(220,38,38,0.10),
                    -4px -4px 8px rgba(255,255,255,0.94);
                position: relative;
                overflow: hidden;
            }}

            .alert-box::before {{
                content: "";
                position: absolute;
                inset: 0 0 auto 0;
                height: 4px;
                background: linear-gradient(90deg, #DC2626, #F87171);
            }}

            .alert-box:hover,
            .info-box:hover,
            .mini-stat:hover,
            .download-wrap:hover {{
                transform: translateY(-4px);
            }}

            .info-box,
            .mini-stat,
            .alert-box,
            .download-wrap,
            .insight-item,
            .pipeline-stage,
            .overview-card,
            .kpi-card {{
                transition: transform 0.22s ease, box-shadow 0.22s ease, background 0.22s ease, border-color 0.22s ease;
            }}

            .info-box:active,
            .mini-stat:active,
            .alert-box:active,
            .download-wrap:active {{
                transform: translateY(-2px) scale(0.995);
            }}

            .download-wrap {{
                background: linear-gradient(180deg, #FFFFFF 0%, #EEF5FF 100%);
                border: 1px solid {THEME["border"]};
                border-radius: 16px;
                padding: 16px 18px;
                box-shadow:
                    8px 8px 16px rgba(0,0,0,0.08),
                    -4px -4px 8px rgba(255,255,255,0.92);
                margin-bottom: 1.35rem;
                position: relative;
                overflow: hidden;
            }}

            .download-wrap::before {{
                content: "";
                position: absolute;
                inset: 0;
                padding: 2px;
                border-radius: 16px;
                background: linear-gradient(90deg, rgba(47,91,234,0.80), rgba(122,90,248,0.55), rgba(47,91,234,0.80));
                -webkit-mask:
                    linear-gradient(#fff 0 0) content-box,
                    linear-gradient(#fff 0 0);
                -webkit-mask-composite: xor;
                mask:
                    linear-gradient(#fff 0 0) content-box,
                    linear-gradient(#fff 0 0);
                mask-composite: exclude;
                pointer-events: none;
            }}

            .download-wrap .stDownloadButton {{
                display: inline-block;
            }}

            .download-wrap p {{
                margin: 0;
            }}

            .footer {{
                margin-top: 1.4rem;
                background:
                    radial-gradient(circle at top right, rgba(122, 90, 248, 0.10), transparent 20%),
                    radial-gradient(circle at bottom left, rgba(47, 91, 234, 0.10), transparent 18%),
                    linear-gradient(135deg, #F7FAFF 0%, #F5F7FB 45%, #EEF4FF 100%);
                border: 1px solid #DCE6F4;
                border-radius: 18px;
                padding: 26px 22px;
                text-align: center;
                color: #5B6B8B;
                box-shadow:
                    12px 12px 22px rgba(31,59,92,0.10),
                    -4px -4px 8px rgba(255,255,255,0.94);
                font-size: 14px;
                line-height: 1.85;
                position: relative;
                overflow: hidden;
                transition: transform 0.24s ease, box-shadow 0.24s ease;
            }}

            .footer:hover {{
                transform: translateY(-4px);
                box-shadow:
                    16px 16px 26px rgba(31,59,92,0.12),
                    -4px -4px 8px rgba(255,255,255,0.96);
            }}

            .footer::after {{
                content: "";
                position: absolute;
                inset: 0 0 auto 0;
                height: 4px;
                background: linear-gradient(90deg, #2F5BEA, #7A5AF8, #2DBE7E);
            }}

            .footer-divider {{
                margin-top: 0.8rem;
                margin-bottom: 1rem;
                border: none;
                border-top: 1px solid rgba(31, 42, 68, 0.12);
            }}

            .footer-title {{
                font-size: 18px;
                color: #1F2A44;
                font-weight: 700;
                margin-bottom: 0.4rem;
                letter-spacing: -0.01em;
            }}

            .footer-subtitle {{
                font-size: 14px;
                color: #5B6B8B;
                margin-bottom: 0.7rem;
            }}

            .footer-name-label {{
                font-size: 14px;
                color: #5B6B8B;
                margin-top: 0.2rem;
            }}

            .footer-name {{
                font-size: 16px;
                font-weight: 700;
                color: #2F5BEA;
                margin-top: 0.2rem;
                margin-bottom: 0.55rem;
                text-shadow: 0 4px 12px rgba(47,91,234,0.16);
            }}

            .footer-program {{
                font-size: 13px;
                color: #7B8798;
            }}

            .chart-caption {{
                color: {THEME["muted"]};
                font-size: 14px;
                margin-top: 0.75rem;
                line-height: 1.75;
            }}

            @keyframes namedTextSlide {{
                0% {{ transform: translateX(0px); }}
                25% {{ transform: translateX(3px); }}
                50% {{ transform: translateX(-3px); }}
                75% {{ transform: translateX(2px); }}
                100% {{ transform: translateX(0px); }}
            }}

            @keyframes namedValueSlide {{
                0% {{ transform: translateX(0px); }}
                25% {{ transform: translateX(4px); }}
                50% {{ transform: translateX(-4px); }}
                75% {{ transform: translateX(3px); }}
                100% {{ transform: translateX(0px); }}
            }}

            @keyframes namedTitleColorShift {{
                0% {{ color: #2F5BEA; text-shadow: 0 2px 10px rgba(47,91,234,0.10); }}
                25% {{ color: #4B74F2; text-shadow: 0 4px 12px rgba(75,116,242,0.16); }}
                50% {{ color: #7A5AF8; text-shadow: 0 4px 12px rgba(122,90,248,0.18); }}
                75% {{ color: #2DBE7E; text-shadow: 0 4px 12px rgba(45,190,126,0.16); }}
                100% {{ color: #2F5BEA; text-shadow: 0 2px 10px rgba(47,91,234,0.10); }}
            }}

            @keyframes heroNamedColorShift {{
                0% {{ color: #FFFFFF; text-shadow: 0 1px 0 rgba(255,255,255,0.18), 0 4px 10px rgba(8, 18, 34, 0.18), 0 10px 22px rgba(8, 18, 34, 0.16); }}
                25% {{ color: #E3ECFF; text-shadow: 0 1px 0 rgba(255,255,255,0.22), 0 6px 14px rgba(8, 18, 34, 0.20), 0 10px 24px rgba(59,130,246,0.18); }}
                50% {{ color: #D6E4FF; text-shadow: 0 1px 0 rgba(255,255,255,0.24), 0 6px 16px rgba(8, 18, 34, 0.22), 0 10px 26px rgba(122,90,248,0.22); }}
                75% {{ color: #E8FFF7; text-shadow: 0 1px 0 rgba(255,255,255,0.22), 0 6px 14px rgba(8, 18, 34, 0.20), 0 10px 24px rgba(45,190,126,0.18); }}
                100% {{ color: #FFFFFF; text-shadow: 0 1px 0 rgba(255,255,255,0.18), 0 4px 10px rgba(8, 18, 34, 0.18), 0 10px 22px rgba(8, 18, 34, 0.16); }}
            }}

            @keyframes namedLabelColorShift {{
                0% {{ color: #425466; }}
                25% {{ color: #5C7394; }}
                50% {{ color: #2F5BEA; }}
                75% {{ color: #61708D; }}
                100% {{ color: #425466; }}
            }}

            @keyframes namedValueColorShift {{
                0% {{ color: #1F2937; text-shadow: 0 0 0 rgba(0,0,0,0); }}
                25% {{ color: #2F5BEA; text-shadow: 0 4px 12px rgba(47,91,234,0.14); }}
                50% {{ color: #7A5AF8; text-shadow: 0 4px 12px rgba(122,90,248,0.16); }}
                75% {{ color: #2DBE7E; text-shadow: 0 4px 12px rgba(45,190,126,0.14); }}
                100% {{ color: #1F2937; text-shadow: 0 0 0 rgba(0,0,0,0); }}
            }}

            @keyframes iconColorShift {{
                0% {{ color: #2F5BEA; }}
                25% {{ color: #2DBE7E; }}
                50% {{ color: #FF9F43; }}
                75% {{ color: #7A5AF8; }}
                100% {{ color: #2F5BEA; }}
            }}


            @keyframes sidebarTextSlide {{
                0% {{ transform: translateX(0px); }}
                25% {{ transform: translateX(3px); }}
                50% {{ transform: translateX(-3px); }}
                75% {{ transform: translateX(2px); }}
                100% {{ transform: translateX(0px); }}
            }}

            @keyframes sidebarTextColorShift {{
                0% {{
                    color: #FFFFFF;
                    text-shadow: 0 0 0 rgba(255,255,255,0);
                }}
                25% {{
                    color: #DDEBFF;
                    text-shadow: 0 0 10px rgba(189, 219, 255, 0.22);
                }}
                50% {{
                    color: #9FD0FF;
                    text-shadow: 0 0 14px rgba(159, 208, 255, 0.28);
                }}
                75% {{
                    color: #DDEBFF;
                    text-shadow: 0 0 10px rgba(189, 219, 255, 0.22);
                }}
                100% {{
                    color: #FFFFFF;
                    text-shadow: 0 0 0 rgba(255,255,255,0);
                }}
            }}

            hr {{
                margin-top: 0.5rem;
                margin-bottom: 1rem;
                border-color: rgba(20, 50, 74, 0.10);
            }}

            .stTabs [data-baseweb="tab-list"] {{
                gap: 0.35rem;
                background: rgba(255, 255, 255, 0.65);
                border: 1px solid rgba(47, 91, 234, 0.14);
                border-radius: 14px;
                padding: 0.25rem;
            }}

            .stTabs [data-baseweb="tab"] {{
                border-radius: 10px;
                font-weight: 700;
                color: #334155;
                padding: 0.45rem 0.95rem;
            }}

            .stTabs [aria-selected="true"] {{
                background: linear-gradient(135deg, #2F5BEA, #4F46E5);
                color: #FFFFFF;
            }}

            .stat-card {{
                border-radius: 16px;
                padding: 16px 18px;
                border: 1px solid var(--card-border);
                border-left: 6px solid var(--card-accent);
                background: linear-gradient(180deg, var(--card-bg-start), var(--card-bg-end));
                box-shadow: 8px 8px 18px rgba(0, 0, 0, 0.10), -4px -4px 8px rgba(255, 255, 255, 0.92);
                min-height: 122px;
                transition: transform 0.22s ease, box-shadow 0.22s ease;
            }}

            .stat-card:hover {{
                transform: translateY(-4px);
                box-shadow: 12px 12px 20px rgba(0, 0, 0, 0.13), -4px -4px 8px rgba(255, 255, 255, 0.94);
            }}

            .stat-title {{
                color: #475569;
                font-size: 15px;
                font-weight: 700;
                margin-bottom: 0.5rem;
            }}

            .stat-value {{
                color: #0F172A;
                font-size: 46px;
                line-height: 1;
                font-weight: 800;
                letter-spacing: -0.02em;
            }}

            .status-alert {{
                border-radius: 14px;
                padding: 14px 16px;
                font-size: 1.05rem;
                font-weight: 700;
                border: 1px solid transparent;
                margin-top: 0.45rem;
            }}

            .status-alert.warning {{
                background: linear-gradient(90deg, #FFF4D6, #FFE8B5);
                border-color: #F4C96C;
                color: #8A4B00;
            }}

            .status-alert.success {{
                background: linear-gradient(90deg, #E8FAF0, #D8F5E5);
                border-color: #86D7A8;
                color: #12633A;
            }}

            [data-testid="stMetric"] {{
                background: linear-gradient(180deg, #FFFFFF 0%, #F5F9FF 100%);
                border: 1px solid #D8E4F3;
                border-radius: 14px;
                padding: 0.9rem 1rem;
                box-shadow: 6px 6px 14px rgba(15, 23, 42, 0.08), -3px -3px 8px rgba(255, 255, 255, 0.9);
            }}

            [data-testid="stMetricLabel"] {{
                color: #475569 !important;
                font-weight: 700;
            }}

            [data-testid="stMetricValue"] {{
                color: #0F172A !important;
                font-weight: 800;
            }}

            [data-testid="stMetricDelta"] {{
                color: #1D4ED8 !important;
            }}

            @media (max-width: 900px) {{
                .block-container {{
                    padding-left: 1rem;
                    padding-right: 1rem;
                }}

                .hero-banner {{
                    padding: 1.5rem;
                }}

                .overview-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def load_data(file_path: str = "HHS_Unaccompanied_Alien_Children_Program.csv") -> pd.DataFrame:
    return pd.read_csv(file_path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned_df = df.copy()

    cleaned_df = cleaned_df.rename(
        columns={
            "Children apprehended and placed in CBP custody*":
            "Children apprehended and placed in CBP custody"
        }
    )

    cleaned_df["Date"] = pd.to_datetime(cleaned_df["Date"], errors="coerce")

    numeric_columns = [
        "Children apprehended and placed in CBP custody",
        "Children in CBP custody",
        "Children transferred out of CBP custody",
        "Children in HHS Care",
        "Children discharged from HHS Care",
    ]

    for column in numeric_columns:
        cleaned_df[column] = pd.to_numeric(
            cleaned_df[column].astype(str).str.replace(",", "", regex=False).str.strip(),
            errors="coerce",
        )

    cleaned_df[numeric_columns] = cleaned_df[numeric_columns].fillna(0)
    cleaned_df = cleaned_df.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)
    return cleaned_df


def calculate_kpis(df: pd.DataFrame) -> pd.DataFrame:
    kpi_df = df.copy()

    kpi_df["Transfer_Efficiency"] = np.where(
        kpi_df["Children in CBP custody"] == 0,
        0,
        kpi_df["Children transferred out of CBP custody"] / kpi_df["Children in CBP custody"],
    )

    kpi_df["Discharge_Effectiveness"] = np.where(
        kpi_df["Children in HHS Care"] == 0,
        0,
        kpi_df["Children discharged from HHS Care"] / kpi_df["Children in HHS Care"],
    )

    kpi_df["Pipeline_Throughput"] = np.where(
        kpi_df["Children apprehended and placed in CBP custody"] == 0,
        0,
        kpi_df["Children discharged from HHS Care"]
        / kpi_df["Children apprehended and placed in CBP custody"],
    )

    kpi_df["Backlog_Rate"] = (
        kpi_df["Children apprehended and placed in CBP custody"]
        - kpi_df["Children discharged from HHS Care"]
    )

    return kpi_df


def format_kpi_value(value: float, value_type: str) -> str:
    if value_type == "percent":
        return f"{value:.2%}"
    return f"{int(round(value)):,}"


def render_section_header(title: str, description: str):
    st.markdown(
        f"""
        <div class="section-title">{title}</div>
        <div class="section-text">{description}</div>
        """,
        unsafe_allow_html=True,
    )


def create_line_chart(
    data: pd.DataFrame,
    columns: list[str],
    chart_title: str,
    y_label: str,
    colors: list[str],
):
    fig, ax = plt.subplots(figsize=(12, 4.9))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    for column, color in zip(columns, colors):
        ax.plot(
            data["Date"],
            data[column],
            color=color,
            linewidth=2.8,
            label=column.replace("_", " "),
            solid_capstyle="round",
        )

    ax.set_title(chart_title, fontsize=15, fontweight="bold", color=THEME["primary"], pad=14)
    ax.set_ylabel(y_label, fontsize=10, color=THEME["muted"])
    ax.grid(True, axis="y", linestyle="--", linewidth=0.8, alpha=0.24)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#D0D9E4")
    ax.spines["bottom"].set_color("#D0D9E4")
    ax.tick_params(axis="both", colors=THEME["muted"], labelsize=10)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.legend(frameon=False, loc="upper left", ncol=len(columns))
    fig.autofmt_xdate(rotation=0, ha="center")
    plt.tight_layout()
    return fig


def create_comparison_chart(data: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(12, 4.9))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    ax.plot(
        data["Date"],
        data["Children apprehended and placed in CBP custody"],
        color=THEME["secondary"],
        linewidth=2.8,
        label="CBP Intake",
        solid_capstyle="round",
    )
    ax.plot(
        data["Date"],
        data["Children discharged from HHS Care"],
        color=THEME["warning"],
        linewidth=2.8,
        label="HHS Discharge",
        solid_capstyle="round",
    )

    ax.set_title("Intake vs Discharge Comparison", fontsize=15, fontweight="bold", color=THEME["primary"], pad=14)
    ax.set_ylabel("Number of Children", fontsize=10, color=THEME["muted"])
    ax.grid(True, axis="y", linestyle="--", linewidth=0.8, alpha=0.24)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#D0D9E4")
    ax.spines["bottom"].set_color("#D0D9E4")
    ax.tick_params(axis="both", colors=THEME["muted"], labelsize=10)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.legend(frameon=False, loc="upper left", ncol=2)
    fig.autofmt_xdate(rotation=0, ha="center")
    plt.tight_layout()
    return fig


def estimate_avg_stay_days(filtered_df: pd.DataFrame) -> float:
    date_diffs = filtered_df["Date"].sort_values().diff().dropna().dt.days
    period_days = float(date_diffs.median()) if not date_diffs.empty else 7.0
    discharge_mean = filtered_df["Children discharged from HHS Care"].mean()
    if discharge_mean <= 0:
        return 0.0
    return float((filtered_df["Children in HHS Care"].mean() / discharge_mean) * period_days)


def calculate_portfolio_kpis(filtered_df: pd.DataFrame) -> dict[str, float]:
    total_patients = float(filtered_df["Children discharged from HHS Care"].sum())
    readmission_proxy = float(
        np.clip(
            (
                (filtered_df["Backlog_Rate"] > 0).sum()
                / max(len(filtered_df), 1)
            ) * 100,
            0,
            100,
        )
    )
    avg_stay_days = estimate_avg_stay_days(filtered_df)
    return {
        "total_patients": total_patients,
        "readmission_proxy": readmission_proxy,
        "avg_stay_days": avg_stay_days,
    }


def render_portfolio_kpi_cards(filtered_df: pd.DataFrame):
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    render_section_header(
        "Extra KPI Snapshot",
        "These two healthcare-style metrics are estimated from available operational data.",
    )
    metric_data = calculate_portfolio_kpis(filtered_df)
    col1, col2, col3 = st.columns(3, gap="large")
    col1.markdown(
        f"""
        <div class="stat-card" style="--card-accent:#2563EB; --card-border:#CFE0FF; --card-bg-start:#FFFFFF; --card-bg-end:#EEF4FF;">
            <div class="stat-title">Total Patients Processed</div>
            <div class="stat-value">{int(round(metric_data['total_patients'])):,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col2.markdown(
        f"""
        <div class="stat-card" style="--card-accent:#F59E0B; --card-border:#FFE2B2; --card-bg-start:#FFFFFF; --card-bg-end:#FFF6E8;">
            <div class="stat-title">Readmission Risk (Estimated)</div>
            <div class="stat-value">{metric_data['readmission_proxy']:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col3.markdown(
        f"""
        <div class="stat-card" style="--card-accent:#16A34A; --card-border:#CDEFD9; --card-bg-start:#FFFFFF; --card-bg-end:#ECFDF3;">
            <div class="stat-title">Avg Stay Duration (Estimated)</div>
            <div class="stat-value">{metric_data['avg_stay_days']:.1f} days</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(
        "Note: This dataset does not have direct readmission events or patient-level stay records, so these are estimate-based proxy metrics."
    )
    st.markdown("</div>", unsafe_allow_html=True)


def calculate_executive_score(filtered_df: pd.DataFrame) -> tuple[float, str]:
    transfer = float(np.clip(filtered_df["Transfer_Efficiency"].mean(), 0, 1))
    discharge = float(np.clip(filtered_df["Discharge_Effectiveness"].mean() * 12, 0, 1))
    throughput = float(np.clip(filtered_df["Pipeline_Throughput"].mean(), 0, 1))
    backlog_health = float(
        np.clip(1 - (filtered_df["Backlog_Rate"].mean() / max(filtered_df["Children apprehended and placed in CBP custody"].mean(), 1)), 0, 1)
    )
    score = (transfer * 0.35 + discharge * 0.20 + throughput * 0.25 + backlog_health * 0.20) * 100
    if score >= 85:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 55:
        grade = "C"
    else:
        grade = "D"
    return float(score), grade


def render_executive_scorecard(filtered_df: pd.DataFrame):
    score, grade = calculate_executive_score(filtered_df)
    trend = filtered_df["Backlog_Rate"].iloc[-1] - filtered_df["Backlog_Rate"].iloc[0]
    status = "Improving" if trend <= 0 else "Under Pressure"

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    render_section_header(
        "Overall Performance Score",
        "A simple combined score based on transfer, discharge, throughput, and backlog health.",
    )
    col1, col2, col3 = st.columns([1, 1, 2], gap="large")
    col1.metric("Performance Score", f"{score:.1f}/100")
    col2.metric("Grade", grade)
    col3.metric("Current Status", status)
    st.progress(int(round(score)))
    st.markdown("</div>", unsafe_allow_html=True)


def render_realtime_monitor(filtered_df: pd.DataFrame):
    latest = filtered_df.iloc[-1]
    recent_window = filtered_df.tail(8).copy()
    avg_recent_backlog = recent_window["Backlog_Rate"].mean()

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    render_section_header(
        "Current Operations Monitor",
        "Latest snapshot with threshold-based alerts.",
    )
    c1, c2, c3, c4 = st.columns(4, gap="large")
    c1.markdown(
        f"""
        <div class="stat-card" style="--card-accent:#3B82F6; --card-border:#CFE3FF; --card-bg-start:#FFFFFF; --card-bg-end:#EFF6FF;">
            <div class="stat-title">Latest Intake</div>
            <div class="stat-value">{int(latest['Children apprehended and placed in CBP custody']):,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c2.markdown(
        f"""
        <div class="stat-card" style="--card-accent:#14B8A6; --card-border:#C8F2EE; --card-bg-start:#FFFFFF; --card-bg-end:#EBFFFC;">
            <div class="stat-title">Latest Discharge</div>
            <div class="stat-value">{int(latest['Children discharged from HHS Care']):,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c3.markdown(
        f"""
        <div class="stat-card" style="--card-accent:#DC2626; --card-border:#F9CECE; --card-bg-start:#FFFFFF; --card-bg-end:#FFF1F1;">
            <div class="stat-title">Latest Backlog</div>
            <div class="stat-value">{int(latest['Backlog_Rate']):,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c4.markdown(
        f"""
        <div class="stat-card" style="--card-accent:#7C3AED; --card-border:#E5D6FF; --card-bg-start:#FFFFFF; --card-bg-end:#F6F0FF;">
            <div class="stat-title">Data Freshness</div>
            <div class="stat-value">{latest['Date'].strftime("%Y-%m-%d")}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    backlog_alert = latest["Backlog_Rate"] > avg_recent_backlog * 1.15
    transfer_alert = latest["Transfer_Efficiency"] < 0.30
    discharge_alert = latest["Discharge_Effectiveness"] < 0.01

    if backlog_alert or transfer_alert or discharge_alert:
        st.markdown(
            """
            <div class="status-alert warning">
                Alert: One or more thresholds are crossed. Please review transfer and discharge flow.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="status-alert success">
                Good: All monitored thresholds are in a normal range.
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def build_executive_report(filtered_df: pd.DataFrame, start_date: pd.Timestamp, end_date: pd.Timestamp) -> str:
    score, grade = calculate_executive_score(filtered_df)
    backlog_change = int(round(filtered_df["Backlog_Rate"].iloc[-1] - filtered_df["Backlog_Rate"].iloc[0]))
    return (
        "Care Transition Analytics - Project Summary\n"
        f"Selected Period: {start_date.date()} to {end_date.date()}\n"
        f"Records: {len(filtered_df):,}\n\n"
        "Top 3 Insights\n"
        f"1) Transfer Efficiency: {filtered_df['Transfer_Efficiency'].mean():.2%}\n"
        f"2) Discharge Effectiveness: {filtered_df['Discharge_Effectiveness'].mean():.2%}\n"
        f"3) Backlog Net Change: {backlog_change:,}\n\n"
        f"Overall Performance Score: {score:.1f}/100 (Grade {grade})\n"
        "Recommended Decision: Increase placement support in backlog-heavy periods and review bottlenecks weekly.\n"
        "Conclusion: Better intake-discharge balance improves overall system stability.\n"
    )


def render_plotly_charts(filtered_df: pd.DataFrame):
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    render_section_header(
        "Interactive Analysis",
        "Use hover and zoom to inspect trends in detail.",
    )
    chart_df = filtered_df.copy()
    chart_df["Transfer Efficiency"] = chart_df["Transfer_Efficiency"]
    chart_df["Discharge Effectiveness"] = chart_df["Discharge_Effectiveness"]
    chart_df["Pipeline Throughput"] = chart_df["Pipeline_Throughput"]

    efficiency_fig = px.line(
        chart_df,
        x="Date",
        y=["Transfer Efficiency", "Discharge Effectiveness", "Pipeline Throughput"],
        title="Efficiency Indicators Over Time",
        color_discrete_sequence=[THEME["secondary"], THEME["accent"], THEME["warning"]],
    )
    efficiency_fig.update_layout(hovermode="x unified", yaxis_tickformat=".0%")
    st.plotly_chart(efficiency_fig, use_container_width=True)

    backlog_fig = px.area(
        chart_df,
        x="Date",
        y="Backlog_Rate",
        title="Backlog Pressure Trend",
        color_discrete_sequence=[THEME["danger"]],
    )
    backlog_fig.update_layout(hovermode="x unified")
    st.plotly_chart(backlog_fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_drilldown_section(filtered_df: pd.DataFrame):
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    render_section_header(
        "Drill-Down Analysis",
        "Select one metric and quickly view top high/low periods.",
    )
    metric_map = {
        "Transfer Efficiency": "Transfer_Efficiency",
        "Discharge Effectiveness": "Discharge_Effectiveness",
        "Pipeline Throughput": "Pipeline_Throughput",
        "Backlog Rate": "Backlog_Rate",
    }
    selected_metric = st.selectbox("Select metric for drill-down", list(metric_map.keys()))
    metric_col = metric_map[selected_metric]

    ranked = filtered_df[["Date", metric_col]].copy()
    ascending = selected_metric != "Backlog Rate"
    ranked = ranked.sort_values(metric_col, ascending=ascending).head(10)
    ranked["Date"] = ranked["Date"].dt.strftime("%Y-%m-%d")
    ranked = ranked.rename(columns={metric_col: "Value"})

    st.dataframe(ranked, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_storytelling_section(filtered_df: pd.DataFrame):
    transfer_mean = filtered_df["Transfer_Efficiency"].mean()
    discharge_mean = filtered_df["Discharge_Effectiveness"].mean()
    throughput_mean = filtered_df["Pipeline_Throughput"].mean()
    backlog_change = filtered_df["Backlog_Rate"].iloc[-1] - filtered_df["Backlog_Rate"].iloc[0]

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    render_section_header(
        "Top 3 Insights and Decision",
        "Main takeaways from the selected date range.",
    )
    st.markdown(
        f"""
        1. **Transfer Efficiency:** Average transfer efficiency is **{transfer_mean:.2%}**, highlighting upstream movement strength.
        2. **Discharge Performance:** Discharge effectiveness is **{discharge_mean:.2%}** with throughput at **{throughput_mean:.2%}**.
        3. **Backlog Direction:** Backlog changed by **{int(round(backlog_change)):,}** over the selected period.
        """
    )

    decision_text = (
        "Scale sponsor-placement capacity and prioritize backlog-heavy periods."
        if backlog_change > 0
        else "Maintain current process controls and redirect resources to further reduce residual backlog."
    )
    st.markdown(f"**What decision can be taken?** {decision_text}")
    st.markdown(
        "**Recommendations:** 1) Do a weekly bottleneck review, 2) add capacity when backlog rises for 2+ periods, 3) copy workflows from high-performing periods."
    )
    st.markdown(
        "**Conclusion:** The system works better when intake and discharge stay close. Long gaps increase pressure."
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_prediction_section(filtered_df: pd.DataFrame):
    transfer_mean = filtered_df["Transfer_Efficiency"].mean()
    discharge_mean = filtered_df["Discharge_Effectiveness"].mean()
    throughput_mean = filtered_df["Pipeline_Throughput"].mean()
    backlog_norm = float(np.clip(filtered_df["Backlog_Rate"].mean() / 10000, 0, 1))

    risk_score = float(
        np.clip((1 - transfer_mean) * 35 + (1 - discharge_mean) * 25 + (1 - throughput_mean) * 25 + backlog_norm * 15, 0, 100)
    )
    risk_label = "High" if risk_score >= 67 else "Medium" if risk_score >= 34 else "Low"

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    render_section_header(
        "Risk Score (Estimate)",
        "Simple heuristic score to flag possible delay risk.",
    )
    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={"text": "Placement Delay Risk Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": THEME["danger"]},
                "steps": [
                    {"range": [0, 34], "color": "#D1FAE5"},
                    {"range": [34, 67], "color": "#FEF3C7"},
                    {"range": [67, 100], "color": "#FEE2E2"},
                ],
            },
        )
    )
    gauge.update_layout(height=300, margin={"t": 50, "b": 10, "l": 10, "r": 10})
    st.plotly_chart(gauge, use_container_width=True)
    st.markdown(
        f"**Risk Band:** {risk_label}. Use this as an early warning indicator for additional staffing or transfer support."
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_about_section(filtered_df: pd.DataFrame):
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    render_section_header(
        "About This Project",
        "Short summary of what I built and how I approached it.",
    )
    st.markdown(
        f"""
        **Project:** Care Transition Analytics Dashboard  
        **Dataset:** HHS Unaccompanied Children Program (`{len(filtered_df):,}` filtered records in current view)  
        **What this dataset includes:** Intake, custody, transfers, HHS care census, and discharges  
        **Tools used:** Streamlit, Pandas, NumPy, Matplotlib, Plotly  
        **Built by:** Rajoli Vishnu Vardan Redy  
        **Purpose:** Identify bottlenecks, monitor backlog pressure, and support practical operational decisions.  
        **Method:** Clean data -> calculate KPIs -> review trend charts -> create alerts -> write recommendations.  
        **Limitations:** This dataset has no patient-level readmission or true length-of-stay records, so those are shown as estimates.
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_header():
    st.markdown(
        """
        <div class="hero-banner">
            <div class="hero-tag">Data Analyst Project Dashboard</div>
            <h1 class="hero-title">Care Transition Efficiency & Placement Outcome Analytics</h1>
            <div class="hero-subtitle">
                This dashboard tracks how children move through the UAC pipeline. It focuses on transfer
                efficiency, discharge performance, throughput, and backlog across CBP custody, HHS care,
                and sponsor placement stages.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def convert_df_to_csv(data: pd.DataFrame) -> bytes:
    export_df = data.copy()
    export_df["Date"] = export_df["Date"].dt.strftime("%Y-%m-%d")
    return export_df.to_csv(index=False).encode("utf-8")


def render_overview_strip(filtered_df: pd.DataFrame):
    start_date = filtered_df["Date"].min().date()
    end_date = filtered_df["Date"].max().date()
    average_intake = filtered_df["Children apprehended and placed in CBP custody"].mean()
    average_discharge = filtered_df["Children discharged from HHS Care"].mean()
    max_hhs_care = filtered_df["Children in HHS Care"].max()

    st.markdown(
        f"""
        <div class="overview-grid">
            <div class="overview-card" style="--metric-accent:#2F5BEA; --metric-border:#D7E3FF; --metric-bg-start:#FFFFFF; --metric-bg-end:#EEF4FF;">
                <div class="overview-label">Selected Period</div>
                <div class="overview-value">{start_date} to {end_date}</div>
                <div class="overview-subtext">Date range used in the dashboard</div>
            </div>
            <div class="overview-card" style="--metric-accent:#2DBE7E; --metric-border:#CFEFDF; --metric-bg-start:#FFFFFF; --metric-bg-end:#F0FFF7;">
                <div class="overview-label">Average Intake</div>
                <div class="overview-value">{average_intake:.1f}</div>
                <div class="overview-subtext">Children entering CBP custody</div>
            </div>
            <div class="overview-card" style="--metric-accent:#FF9F43; --metric-border:#FFE0BF; --metric-bg-start:#FFFFFF; --metric-bg-end:#FFF5EA;">
                <div class="overview-label">Average Discharge</div>
                <div class="overview-value">{average_discharge:.1f}</div>
                <div class="overview-subtext">Children discharged from HHS care</div>
            </div>
            <div class="overview-card" style="--metric-accent:#7A5AF8; --metric-border:#E6DEFF; --metric-bg-start:#FFFFFF; --metric-bg-end:#F5F1FF;">
                <div class="overview-label">Peak HHS Care</div>
                <div class="overview-value">{int(max_hhs_care):,}</div>
                <div class="overview-subtext">Highest number of children in HHS care</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_filters(df: pd.DataFrame):
    st.sidebar.markdown(
        '<div class="filter-panel-title">Filter Panel</div>',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        """
        <div class="sidebar-panel">
            <div class="sidebar-title">Dashboard Filters</div>
            <div style="font-size:0.88rem; opacity:0.9;">
                Select the date range for all metrics and visualizations.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    date_selection = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # Streamlit can return a single date or a date range depending on user interaction.
    if isinstance(date_selection, tuple):
        if len(date_selection) == 2:
            start_date, end_date = date_selection
        elif len(date_selection) == 1:
            start_date = end_date = date_selection[0]
        else:
            start_date, end_date = min_date, max_date
    else:
        start_date = end_date = date_selection

    if start_date > end_date:
        start_date, end_date = end_date, start_date

    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.sidebar.markdown(
        f"""
        <div class="sidebar-panel">
            <div class="sidebar-title">Dataset Overview</div>
            <div style="font-size:0.9rem; line-height:1.8;">
                Records: <strong>{len(df):,}</strong><br>
                From: <strong>{min_date}</strong><br>
                To: <strong>{max_date}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return pd.to_datetime(start_date), pd.to_datetime(end_date)


def render_kpi_cards(filtered_df: pd.DataFrame):
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    render_section_header(
        "Key Performance Indicators",
        "Summary measures for pipeline efficiency and backlog conditions.",
    )

    columns = st.columns(4, gap="large")
    for card_column, kpi in zip(columns, KPI_DETAILS):
        series = filtered_df[kpi["column"]]
        current_value = series.mean()

        card_column.markdown(
            f"""
            <div class="kpi-card" style="--accent: {kpi["color"]};">
                <div class="kpi-row">
                    <div class="kpi-label">{kpi["label"]}</div>
                    <div class="kpi-icon">{kpi["icon"]}</div>
                </div>
                <div class="kpi-value">{format_kpi_value(current_value, kpi["format"])}</div>
                <div class="kpi-note">{kpi["description"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def render_efficiency_section(filtered_df: pd.DataFrame):
    chart_col, text_col = st.columns([1.9, 1], gap="large")

    with chart_col:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        render_section_header(
            "Efficiency Trend Analysis",
            "Transfer efficiency and discharge effectiveness across the selected period.",
        )
        fig = create_line_chart(
            filtered_df,
            ["Transfer_Efficiency", "Discharge_Effectiveness"],
            "Transfer Efficiency and Discharge Effectiveness",
            "Efficiency Rate",
            [THEME["secondary"], THEME["accent"]],
        )
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        st.markdown(
            """
            <div class="chart-caption">
                <strong>Interpretation:</strong> Higher transfer efficiency indicates faster
                movement from CBP custody to HHS care. Higher discharge effectiveness indicates stronger
                discharge performance from HHS care. Lower values may indicate delay at the corresponding
                stage of the pipeline.
            </div>
            """
            ,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with text_col:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        render_section_header(
            "Efficiency Summary",
            "Reference values for the efficiency trend.",
        )
        latest_record = filtered_df.iloc[-1]
        st.markdown(
            """
            <div class="info-box">
                Higher values indicate stronger case movement through the care pipeline and fewer delays
                between operational stages.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="mini-stat">
                <div class="mini-stat-label">Latest Transfer Efficiency</div>
                <div class="mini-stat-value">{latest_record['Transfer_Efficiency']:.2%}</div>
            </div>
            <div class="mini-stat">
                <div class="mini-stat-label">Latest Discharge Effectiveness</div>
                <div class="mini-stat-value">{latest_record['Discharge_Effectiveness']:.2%}</div>
            </div>
            <div class="mini-stat">
                <div class="mini-stat-label">Average Pipeline Throughput</div>
                <div class="mini-stat-value">{filtered_df['Pipeline_Throughput'].mean():.2%}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


def render_backlog_section(filtered_df: pd.DataFrame):
    chart_col, status_col = st.columns([1.8, 1], gap="large")

    with chart_col:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        render_section_header(
            "Backlog Trend Analysis",
            "Backlog trend based on intake volume and discharge volume.",
        )
        fig = create_line_chart(
            filtered_df,
            ["Backlog_Rate"],
            "Backlog Rate Over Time",
            "Number of Children",
            [THEME["danger"]],
        )
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        st.markdown(
            """
            <div class="chart-caption">
                <strong>Interpretation:</strong> Backlog rises when intake exceeds discharge.
                Sustained increases may indicate processing delays, placement constraints, or system
                capacity pressure.
            </div>
            """
            ,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with status_col:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        render_section_header(
            "Bottleneck Alert",
            "Status indicator for transfer performance and backlog pressure.",
        )

        transfer_efficiency_mean = filtered_df["Transfer_Efficiency"].mean()
        average_backlog = filtered_df["Backlog_Rate"].mean()

        if transfer_efficiency_mean < 0.30:
            st.markdown(
                """
                <div class="alert-box">
                    Transfer bottleneck detected: average transfer efficiency is below the 30% threshold.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="info-box">
                    No major transfer bottleneck detected for the selected period.
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div class="mini-stat">
                <div class="mini-stat-label">Average Backlog</div>
                <div class="mini-stat-value">{int(round(average_backlog)):,}</div>
            </div>
            <div class="mini-stat">
                <div class="mini-stat-label">Peak Backlog</div>
                <div class="mini-stat-value">{int(filtered_df['Backlog_Rate'].max()):,}</div>
            </div>
            <div class="mini-stat">
                <div class="mini-stat-label">Minimum Backlog</div>
                <div class="mini-stat-value">{int(filtered_df['Backlog_Rate'].min()):,}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


def render_comparison_section(filtered_df: pd.DataFrame):
    chart_col, summary_col = st.columns([1.9, 1], gap="large")

    with chart_col:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        render_section_header(
            "Intake vs Discharge Comparison",
            "Comparison of CBP intake volume and HHS discharge volume over the selected period.",
        )
        fig = create_comparison_chart(filtered_df)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        st.markdown(
            """
            <div class="chart-caption">
                <strong>Interpretation:</strong> When intake remains consistently above discharge,
                backlog pressure may increase. Smaller gaps indicate improved downstream movement through
                the care pipeline.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with summary_col:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        render_section_header(
            "Comparison Summary",
            "Reference values for intake and discharge activity.",
        )
        intake_mean = filtered_df["Children apprehended and placed in CBP custody"].mean()
        discharge_mean = filtered_df["Children discharged from HHS Care"].mean()
        gap_mean = intake_mean - discharge_mean
        st.markdown(
            f"""
            <div class="mini-stat">
                <div class="mini-stat-label">Average Intake</div>
                <div class="mini-stat-value">{int(round(intake_mean)):,}</div>
            </div>
            <div class="mini-stat">
                <div class="mini-stat-label">Average Discharge</div>
                <div class="mini-stat-value">{int(round(discharge_mean)):,}</div>
            </div>
            <div class="mini-stat">
                <div class="mini-stat-label">Average Gap</div>
                <div class="mini-stat-value">{int(round(gap_mean)):,}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


def render_pipeline_section():
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    render_section_header(
        "Pipeline Flow",
        "Operational flow of children through the care transition process.",
    )
    st.markdown(
        """
        <div class="pipeline-flow">
            <div class="pipeline-stage">
                <div class="pipeline-icon">🚓</div>
                <div class="pipeline-title">CBP Custody</div>
                <div class="pipeline-text">
                    Children are apprehended and placed in CBP custody as the first stage of intake.
                </div>
            </div>
            <div class="pipeline-arrow">→</div>
            <div class="pipeline-stage">
                <div class="pipeline-icon">🏥</div>
                <div class="pipeline-title">HHS Care</div>
                <div class="pipeline-text">
                    Children are transferred into HHS care for case management, support, and supervision.
                </div>
            </div>
            <div class="pipeline-arrow">→</div>
            <div class="pipeline-stage">
                <div class="pipeline-icon">🏠</div>
                <div class="pipeline-title">Sponsor Placement</div>
                <div class="pipeline-text">
                    Children are discharged from HHS care after sponsor placement and related processing.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_insights_section(filtered_df: pd.DataFrame):
    transfer_mean = filtered_df["Transfer_Efficiency"].mean()
    discharge_mean = filtered_df["Discharge_Effectiveness"].mean()
    backlog_trend = filtered_df["Backlog_Rate"].iloc[-1] - filtered_df["Backlog_Rate"].iloc[0]
    throughput_mean = filtered_df["Pipeline_Throughput"].mean()

    transfer_text = (
        "Transfer efficiency remains stable during the selected period."
        if transfer_mean >= 0.30
        else "Transfer efficiency is below the threshold, indicating slower movement from CBP custody to HHS care."
    )
    placement_text = (
        "Discharge effectiveness indicates consistent sponsor placement and discharge activity."
        if discharge_mean >= 0.01
        else "Discharge effectiveness remains limited, suggesting slower sponsor placement and case completion."
    )
    backlog_text = (
        "Backlog levels increased across the selected period, indicating continued accumulation in the system."
        if backlog_trend > 0
        else "Backlog levels remained stable or declined across the selected period."
    )
    transfer_action = (
        "Prioritize transfers from high-volume CBP sites and monitor facilities with transfer efficiency below 30% weekly."
        if transfer_mean < 0.30
        else "Sustain current transfer workflows and replicate high-performing site practices in lower-performing regions."
    )
    placement_action = (
        "Expand sponsor outreach and case documentation support to reduce discharge delays."
        if discharge_mean < 0.01
        else "Protect current discharge momentum by tracking time-to-placement and preventing case review bottlenecks."
    )
    backlog_action = (
        "Trigger surge capacity planning where intake exceeds discharge for multiple periods."
        if backlog_trend > 0
        else "Use this window to clear legacy backlog and maintain discharge volume above intake."
    )

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    render_section_header(
        "Insights",
        "Key observations based on the filtered results.",
    )
    st.markdown(
        f"""
        <div class="insight-item">
            <div class="insight-title">Transfer Efficiency Trend</div>
            <div class="insight-text">
                Average transfer efficiency is {transfer_mean:.2%}. {transfer_text}
                <br><strong>Recommended action:</strong> {transfer_action}
            </div>
        </div>
        <div class="insight-item">
            <div class="insight-title">Sponsor Placement and Discharge</div>
            <div class="insight-text">
                Average discharge effectiveness is {discharge_mean:.2%} and average pipeline throughput is
                {throughput_mean:.2%}. {placement_text}
                <br><strong>Recommended action:</strong> {placement_action}
            </div>
        </div>
        <div class="insight-item">
            <div class="insight-title">Backlog Accumulation Pattern</div>
            <div class="insight-text">
                The net change in backlog across the selected period is {int(round(backlog_trend)):,}.
                {backlog_text}
                <br><strong>Recommended action:</strong> {backlog_action}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_footer(filtered_df: pd.DataFrame, start_date: pd.Timestamp, end_date: pd.Timestamp):
    st.markdown(
        f"""
        <hr class="footer-divider">
        <div class="footer">
            <div class="footer-title">Care Transition Efficiency & Placement Outcome Analytics</div>
            <div class="footer-subtitle">B.Tech Final Year Internship Project</div>
            <div class="footer-name-label">Developed by:</div>
            <div class="footer-name">RAJOLI VISHNU VARDAN REDY</div>
            <div class="footer-program">Unified Mentor Internship Program</div>
            <div class="footer-program">Selected date range: {start_date.date()} to {end_date.date()} | Records displayed: {len(filtered_df):,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_dashboard():
    inject_css()

    raw_df = load_data()
    cleaned_df = clean_data(raw_df)
    analytics_df = calculate_kpis(cleaned_df)

    start_date, end_date = render_sidebar_filters(analytics_df)

    filtered_df = analytics_df[
        (analytics_df["Date"] >= start_date) & (analytics_df["Date"] <= end_date)
    ].copy()

    render_header()

    if filtered_df.empty:
        st.error("No data is available for the selected date range.")
        return

    st.markdown('<div class="download-wrap">', unsafe_allow_html=True)
    st.download_button(
        label="Download Filtered Data (CSV)",
        data=convert_df_to_csv(filtered_df),
        file_name="care_transition_filtered_data.csv",
        mime="text/csv",
        use_container_width=False,
    )
    st.markdown("</div>", unsafe_allow_html=True)
    render_kpi_cards(filtered_df)
    render_portfolio_kpi_cards(filtered_df)

    tab_overview, tab_monitor, tab_analysis, tab_prediction, tab_about = st.tabs(
        ["Overview", "Monitor", "Analysis", "Risk", "About"]
    )

    with tab_overview:
        render_overview_strip(filtered_df)
        render_efficiency_section(filtered_df)
        render_backlog_section(filtered_df)
        render_storytelling_section(filtered_df)

    with tab_monitor:
        render_realtime_monitor(filtered_df)
        render_comparison_section(filtered_df)
        render_drilldown_section(filtered_df)

    with tab_analysis:
        render_plotly_charts(filtered_df)
        render_pipeline_section()
        render_insights_section(filtered_df)

    with tab_prediction:
        render_prediction_section(filtered_df)

    with tab_about:
        render_about_section(filtered_df)

    render_footer(filtered_df, start_date, end_date)


if __name__ == "__main__":
    build_dashboard()
