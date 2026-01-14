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

    /* رفع الجدول ليغطي خط التابات */
.stDataFrame {
    margin-top: -14px;      /* عدّل القيمة إذا لزم */
    position: relative;
    z-index: 2;
}

}
/* ================== تحسين Tabs ================== */

/* ================== Elegant Tabs (Segmented Style) ================== */

/* ================== إزالة الخط الممتد تحت Tabs نهائيًا ================== */

/* جعل التابات ملتصقة بالجدول */
[data-testid="stTabs"] {
    margin-bottom: -10px;   /* يلغي الفراغ والخط */
    position: relative;
    z-index: 1;
}

/* حافة علوية للجدول لتغطي أي خط */
.stDataFrame {
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}


/* إزالة أي حدود أساسية */
[data-testid="stTabs"] * {
    border-bottom: none !important;
    box-shadow: none !important;
}

/* إزالة العنصر الوهمي الذي يرسم الخط */
[data-testid="stTabs"] div::before,
[data-testid="stTabs"] div::after {
    content: none !important;
    display: none !important;
}

/* إزالة الفاصل الذي يضيفه Streamlit بعد Tabs */
[data-testid="stTabs"] + div {
    border-top: none !important;
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* احتياطي أخير */
[data-testid="stTabs"] hr {
    display: none !important;
}



/* حاوية التابات */
[data-testid="stTabs"] {
    background: rgba(255,255,255,0.55);
    padding: 6px;
    border-radius: 12px;
    display: inline-block;
}

/* التاب */
[data-testid="stTab"] {
    padding: 10px 26px;
    border-radius: 10px;
    margin-right: 6px;
    font-weight: 600;
    font-size: 16px;
    color: #3c4043;
    background: transparent;
    border: none;
    transition: all 0.25s ease;
}

/* Hover */
[data-testid="stTab"]:hover {
    background-color: rgba(66,133,244,0.08);
}

/* التاب النشط */
[data-testid="stTab"][aria-selected="true"] {
    background: linear-gradient(
        135deg,
        #4f8cff,
        #3b6df2
    );
    color: #ffffff;
    box-shadow: 0 6px 18px rgba(59,109,242,0.35);
}

/* إزالة أي underline */
[data-testid="stTab"]::after {
    display: none !important;
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
        height=600,
        hide_index=True
    )

# ================== Tabs (الفترات) ==================
tab1, tab2 = st.tabs(["Period 1", "Period 2"])

with tab1:
    load_and_display("Results1.xlsx")

with tab2:
    load_and_display("Results2.xlsx")









