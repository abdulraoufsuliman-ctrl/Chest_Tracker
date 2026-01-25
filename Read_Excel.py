import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# ================== إعداد الصفحة ==================
st.set_page_config(
    page_title="Player Results",
    layout="wide"
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ================== CSS المطور لتحسين المظهر ==================
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

/* تقليل الفراغ العلوي وتوسيط المحتوى */
.block-container {
    padding-top: 0.1rem;
    max-width: 95%;
}

/* Header layout */
.header {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 25px;
    position: relative;
}

.logo {
    width: 70px;
    height: auto;
}

.title {
    font-size: 35px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #000000;
    line-height: 2.9;
    padding-top: 4px;
}

/* ================== إزالة الخط السفلي للتابات وجعلها ملتصقة ================== */

/* إزالة الخط السفلي الافتراضي من Streamlit */
[data-testid="stTabs"] [data-baseweb="tab-border"] {
    display: none !important;
}

/* تنسيق حاوية التابات */
[data-testid="stTabs"] [role="tablist"] {
    gap: 5px; 
}

/* تصميم التاب الفردي */
[data-testid="stTab"] {
    height: 45px;
    background-color: #f0f2f6;
    color: #31333F !important;
    border-radius: 8px 8px 0 0 !important;
    border: 1px solid #ddd !important;
    border-bottom: none !important;
    padding: 0 30px !important;
    font-weight: 600;
}

/* التاب النشط */
[data-testid="stTab"][aria-selected="true"] {
    background: linear-gradient(135deg, #4f8cff, #3b6df2) !important;
    color: white !important;
    border-color: #3b6df2 !important;
}

/* التاريخ */
.tabs-date {
    font-size: 12px;
    color: #5f6368;
    white-space: nowrap;
    margin-bottom: 10px;
    text-align: Left;
}

/* ================== تنسيق الجدول (حواف حادة) ================== */
.stDataFrame {
    margin-top: -1px !important;
}

/* حواف حادة للجدول */
[data-testid="stTable"] , [data-testid="stDataFrame"] {
    border: 1px solid #ddd !important;
    border-radius: 0px !important; 
}

/* زر النقاط المستخدمة */
.used-points-btn {
    position: absolute;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
    font-size: 14px;
}

.used-points-btn:hover {
    background: linear-gradient(135deg, #2563eb, #1e40af);
}

/* تنسيق للنافذة المنبثقة */
.popup-container {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #ddd;
    margin: 10px 0;
}

.popup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid #3b82f6;
}

.popup-title {
    font-size: 24px;
    font-weight: bold;
    color: #1e3a8a;
}

.close-btn {
    background-color: #ef4444;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
}

.close-btn:hover {
    background-color: #dc2626;
}

/* تظليل الخلفية عند فتح النافذة المنبثقة */
.popup-background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 999;
    display: flex;
    justify-content: center;
    align-items: center;
}

.popup-content {
    background-color: white;
    border-radius: 10px;
    padding: 20px;
    max-width: 90%;
    max-height: 90%;
    overflow: auto;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}

</style>
""", unsafe_allow_html=True)

# ================== تهيئة حالة الجلسة ==================
if 'show_used_points' not in st.session_state:
    st.session_state.show_used_points = False

# ================== HEADER مع زر النقاط المستخدمة ==================
logo_url = "https://raw.githubusercontent.com/abdulraoufsuliman-ctrl/Chest_Tracker/main/logo.png"

st.markdown(f"""
<div class="header">
    <img src="{logo_url}" class="logo">
    <div class="title">[RUM] BOTTLES AND BATTLE</div>
    <button class="used-points-btn" onclick="document.getElementById('openPopup').click()">
        📊 النقاط المستخدمة
    </button>
</div>
""", unsafe_allow_html=True)

# زر خفي لفتح النافذة المنبثقة
if st.button("Open Popup", key="openPopup", type="secondary", help="hidden"):
    st.session_state.show_used_points = True

# ================== دالة لتحميل بيانات النقاط المستخدمة ==================
def load_used_points():
    try:
        # التحقق من وجود الملف
        if not os.path.exists("Used_Points.xlsx"):
            st.error("❌ ملف Used_Points.xlsx غير موجود في المجلد الحالي")
            return None
        
        # تحميل البيانات
        df = pd.read_excel("Used_Points.xlsx", sheet_name="Points")
        
        # التحقق من أن البيانات غير فارغة
        if df.empty:
            st.warning("⚠️ ورقة Points في الملف فارغة")
            return None
            
        return df
        
    except FileNotFoundError:
        st.error("❌ لم يتم العثور على الملف: Used_Points.xlsx")
        return None
    except ValueError as e:
        if "Worksheet" in str(e) and "not found" in str(e):
            st.error("❌ لم يتم العثور على الورقة 'Points' في الملف")
        else:
            st.error(f"❌ خطأ في قراءة الملف: {str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ خطأ غير متوقع: {str(e)}")
        return None

# ================== النافذة المنبثقة للنقاط المستخدمة ==================
if st.session_state.show_used_points:
    # استخدام HTML/CSS/JavaScript لعمل نافذة منبثقة
    st.markdown("""
    <div class="popup-background" id="usedPointsPopup">
        <div class="popup-content">
            <div class="popup-header">
                <div class="popup-title">📊 النقاط المستخدمة</div>
                <button class="close-btn" onclick="document.getElementById('closePopup').click()">✕ إغلاق</button>
            </div>
    """, unsafe_allow_html=True)
    
    # تحميل وعرض البيانات
    used_points_df = load_used_points()
    
    if used_points_df is not None:
        if not used_points_df.empty:
            # تنسيق الأعمدة الرقمية
            num_cols = used_points_df.select_dtypes(include="number").columns
            for col in num_cols:
                used_points_df[col] = used_points_df[col].fillna(0)
            
            # عرض الجدول
            st.dataframe(
                used_points_df,
                use_container_width=True,
                height=400,
                hide_index=True
            )
            
            # معلومات عن عدد الصفوف والأعمدة
            st.caption(f"عدد السجلات: {len(used_points_df)} | عدد الأعمدة: {len(used_points_df.columns)}")
        else:
            st.warning("⚠️ لا توجد بيانات في جدول النقاط المستخدمة")
    else:
        st.error("❌ تعذر تحميل بيانات النقاط المستخدمة")
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # زر خفي للإغلاق
    if st.button("Close Popup", key="closePopup", type="secondary", help="hidden"):
        st.session_state.show_used_points = False
        st.rerun()

# ================== الدوال المساعدة ==================
def get_file_modified_time(file_name):
    try:
        ts = os.path.getmtime(file_name)
        dt = datetime.fromtimestamp(ts) + timedelta(hours=2)
        return dt.strftime("%Y-%m-%d %H:%M (UTC+2)")
    except:
        return "غير متوفر"

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

def highlight_points_normal(val):
    if not isinstance(val, (int, float)):
        return "text-align: center;"

    if val == 0:
        return (
            "background-color: #fce8e6;"
            "color: #c5221f;"
            "font-weight: 700;"
            "text-align: center;"
        )
    elif 0 < val < 2500:
        return (
            "background-color: #fff4ce;"
            "color: #7a5c00;"
            "font-weight: 700;"
            "text-align: center;"
        )
    else:  # >= 2500
        return (
            "background-color: #e6f4ea;"
            "color: #1e7f43;"
            "font-weight: 700;"
            "text-align: center;"
        )
        
def highlight_points_castle(val):
    if not isinstance(val, (int, float)):
        return "text-align: center;"

    if val > 0:
        return (
            "background-color: #e6f4ea;"
            "color: #1e7f43;"
            "font-weight: 700;"
            "text-align: center;"
        )
    elif val == 0:
        return (
            "background-color: #fce8e6;"
            "color: #c5221f;"
            "font-weight: 700;"
            "text-align: center;"
        )
    else:  # val < 0
        return (
            "background-color: #fce8e6;"
            "color: #c5221f;"
            "font-weight: 700;"
            "text-align: center;"
        )

# ================== دالة تحميل وعرض البيانات الرئيسية ==================
def load_and_display(file_name, is_castle=False):
    try:
        # التحقق من وجود الملف
        if not os.path.exists(file_name):
            st.error(f"❌ الملف {file_name} غير موجود")
            return
        
        df = pd.read_excel(file_name, sheet_name="Results")
        
        num_cols = df.select_dtypes(include="number").columns
        for col in num_cols:
            df[col] = df[col].fillna(0).astype(int)

        if is_castle:
            points_highlight_func = highlight_points_castle
        else:
            points_highlight_func = highlight_points_normal

        styled_df = (
            df.style
            .format("{:,}", subset=num_cols)
            .applymap(points_highlight_func, subset=["Points"])
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
    except Exception as e:
        st.error(f"❌ خطأ في تحميل {file_name}: {str(e)}")

# ================== Tabs (الفترات) ==================
tab1, tab2, tab3, tab4 = st.tabs(["Period 1", "Period 2", "Period 3", "Castle Competition"])

with tab1:
    st.markdown(
        f"<div class='tabs-date'>Last update: {get_file_modified_time('Results1.xlsx')}</div>",
        unsafe_allow_html=True
    )
    load_and_display("Results1.xlsx", is_castle=False)

with tab2:
    st.markdown(
        f"<div class='tabs-date'>Last update: {get_file_modified_time('Results2.xlsx')}</div>",
        unsafe_allow_html=True
    )
    load_and_display("Results2.xlsx", is_castle=False)

with tab3:
    st.markdown(
        f"<div class='tabs-date'>Last update: {get_file_modified_time('Results3.xlsx')}</div>",
        unsafe_allow_html=True
    )
    load_and_display("Results3.xlsx", is_castle=False)

with tab4:
    st.markdown(
        f"<div class='tabs-date'>Last update: {get_file_modified_time('Results_Castle.xlsx')}</div>",
        unsafe_allow_html=True
    )
    load_and_display("Results_Castle.xlsx", is_castle=True)

# إضافة JavaScript لإغلاق النافذة عند الضغط على ESC
st.markdown("""
<script>
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape' && document.getElementById('usedPointsPopup')) {
        document.getElementById('closePopup').click();
    }
});
</script>
""", unsafe_allow_html=True)
