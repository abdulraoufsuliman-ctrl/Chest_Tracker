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

/* Header layout */
.header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 10px;
}

/* Logo */
.logo {
    width: 80px;
    height: auto;
    display: block;
}

/* Title */
.title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #000000;
    line-height: 1;
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

st.markdown(f"""
<div class="header">
    <img src="{logo_url}" class="logo">
    <div class="title">[RUM] BOTTLES AND BATTLE</div>
</div>
""", unsafe_allow_html=True)

# ================== DATA ==================
file_name = "Results.xlsx"
sheet_target = "Results"

try:
    df = pd.read_excel(file_name, sheet_name=sheet_target)
    df = df.dropna(how="all", axis=0).dropna(how="all", axis=1)

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
