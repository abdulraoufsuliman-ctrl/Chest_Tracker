import streamlit as st
import pandas as pd

# إعداد الصفحة بالعرض الكامل
st.set_page_config(page_title="Player Results", layout="wide")

# ================== CSS ==================
st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: white;
}

/* تقليل الفراغ العلوي */
.block-container {
    padding-top: 1.5rem;
}

/* عنوان الصفحة */
.main-title {
    font-size: 42px !important;
    font-weight: 800;
    letter-spacing: 2px;
    margin: 0;
    color: #000000;
}

/* جدول بحواف حادة */
.stDataFrame {
    border: 1px solid #000000;
    border-radius: 0px;
    overflow: hidden;
    box-shadow: none;
}
</style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
logo_url = "https://raw.githubusercontent.com/abdulraoufsuliman-ctrl/Chest_Tracker/main/logo.png"

col1, col2 = st.columns([1, 6], vertical_alignment="center")

with col1:
    st.image(logo_url, width=90)

with col2:
    st.markdown(
        '<p class="main-title">[RUM] BOTTLES AND BATTLE</p>',
        unsafe_allow_html=True
    )

# ================== DATA ==================
file_name = 'Results.xlsx'
sheet_target = 'Results'

try:
    df = pd.read_excel(file_name, sheet_name=sheet_target)
    df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)

    if not df.empty:
        df = df.dropna(subset=[df.columns[0], df.columns[1]])
        df = df.sort_values(by=df.columns[1], ascending=False)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=700
        )

except Exception as e:
    st.error(f"Error: {e}")
















