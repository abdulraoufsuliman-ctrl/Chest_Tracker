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

/* Header */
.header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding-top: 10px;
    margin-bottom: 16px;
}

.logo {
    width: 70px;
    height: auto;
    display: block;
}

.title {
    font-size: 40px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #000000;
    line-height: 2.2;
    padding-top: 4px;   /* ✅ أمان إضافي */

}

/* جدول */
.stDataFrame {
    background-color: #ffffff;
    border: 1px solid #dadce0;
    border-radius: 0px;
}

.stDataFrame thead th {
    background-color: #e0e3e7;
    color: #1f1f1f;
    font-weight: 600;
    text-align: center;
}
.stDataFrame tbody td:nth-child(1),
.stDataFrame thead th:nth-child(1) {
    position: sticky;
    left: 0;
    z-index: 12;
    background-color: #f1f3f4;
    text-align: center;
    border-right: 1px solid #c4c7cc;
}

/* ===== تثبيت عمود Name (العمود الثاني) ===== */
.stDataFrame tbody td:nth-child(2),
.stDataFrame thead th:nth-child(2) {
    position: sticky;
    left: 48px;              /* عرض عمود الترقيم */
    z-index: 11;
    background-color: #f1f3f4;
    font-weight: 600;
    text-align: left;
    border-right: 1px solid #c4c7cc;
}

/* ===== تقاطع Header + Index ===== */
.stDataFrame thead th:nth-child(1) {
    z-index: 14;
}

/* ===== تقاطع Header + Name ===== */
.stDataFrame thead th:nth-child(2) {
    z-index: 13;
    background-color: #d2d6db;
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

# تنظيف الصفوف والأعمدة الفارغة
df = df.dropna(how="all", axis=0).dropna(how="all", axis=1)

# ======== هذا مكان السطرين بالضبط ========
num_cols = df.select_dtypes(include="number").columns
df[num_cols] = df[num_cols].fillna(0).astype(int)
# ========================================

# ترتيب حسب النقاط (العمود الثاني)
df = df.dropna(subset=[df.columns[1]])
df = df.sort_values(by=df.columns[1], ascending=False)

# ================== تلوين الخلايا ==================
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

styled_df = (
    df.style
    .format("{:,}", subset=df.select_dtypes(include="number").columns)
    .applymap(highlight_cells, subset=df.columns[2:])  # تلوين الأعمدة الرقمية
    .set_properties(**{
        "border": "1px solid #e0e0e0",
        "font-size": "14px"
    })
)

# ================== عرض الجدول ==================
st.dataframe(
    styled_df,
    use_container_width=True,
    height=700
)






