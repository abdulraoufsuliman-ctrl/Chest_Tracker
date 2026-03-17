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

# ===== زر النقاط المستخدمة =====



# ================== CSS المطور لتحسين المظهر ==================
image_url = "https://raw.githubusercontent.com/abdulraoufsuliman-ctrl/Chest_Tracker/main/imageBack.png"  # ضع رابط صورتك هنا

st.markdown(f"""
<style>

/* ===== الخلفية العامة ===== */
.stApp {{
    background-image: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)), url("{image_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* ===== الحاوية الرئيسية ===== */
.block-container {{
    padding-top: 0.5rem;
    max-width: 95%;
    background-color: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 15px;
}}

/* ===== الهيدر ===== */
.header {{
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 25px;
}}

.logo {{
    width: 70px;
}}

.title {{
    font-size: 38px;
    font-weight: 900;
    color: #ffd700 !important;
    text-shadow: 2px 2px 6px #000;
    letter-spacing: 3px;
}}

/* ===== التابات ===== */
[data-testid="stTab"] {{
    height: 45px;
    background-color: rgba(255,255,255,0.1) !important;
    color: white !important;
    border-radius: 8px 8px 0 0 !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    padding: 0 30px !important;
}}

[data-testid="stTab"][aria-selected="true"] {{
    background: linear-gradient(135deg, #4f8cff, #3b6df2) !important;
    color: white !important;
}}

/* ===== الجدول ===== */
.stDataFrame {{
    background-color: rgba(255,255,255,0.92) !important;
    border-radius: 10px !important;
}}

</style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
logo_url = "https://raw.githubusercontent.com/abdulraoufsuliman-ctrl/Chest_Tracker/main/logo.png"

st.markdown(f"""
<div class="header">
    <img src="{logo_url}" class="logo">
    <div class="title">[RUM] BOTTLES AND BATTLE</div>
</div>
""", unsafe_allow_html=True)

#=============================================
def get_file_modified_time(file_name):
    ts = os.path.getmtime(file_name)
    dt = datetime.fromtimestamp(ts) + timedelta(hours=2)
    return dt.strftime("%Y-%m-%d %H:%M (UTC+2)")

# ================== دالة تلوين الخلايا ==================
def highlight_cells(val):
    if isinstance(val, (int, float)):
        if val > 0:
            return (
                "background-color: #e6f4ea;"
                "color: #1e7f43;"
                "font-weight: 600;"
                "text-align: center;"
            )
        else:
            return (
                "background-color: #fce8e6;"
                "color: #c5221f;"
                "font-weight: 600;"
                "text-align: center;"
            )
    return "text-align: center;"

def highlight_points_normal(val):
    if not isinstance(val, (int, float)):
        return "text-align: center;"

    if val == 0:
        return (
            "background-color: #fce8e6;"
            "color: #c5221f;"
            "font-weight: 700;"
            "text-align: center;"
        )
    elif 0 < val < 2500:
        return (
            "background-color: #fff4ce;"
            "color: #7a5c00;"
            "font-weight: 700;"
            "text-align: center;"
        )
    else:  # >= 2500
        return (
            "background-color: #e6f4ea;"
            "color: #1e7f43;"
            "font-weight: 700;"
            "text-align: center;"
        )
        
def highlight_points_castle(val):
    if not isinstance(val, (int, float)):
        return "text-align: center;"

    if val > 0:
        return (
            "background-color: #e6f4ea;"
            "color: #1e7f43;"
            "font-weight: 700;"
            "text-align: center;"
        )
    elif val == 0:
        return (
            "background-color: #fce8e6;"
            "color: #c5221f;"
            "font-weight: 700;"
            "text-align: center;"
        )
    else:  # val < 0
        return (
            "background-color: #fce8e6;"
            "color: #c5221f;"
            "font-weight: 700;"
            "text-align: center;"
        )


# ================== دالة تحميل وعرض البيانات ==================
def load_and_display(file_name, is_castle=False):
    try:
        # قراءة البيانات
        df = pd.read_excel(file_name, sheet_name="Results")
        
        # تحويل الأعمدة الرقمية وتنسيقها
        num_cols = df.select_dtypes(include="number").columns
        for col in num_cols:
            # تحويل القيم إلى أعداد صحيحة (بدون فاصلة عشرية)
            df[col] = df[col].fillna(0).astype(int)

        # اختيار دالة التلوين المناسبة للنقاط
        if is_castle:
            points_highlight_func = highlight_points_castle
        else:
            points_highlight_func = highlight_points_normal

        # تنسيق الستايل
        styled_df = (
            df.style
            .format("{:,}", subset=num_cols)
        
            # تلوين عمود Points بشروط خاصة
            .applymap(points_highlight_func, subset=["Points"])
        
            # تلوين بقية الأعمدة الرقمية
            .applymap(highlight_cells, subset=df.columns[2:])
        
            .set_properties(**{
                "border": "1px solid #e0e0e0",
                "font-size": "14px"
            })
        )

        st.dataframe(
            styled_df,
            use_container_width=True,
            height=600,
            hide_index=True
        )
    except Exception as e:
        st.error(f"Error loading {file_name}: {e}")

# ================== Tabs (الفترات) ==================
# تأكدنا هنا أن أسماء الفترات مكتوبة بوضوح
tab1, tab2, tab3, tab4 = st.tabs(["P1 (8-14)", "P2 (14-20)",  "P3 (20-26)", "Castle Competition"])
#tab1, tab2, tab3, tab4 = st.tabs(["Period 1", "Period 2",  "Period 3", "Castle Competition"])
with tab1:
    st.markdown(
        f"<div class='tabs-date'>Last update: {get_file_modified_time('Results1.xlsx')}</div>",
        unsafe_allow_html=True
    )
    load_and_display("Results1.xlsx", is_castle=False)

with tab2:
    st.markdown(
        f"<div class='tabs-date'>Last update: {get_file_modified_time('Results2.xlsx')}</div>",
        unsafe_allow_html=True
    )
    load_and_display("Results2.xlsx", is_castle=False)

with tab3:
    st.markdown(
        f"<div class='tabs-date'>Last update: {get_file_modified_time('Results3.xlsx')}</div>",
        unsafe_allow_html=True
    )
    load_and_display("Results3.xlsx", is_castle=False)


with tab4:
    st.markdown(
        f"<div class='tabs-date'>Last update: {get_file_modified_time('Results_Castle.xlsx')}</div>",
        unsafe_allow_html=True
    )
    load_and_display("Results_Castle.xlsx", is_castle=True)
















