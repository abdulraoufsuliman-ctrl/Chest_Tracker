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

/* جدول */
.stDataFrame {
    background-color: #ffffff;
    border: 1px solid #dadce0;
    border-radius: 0;
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

# ================== دالة تحميل وعرض البيانات ==================
def load_and_display(file_name):
    df = pd.read_excel(file_name, sheet_name="Results")

    df = df.dropna(how="all", axis=0).dropna(how="all", axis=1)

    num_cols = df.select_dtypes(include="number").columns
    df[num_cols] = df[num_cols].fillna(0).astype(int)

    df = df.dropna(subset=[df.columns[1]])
    df = df.sort_values(by=df.columns[1], ascending=False)
    df = df.reset_index(drop=True)

    styled_df = (
        df.style
        .format("{:,}", subset=num_cols)
        .applymap(highlight_cells, subset=df.columns[2:])
        .set_properties(**{
            "border": "1px solid #e0e0e0",
            "font-size": "14px"
        })
    )

    st.dataframe(
        styled_df,
        use_container_width=True,
        height=600
        hide_index=True
    )

# ================== Tabs (الفترات) ==================
tab1, tab2 = st.tabs(["Period 1", "Period 2"])

with tab1:
    load_and_display("Results1.xlsx")

with tab2:
    load_and_display("Results2.xlsx")

