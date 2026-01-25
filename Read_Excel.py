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

/* Header layout */
.header-container {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 15px;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
}

.logo {
    width: 50px;
    height: auto;
}

.title {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: 1px;
    color: #000000;
}

/* Ultra Small Chest Points Button - Force strict sizing */
div[data-testid="stButton"] > button {
    height: 25px !important;
    min-height: 25px !important;
    line-height: 1 !important;
    padding: 0px 8px !important;
    font-size: 9px !important;
    border-radius: 4px !important;
    background-color: white !important;
    color: #31333F !important;
    border: 1px solid #ddd !important;
    font-weight: 500 !important;
    margin-top: 5px !important;
}

div[data-testid="stButton"] > button:hover {
    border-color: #4f8cff !important;
    color: #4f8cff !important;
}

/* Tab Design */
[data-testid="stTabs"] [data-baseweb="tab-border"] {
    display: none !important;
}

[data-testid="stTab"] {
    height: 38px;
    background-color: #f0f2f6; 
    border-radius: 8px 8px 0 0 !important; 
    border: 1px solid #ddd !important;
    border-bottom: none !important;
    padding: 0 20px !important;
    font-weight: 600;
}

[data-testid="stTab"][aria-selected="true"] {
    background: linear-gradient(135deg, #4f8cff, #3b6df2) !important;
    color: white !important;
}

.tabs-date {
    font-size: 11px;
    color: #5f6368;
    margin-bottom: 8px;
}

[data-testid="stTable"] , [data-testid="stDataFrame"] {
    border: 1px solid #ddd !important;
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

# 1. Top Bar - Using a very small column for the button (0.08) to prevent stretching
t1, t2 = st.columns([0.92, 0.08])
with t2:
    # Removed use_container_width to let CSS control the width
    st.button("📊 Chest", on_click=open_modal)

# 2. Main Header
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
        
        if st.button("Close ✖️", on_click=close_modal):
            st.rerun()
    st.markdown("---")

# ================== Main Functions ==================
def get_file_modified_time(file_name):
    try:
        ts = os.path.getmtime(file_name)
        dt = datetime.fromtimestamp(ts) + timedelta(hours=2)
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return "N/A"

def load_and_display(file_name, is_castle=False):
    try:
        df = pd.read_excel(file_name, sheet_name="Results")
        num_cols = df.select_dtypes(include="number").columns
        for col in num_cols:
            df[col] = df[col].fillna(0).astype(int)
        
        # Color coding functions (Simplified for display)
        def style_points(val):
            if not isinstance(val, (int, float)): return ""
            if val <= 0: return "background-color: #fce8e6; color: #c5221f; font-weight: 700;"
            return "background-color: #e6f4ea; color: #1e7f43; font-weight: 700;"

        styled_df = (
            df.style
            .format("{:,}", subset=num_cols)
            .applymap(style_points, subset=["Points"])
            .set_properties(**{"text-align": "center", "border": "1px solid #e0e0e0"})
        )
        st.dataframe(styled_df, use_container_width=True, height=600, hide_index=True)
    except Exception as e:
        st.error(f"Error: {e}")

# ================== Tabs ==================
tab1, tab2, tab3, tab4 = st.tabs(["Period 1", "Period 2", "Period 3", "Castle"])

for i, tab in enumerate([tab1, tab2, tab3, tab4], 1):
    with tab:
        fname = f"Results{i}.xlsx" if i < 4 else "Results_Castle.xlsx"
        st.markdown(f"<div class='tabs-date'>Update: {get_file_modified_time(fname)}</div>", unsafe_allow_html=True)
        load_and_display(fname, is_castle=(i==4))

