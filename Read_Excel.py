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

/* جدول HTML مخصص مع تثبيت العمود الأول */
.fixed-column-table {
    width: 100%;
    overflow-x: auto;
    border: 1px solid #dadce0;
    background-color: white;
    margin-bottom: 20px;
}

.fixed-column-table table {
    width: 100%;
    border-collapse: collapse;
    min-width: 1000px;
}

.fixed-column-table th,
.fixed-column-table td {
    padding: 10px 12px;
    border: 1px solid #e0e0e0;
    text-align: center;
    font-size: 14px;
}

.fixed-column-table th {
    background-color: #f8f9fa;
    font-weight: bold;
    position: sticky;
    top: 0;
    z-index: 10;
}

/* تثبيت العمود الأول */
.fixed-column-table th:first-child,
.fixed-column-table td:first-child {
    position: sticky;
    left: 0;
    background-color: white;
    z-index: 5;
    border-right: 2px solid #e0e0e0;
    min-width: 120px;
    text-align: left;
}

.fixed-column-table th:first-child {
    z-index: 15;
    background-color: #f8f9fa;
}

/* تلوين الخلايا */
.positive-cell {
    background-color: #e6f4ea !important;
    color: #1e7f43 !important;
    font-weight: 600 !important;
}

.negative-cell {
    background-color: #fce8e6 !important;
    color: #c5221f !important;
    font-weight: 600 !important;
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

# ================== إنشاء جدول HTML يدويًا ==================

# وظيفة لتحديد لون الخلية
def get_cell_class(val):
    if isinstance(val, (int, float)):
        if val > 0:
            return "positive-cell"
        elif val == 0:
            return "negative-cell"
    return ""

# بداية الجدول
html_table = '<div class="fixed-column-table"><table>'

# رأس الجدول
html_table += '<thead><tr>'
for col in df.columns:
    html_table += f'<th>{col}</th>'
html_table += '</tr></thead>'

# جسم الجدول
html_table += '<tbody>'
for _, row in df.iterrows():
    html_table += '<tr>'
    for idx, (col_name, value) in enumerate(row.items()):
        cell_class = get_cell_class(value) if idx > 0 else ""
        # تنسيق الأرقام بفواصل الآلاف
        if isinstance(value, (int, float)) and idx > 0:
            display_value = f"{value:,}"
        else:
            display_value = str(value)
        
        html_table += f'<td class="{cell_class}">{display_value}</td>'
    html_table += '</tr>'
html_table += '</tbody></table></div>'

# ================== عرض الجدول ==================
st.markdown(html_table, unsafe_allow_html=True)
