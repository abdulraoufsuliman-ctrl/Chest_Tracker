import streamlit as st
import pandas as pd

# إعدادات الصفحة - جعلناها Wide لإعطاء مساحة أكبر للجدول
st.set_page_config(page_title="Player Results", layout="wide")

# تصميم الثيم
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    h1 { color: #00e5ff; text-align: center; font-family: 'Arial'; }
    /* تحسين شكل الجداول */
    .stDataFrame { border: 1px solid #4B0082; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 Leaderboard")

file_name = 'Results.xlsx'
# تأكد من مطابقة هذا الاسم لاسم الورقة في إكسل تماماً (بدون مسافات زائدة)
sheet_target = 'Results' 

try:
    # 1. قراءة البيانات
    df = pd.read_excel(file_name, sheet_name=sheet_target)

    # 2. تنظيف البيانات من الصفوف والأعمدة الفارغة تماماً
    df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)

    # 3. حذف الصفوف التي تفتقد لبيانات أساسية (الاسم أو النقاط)
    if not df.empty:
        df = df.dropna(subset=[df.columns[0], df.columns[1]])

        # 4. ترتيب البيانات حسب النقاط
        df = df.sort_values(by=df.columns[1], ascending=False)

        st.write(f"### Leaders list (live update)")
        
        # التعديل الجوهري هنا: استخدام dataframe بدلاً من table
        # هذا يسمح للجدول بالتمدد بشكل مريح ويمنع النصوص من الظهور بشكل رأسي
        st.dataframe(df, use_container_width=True, hide_index=True) 
    else:
        st.warning("الورقة المختارة فارغة، تأكد من وجود بيانات في ملف Results.xlsx")

except Exception as e:
    st.error(f"Error: Make sure the file and sheet name are correct. Details: {e}")


