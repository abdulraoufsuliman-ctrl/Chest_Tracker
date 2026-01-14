import streamlit as st
import pandas as pd

# إعداد الصفحة بالعرض الكامل
st.set_page_config(page_title="Player Results", layout="wide")

# --- تحسينات التصميم عبر CSS ---
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

/* عنوان الصفحة - أسود */
.main-title {
    font-size: 42px !important;
    font-weight: 800;
    text-align: center;
    letter-spacing: 2px;
    margin-bottom: 12px;
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


# --- إضافة الشعار (Logo) ---
# يمكنك استبدال الرابط أدناه برابط مباشر لصورة شعارك
#logo_url = "https://raw.githubusercontent.com/abdulraoufsuliman-ctrl/Chest_Tracker/main/logo.png"

# عرض الشعار في المنتصف
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    # إذا كان لديك شعار، سيظهر هنا، وإذا لم يوجد سيتجاهله الكود
    try:
        st.image(logo_url, width=200)
    except:
        pass

# --- عنوان الصفحة بحجم مخصص ---
st.markdown('<p class="main-title">[RUM] BOTTLES AND BATTLE</p>', unsafe_allow_html=True)

file_name = 'Results.xlsx'
sheet_target = 'Results' 

try:
    df = pd.read_excel(file_name, sheet_name=sheet_target)
    df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)

    if not df.empty:
        df = df.dropna(subset=[df.columns[0], df.columns[1]])
        df = df.sort_values(by=df.columns[1], ascending=False)

        # إضافة نص "آخر تحديث" ليعرف اللاعبون دقة البيانات
       # st.info("💡 The leaderboard is updated live based on game progress.")
        
        # عرض الجدول بارتفاع كبير وعرض كامل
        st.dataframe(df, use_container_width=True, hide_index=True, height=600) 

except Exception as e:
    st.error(f"Error: {e}")












