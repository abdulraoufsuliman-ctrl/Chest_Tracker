import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# ================== Page Setup ==================
st.set_page_config(
    page_title="Player Results",
    layout="wide"
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ================== Enhanced CSS for UI and Modal ==================
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

/* Reduce top padding and center content */
.block-container {
    padding-top: 0rem;
    max-width: 95%;
}

/* New Top Settings Bar */
.settings-bar {
    display: flex;
    justify-content: flex-end;
    padding: 10px 0;
    margin-bottom: -10px;
}

/* Header layout */
.header-container {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 25px;
    border-bottom: 1px solid #eee;
    padding-bottom: 15px;
}

.logo {
    width: 60px;
    height: auto;
}

.title {
    font-size: 32px;
    font-weight: 800;
    letter-spacing: 1px;
    color: #000000;
}

/* Smaller Chest Points Button */
div[data-testid="stButton"] > button {
    height: 15px;
    padding: 0px 5px !important;
    font-size: 8px !important;
    border-radius: 6px !important;
    background-color: white !important;
    color: #31333F !important;
    border: 1px solid #ddd !important;
    font-weight: 500 !important;
}

div[data-testid="stButton"] > button:hover {
    border-color: #4f8cff !important;
    color: #4f8cff !important;
}

/* Remove Tab Bottom Border and make them connected */
[data-testid="stTabs"] [data-baseweb="tab-border"] {
    display: none !important;
}

[data-testid="stTabs"] [role="tablist"] {
    gap: 5px; 
}

/* Individual Tab Design */
[data-testid="stTab"] {
    height: 40px;
    background-color: #f0f2f6; 
    color: #31333F !important; 
    border-radius: 8px 8px 0 0 !important; 
    border: 1px solid #ddd !important;
    border-bottom: none !important;
    padding: 0 25px !important;
    font-weight: 600;
    font-size: 14px;
}

/* Active Tab */
[data-testid="stTab"][aria-selected="true"] {
    background: linear-gradient(135deg, #4f8cff, #3b6df2) !important;
    color: white !important;
    border-color: #3b6df2 !important;
}

/* Date Display */
.tabs-date {
    font-size: 12px;
    color: #5f6368;
    white-space: nowrap;
    margin-bottom: 10px;
    text-align: left;
}

/* Table Alignment */
.stDataFrame {
    margin-top: -1px !important; 
}

[data-testid="stTable"] , [data-testid="stDataFrame"] {
    border: 1px solid #ddd !important;
    border-radius: 0px !important; 
}

</style>
""", unsafe_allow_html=True)

# ================== State Management ==================
if 'show_modal' not in st.session_state:
    st.session_state.show_modal = False

def open_modal():
    st.session_state.show_modal = True

def close_modal():
    st.session_state.show_modal = False

# ================== TOP SETTINGS BAR & HEADER ==================

# 1. Top Bar for the Button
t1, t2 = st.columns([0.85, 0.15])
with t2:
    if st.button("📊 Chest Points", on_click=open_modal, use_container_width=True):
        pass

# 2. Main Header (Logo + Title)
logo_url = "https://raw.githubusercontent.com/abdulraoufsuliman-ctrl/Chest_Tracker/main/logo.png"
st.markdown(f"""
<div class="header-container">
    <img src="{logo_url}" class="logo">
    <div class="title">[RUM] BOTTLES AND BATTLE</div>
</div>
""", unsafe_allow_html=True)

# ================== Points Modal ==================
if st.session_state.show_modal:
    st.markdown("---")
    m_col1, m_col2, m_col3 = st.columns([0.1, 0.8, 0.1])
    with m_col2:
        st.subheader("📋 Used Chest Points")
        try:
            df_used = pd.read_excel("Used_Points.xlsx", sheet_name="Points")
            num_cols_used = df_used.select_dtypes(include="number").columns
            for col in num_cols_used:
                df_used[col] = df_used[col].fillna(0).astype(int)
            st.dataframe(df_used, use_container_width=True, hide_index=True, height=400)
        except Exception as e:
            st.error(f"Error loading Used_Points.xlsx: {e}")
        
        if st.button("Close Screen ✖️", on_click=close_modal):
            st.rerun()
    st.markdown("---")

# ================== Helper Functions ==================
def get_file_modified_time(file_name):
    try:
        ts = os.path.getmtime(file_name)
        dt = datetime.fromtimestamp(ts) + timedelta(hours=2)
        return dt.strftime("%Y-%m-%d %H:%M (UTC+2)")
    except:
        return "N/A"

def highlight_cells(val):
    if isinstance(val, (int, float)):
        if val > 0:
            return "background-color: #e6f4ea; color: #1e7f43; font-weight: 600; text-align: center;"
        else:
            return "background-color: #fce8e6; color: #c5221f; font-weight: 600; text-align: center;"
    return "text-align: center;"

def highlight_points_normal(val):
    if not isinstance(val, (int, float)): return "text-align: center;"
    if val == 0: return "background-color: #fce8e6; color: #c5221f; font-weight: 700; text-align: center;"
    elif 0 < val < 2500: return "background-color: #fff4ce; color: #7a5c00; font-weight: 700; text-align: center;"
    else: return "background-color: #e6f4ea; color: #1e7f43; font-weight: 700; text-align: center;"

def highlight_points_castle(val):
    if not isinstance(val, (int, float)): return "text-align: center;"
    if val >= 0: return "background-color: #e6f4ea; color: #1e7f43; font-weight: 700; text-align: center;"
    else: return "background-color: #fce8e6; color: #c5221f; font-weight: 700; text-align: center;"

# ================== Main Data Loading & Display ==================
def load_and_display(file_name, is_castle=False):
    try:
        df = pd.read_excel(file_name, sheet_name="Results")
        num_cols = df.select_dtypes(include="number").columns
        for col in num_cols:
            df[col] = df[col].fillna(0).astype(int)

        points_highlight_func = highlight_points_castle if is_castle else highlight_points_normal

        styled_df = (
            df.style
            .format("{:,}", subset=num_cols)
            .applymap(points_highlight_func, subset=["Points"])
            .applymap(highlight_cells, subset=df.columns[2:])
            .set_properties(**{"border": "1px solid #e0e0e0", "font-size": "14px"})
        )

        st.dataframe(styled_df, use_container_width=True, height=600, hide_index=True)
    except Exception as e:
        st.error(f"Error loading {file_name}: {e}")

# ================== Tabs (Periods) ==================
tab1, tab2, tab3, tab4 = st.tabs(["Period 1", "Period 2", "Period 3", "Castle Competition"])

with tab1:
    st.markdown(f"<div class='tabs-date'>Last update: {get_file_modified_time('Results1.xlsx')}</div>", unsafe_allow_html=True)
    load_and_display("Results1.xlsx", is_castle=False)

with tab2:
    st.markdown(f"<div class='tabs-date'>Last update: {get_file_modified_time('Results2.xlsx')}</div>", unsafe_allow_html=True)
    load_and_display("Results2.xlsx", is_castle=False)

with tab3:
    st.markdown(f"<div class='tabs-date'>Last update: {get_file_modified_time('Results3.xlsx')}</div>", unsafe_allow_html=True)
    load_and_display("Results3.xlsx", is_castle=False)

with tab4:
    st.markdown(f"<div class='tabs-date'>Last update: {get_file_modified_time('Results_Castle.xlsx')}</div>", unsafe_allow_html=True)
    load_and_display("Results_Castle.xlsx", is_castle=True)





