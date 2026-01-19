import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
# ================== إعداد الصفحة ==================
st.set_page_config(
    page_title="Player Results",
    layout="wide"
)

# ================== CSS المطور لتحسين المظهر ==================
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

/* تقليل الفراغ العلوي وتوسيط المحتوى */
.block-container {
    padding-top: 1.5rem;
    max-width: 95%;
}

/* Header layout */
.header {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 25px;
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

/* ================== إزالة الخط السفلي للتابات وجعلها ملتصقة ================== */

/* إزالة الخط الممتد تحت التابات */
[data-testid="stTabs"] {
    border-bottom: none !important;
}

/* إزالة المسافة الفاصلة بين التابات والمحتوى (الجدول) */
[data-testid="stTabContent"] {
    padding-top: 0px !important;
}

/* إزالة الخط السفلي الافتراضي من Streamlit */
[data-testid="stTabs"] [data-baseweb="tab-border"] {
    display: none !important;
}

/* تنسيق حاوية التابات */
[data-testid="stTabs"] [role="tablist"] {
    gap: 5px; 
}

/* تصميم التاب الفردي */
[data-testid="stTab"] {
    height: 45px;
    background-color: #f0f2f6; /* لون خلفية خفيف للتابات غير النشطة */
    color: #31333F !important; /* إظهار النص بوضوح */
    border-radius: 8px 8px 0 0 !important; /* حواف علوية دائرية قليلاً */
    border: 1px solid #ddd !important;
    border-bottom: none !important;
    padding: 0 30px !important;
    font-weight: 600;
}

/* التاب النشط */
[data-testid="stTab"][aria-selected="true"] {
    background: linear-gradient(135deg, #4f8cff, #3b6df2) !important;
    color: white !important;
    border-color: #3b6df2 !important;
}

/* إزالة الخط الملون المتحرك تحت التاب */
[data-testid="stTab"] div[data-baseweb="tab-highlight"] {
    display: none !important;
}
/* صف التابات + التاريخ */
.tabs-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: -6px;   /* دمج مع الجدول */
}

/* التاريخ */
.tabs-date {
    font-size: 12px;
    color: #5f6368;
    white-space: nowrap;
}


/* ================== تنسيق الجدول (حواف حادة) ================== */
.stDataFrame {
    margin-top: -1px !important; /* سحب الجدول للأعلى ليلتصق بالتابات */
}

/* حواف حادة للجدول */
[data-testid="stTable"] , [data-testid="stDataFrame"] {
    border: 1px solid #ddd !important;
    border-radius: 0px !important; 
}

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

def highlight_points(val):
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



# ================== دالة تحميل وعرض البيانات ==================
def load_and_display(file_name):
    try:
        # قراءة البيانات
        df = pd.read_excel(file_name, sheet_name="Results")
        
        # تنظيف البيانات
        df = df.dropna(how="all", axis=0).dropna(how="all", axis=1)

        # تحويل الأعمدة الرقمية وتنسيقها
        num_cols = df.select_dtypes(include="number").columns
        df[num_cols] = df[num_cols].fillna(0)

        # تنسيق الستايل
        styled_df = (
            df.style
            .format("{:,}", subset=num_cols)
        
            # تلوين عمود Points بشروط خاصة
            .applymap(highlight_points, subset=["Points"])
        
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
tab1, tab2 = st.tabs(["Period 1", "Period 2"])

with tab1:
    st.markdown(
        f"<div class='tabs-date'>Last update: {get_file_modified_time('Results1.xlsx')}</div>",
        unsafe_allow_html=True
    )
    load_and_display("Results1.xlsx")

with tab2:
    st.markdown(
        f"<div class='tabs-date'>Last update: {get_file_modified_time('Results2.xlsx')}</div>",
        unsafe_allow_html=True
    )
    load_and_display("Results2.xlsx")







