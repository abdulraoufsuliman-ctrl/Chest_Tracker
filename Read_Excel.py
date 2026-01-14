import streamlit as st
import pandas as pd

# ================== إعداد الصفحة ==================
st.set_page_config(
    page_title="Player Results",
    layout="wide"
)

# ================== CSS ==================
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

/* تقليل الفراغ العلوي */
.block-container {
    padding-top: 1.5rem;
}

/* Header layout */
.header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 12px;
    padding-top: 10px;
}

.logo {
    width: 80px;
    height: auto;
    display: block;
}

.title {
    font-size: 35px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #000000;
    line-height: 2.9;
    padding-top: 4px;
}

/* تثبيت العمود الأول في الجدول */
[data-testid="stDataFrame"] {
    overflow-x: auto !important;
}

[data-testid="stDataFrame"] table {
    min-width: 100%;
    border-collapse: separate !important;
    border-spacing: 0 !important;
}

/* تثبيت العمود الأول */
[data-testid="stDataFrame"] table thead tr th:first-child,
[data-testid="stDataFrame"] table tbody tr td:first-child {
    position: sticky !important;
    left: 0 !important;
    background-color: white !important;
    z-index: 10 !important;
    border-right: 2px solid #e0e0e0 !important;
    box-shadow: 2px 0 5px -2px rgba(0,0,0,0.1) !important;
}

/* رأس العمود الثابت */
[data-testid="stDataFrame"] table thead tr th:first-child {
    z-index: 20 !important;
    top: 0 !important;
}

/* تأكد من أن المحتوى محاذي بشكل صحيح */
[data-testid="stDataFrame"] table th:first-child,
[data-testid="stDataFrame"] table td:first-child {
    min-width: 120px !important;
    max-width: 120px !important;
    white-space: nowrap !important;
}

/* خلايا إيجابية وسلبية */
[data-testid="stDataFrame"] td[data-testid="StyledDataCell"] {
    text-align: center !important;
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

# ================== تحميل البيانات ==================
file_name = "Results.xlsx"
sheet_target = "Results"

df = pd.read_excel(file_name, sheet_name=sheet_target)

# حذف الصفوف والأعمدة الفارغة
df = df.dropna(how="all", axis=0).dropna(how="all", axis=1)

# تحويل الأعمدة الرقمية لأعداد صحيحة
num_cols = df.select_dtypes(include="number").columns
df[num_cols] = df[num_cols].fillna(0).astype(int)

# ترتيب حسب العمود الثاني (النقاط)
df = df.dropna(subset=[df.columns[1]])
df = df.sort_values(by=df.columns[1], ascending=False)
df = df.reset_index(drop=True)

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

# ================== تنسيق الجدول ==================
styled_df = (
    df.style
    .format("{:,}", subset=num_cols)
    .applymap(highlight_cells, subset=df.columns[2:])
    .set_properties(**{
        "border": "1px solid #e0e0e0",
        "font-size": "14px"
    })
)

# ================== عرض الجدول ==================
st.dataframe(
    styled_df,
    use_container_width=True,
    height=600,
    hide_index=True
)
