import streamlit as st
import pandas as pd

# 1. إعداد الصفحة بالوضع العريض (Wide) لاستغلال كامل مساحة الشاشة
st.set_page_config(page_title="Player results", layout="wide")

# تصميم الثيم
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    h1 { color: #00e5ff; text-align: center; font-family: 'Arial'; }
    /* إضافة إطار بسيط للجدول */
    .stDataFrame { border: 1px solid #4B0082; }
    </style>
    """, unsafe_allow_html=True)

#st.title("🏆 Leaderboard")

file_name = 'Results.xlsx'
sheet_target = 'Results' 

try:
    df = pd.read_excel(file_name, sheet_name=sheet_target)

    # تنظيف البيانات
    df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)

    if not df.empty:
        # حذف الصفوف الفارغة في الأعمدة الأساسية
        df = df.dropna(subset=[df.columns[0], df.columns[1]])
        
        # ترتيب البيانات
        df = df.sort_values(by=df.columns[1], ascending=False)

        st.write(f"### Leaders list (live update)")
        
        # 2. عرض الجدول مع خاصية التمدد العريض
        st.dataframe(df, use_container_width=True, hide_index=True) 

except Exception as e:
    st.error(f"Error: {e}")




