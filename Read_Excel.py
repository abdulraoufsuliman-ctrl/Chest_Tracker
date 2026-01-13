import streamlit as st
import pandas as pd

# إعداد الصفحة بالعرض الكامل
st.set_page_config(page_title="Player Results", layout="wide")

# تصميم الواجهة
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    h1 { color: #00e5ff; text-align: center; font-family: 'Arial'; margin-bottom: 0px;}
    .stDataFrame { border: 1px solid #4B0082; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 [RUM] BOTTLES AND BATTLES")

file_name = 'Results.xlsx'
sheet_target = 'Results' 

try:
    df = pd.read_excel(file_name, sheet_name=sheet_target)

    # تنظيف البيانات
    df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)

    if not df.empty:
        # حذف الصفوف الفارغة في أول عمودين (الاسم والنقاط)
        df = df.dropna(subset=[df.columns[0], df.columns[1]])
        
        # ترتيب البيانات حسب النقاط
        df = df.sort_values(by=df.columns[1], ascending=False)

        st.write(f"### Leaders list (live update)")
        
        # التعديل هنا: أضفنا height=1000 لزيادة الارتفاع بشكل كبير
        # يمكنك تغيير الرقم 1000 إلى 1500 أو أكثر حسب رغبتك
        st.dataframe(df, use_container_width=True, hide_index=True, height=500) 

except Exception as e:
    st.error(f"Error: {e}")






