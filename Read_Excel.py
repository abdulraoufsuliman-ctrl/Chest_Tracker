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
    padding-top: 10px;   /* ✅ هذا هو المفتاح */
}

.logo {
    width: 80px;
    height: auto;
    display: block;
}

.title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #000000;
    line-height: 2.9;    /* ✅ لا تجعلها 1 */
    padding-top: 4px;   /* ✅ أمان إضافي */
}


/* جدول */
.stDataFrame {
    background-color: #ffffff;
    border: 1px solid #dadce0;
    border-radius: 0;
}

.stDataFrame thead th {
    background-color: #e0e3e7;
    color: #1f1f1f;
    font-weight: 600;
    text-align: center;
    border-bottom: 1px solid #c4c7cc;
}
</style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
logo_url = "https://raw.githubusercontent.com/abdulraoufsuliman-ctrl/Chest_Tracker/main/logo.png"

st.markdown(f"""
<div style="display:flex; align-items:center; gap:16px; padding-top:10px; margin-bottom:16px;">
    <img src="{logo_url}" style="width:70px;">
    <div style="font-size:40px; font-weight:700; letter-spacing:1.5px; color:#000;">
        [RUM] BOTTLES AND BATTLE
    </div>
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
    # فصل الآلاف
    .format("{:,}", subset=num_cols)

    # تلوين الأعمدة الرقمية (تجاوز عمود الاسم)
    .applymap(highlight_cells, subset=df.columns[2:])

    # خصائص عامة
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



