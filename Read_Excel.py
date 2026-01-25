import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# ================== إعداد الصفحة ==================
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

# ================== CSS المطور لتحسين المظهر والنافذة المنبثقة ==================
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

/* تقليل الفراغ العلوي وتوسيط المحتوى */
.block-container {
    padding-top: 0.1rem;
    max-width: 95%;
}

/* Header layout */
.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 20px;
}

.logo {
    width: 70px;
    height: auto;
}

.title {
    font-size: 35px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #000000;
    line-height: 2.9;
    padding-top: 4px;
}

/* زر نقاط الصندوق */
.stButton>button {
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 600;
}

/* إزالة الخط السفلي للتابات وجعلها ملتصقة */
[data-testid="stTabs"] [data-baseweb="tab-border"] {
    display: none !important;
}

[data-testid="stTabs"] [role="tablist"] {
    gap: 5px; 
}

[data-testid="stTab"] {
    height: 45px;
    background-color: #f0f2f6; 
    color: #31333F !important; 
    border-radius: 8px 8px 0 0 !important; 
    border: 1px solid #ddd !important;
    border-bottom: none !important;
    padding: 0 30px !important;
    font-weight: 600;
}

[data-testid="stTab"][aria-selected="true"] {
    background: linear-gradient(135deg, #4f8cff, #3b6df2) !important;
    color: white !important;
    border-color: #3b6df2 !important;
}

.tabs-date {
    font-size: 12px;
    color: #5f6368;
    white-space: nowrap;
    margin-bottom: 10px;
    text-align: Left;
}

.stDataFrame {
    margin-top: -1px !important; 
}

[data-testid="stTable"] , [data-testid="stDataFrame"] {
    border: 1px solid #ddd !important;
    border-radius: 0px !important; 
}

/* تنسيق النافذة المنبثقة المخصصة */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    z-index: 9999;
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal-content {
    background: white;
    padding: 20px;
    border-radius: 12px;
    width: 80%;
    max-height: 80vh;
    overflow-y: auto;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
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

# ================== HEADER ==================
logo_url = "https://raw.githubusercontent.com/abdulraoufsuliman-ctrl/Chest_Tracker/main/logo.png"

# استخدام أعمدة streamlit لوضع الزر في الهيدر بجانب العنوان
col_header, col_btn = st.columns([0.8, 0.2])

with col_header:
    st.markdown(f"""
    <div class="header-left">
        <img src="{logo_url}" class="logo">
        <div class="title">[RUM] BOTTLES AND BATTLE</div>
    </div>
    """, unsafe_allow_html=True)

with col_btn:
    st.write("<br>", unsafe_allow_html=True) # موازنة المسافة
    if st.button("📊 نقاط الصندوق", on_click=open_modal, use_container_width=True):
        pass

# ================== النافذة المنبثقة (Modal) ==================
if st.session_state.show_modal:
    with st.container():
        # محاكاة نافذة منبثقة فوق المحتوى
        st.markdown("---")
        modal_cols = st.columns([0.1, 0.8, 0.1])
        with modal_cols[1]:
            st.subheader("📋 نقاط الصندوق المستخدمة")
            
            try:
                # قراءة ملف Used_Points.xlsx
                df_used = pd.read_excel("Used_Points.xlsx", sheet_name="Points")
                
                # تنظيف البيانات (أرقام صحيحة)
                num_cols_used = df_used.select_dtypes(include="number").columns
                for col in num_cols_used:
                    df_used[col] = df_used[col].fillna(0).astype(int)
                
                # عرض الجدول
                st.dataframe(df_used, use_container_width=True, hide_index=True, height=400)
                
            except Exception as e:
                st.error(f"خطأ في تحميل ملف Used_Points.xlsx: {e}")
            
            if st.button("إغلاق الشاشة ✖️", on_click=close_modal):
                st.rerun()
        st.markdown("---")

# ================== دالة تلوين الخلايا (الكود الأصلي) ==================
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

# ================== دالة تحميل وعرض البيانات ==================
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

# ================== Tabs (الفترات) ==================
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
