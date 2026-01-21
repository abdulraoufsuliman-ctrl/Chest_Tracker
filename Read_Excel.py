import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# ================== إعداد الصفحة ==================
st.set_page_config(
    page_title="Player Results",
    layout="wide"
)

# ================== CSS المطور لتحسين المظهر ==================
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

/* تقليل الفراغ العلوي وتوسيط المحتوى */
.block-container {
    padding-top: 1.5rem;
    max-width: 95%;
}

/* Header layout */
.header {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 25px;
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
[data-testid="stTabs"] [data-baseweb="tab-border"] {
    display: none !important;
}

[data-testid="stTabs"] [role="tablist"] {
    gap: 5px; 
}

/* التاب الفردي - اللون الافتراضي */
[data-testid="stTab"] {
    height: 45px;
    background-color: #f0f2f6;
    color: #31333F !important;
    border-radius: 8px 8px 0 0 !important;
    border: 1px solid #ddd !important;
    border-bottom: none !important;
    padding: 0 30px !important;
    font-weight: 600;
    transition: all 0.3s ease;
}

/* التاب النشط - اللون الافتراضي */
[data-testid="stTab"][aria-selected="true"] {
    background: linear-gradient(135deg, #4f8cff, #3b6df2) !important;
    color: white !important;
    border-color: #3b6df2 !important;
}

/* التاب الذي يحتوي على بيانات (أرقام موجبة) */
.tab-with-data {
    background: linear-gradient(135deg, #34a853, #2e7d32) !important;
    color: white !important;
    border-color: #2e7d32 !important;
}

/* التاب الذي يحتوي على أصفار فقط */
.tab-with-zeros {
    background: linear-gradient(135deg, #ea4335, #c5221f) !important;
    color: white !important;
    border-color: #c5221f !important;
}

/* التاب النشط الذي يحتوي على بيانات */
.tab-with-data[aria-selected="true"] {
    background: linear-gradient(135deg, #2e7d32, #1b5e20) !important;
    color: white !important;
    border-color: #1b5e20 !important;
}

/* التاب النشط الذي يحتوي على أصفار فقط */
.tab-with-zeros[aria-selected="true"] {
    background: linear-gradient(135deg, #c5221f, #a50e0e) !important;
    color: white !important;
    border-color: #a50e0e !important;
}

.tabs-date {
    font-size: 12px;
    color: #5f6368;
    white-space: nowrap;
    margin-bottom: 10px;
    text-align: left;
}

.stDataFrame {
    margin-top: -1px !important;
}

[data-testid="stTable"] , [data-testid="stDataFrame"] {
    border: 1px solid #ddd !important;
    border-radius: 0px !important; 
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

# ================== دالة الحصول على وقت تعديل الملف ==================
def get_file_modified_time(file_name):
    try:
        if os.path.exists(file_name):
            ts = os.path.getmtime(file_name)
            dt = datetime.fromtimestamp(ts) + timedelta(hours=2)
            return dt.strftime("%Y-%m-%d %H:%M (UTC+2)")
        else:
            return "File not found"
    except Exception as e:
        return f"Error: {str(e)}"

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

# ================== دالة لفحص إذا كان الجدول يحتوي على أرقام موجبة ==================
def has_positive_data(df):
    """تحقق إذا كان الجدول يحتوي على أرقام موجبة في الأعمدة الرقمية"""
    try:
        # اختيار الأعمدة الرقمية فقط
        num_cols = df.select_dtypes(include="number").columns
        
        if len(num_cols) == 0:
            return False  # لا توجد أعمدة رقمية
            
        # جمع كل القيم في الأعمدة الرقمية
        total_positive = 0
        for col in num_cols:
            total_positive += (df[col] > 0).sum()
            
        return total_positive > 0
    except:
        return False

# ================== دالة تحميل وعرض البيانات ==================
def load_and_display(file_name, is_castle=False):
    has_data = False  # لتحديد لون التاب
    
    try:
        # التحقق من وجود الملف أولاً
        if not os.path.exists(file_name):
            st.error(f"File '{file_name}' not found!")
            return False
            
        # قراءة البيانات
        df = pd.read_excel(file_name, sheet_name="Results")
        
        # تحويل الأعمدة الرقمية وتنسيقها
        num_cols = df.select_dtypes(include="number").columns
        df[num_cols] = df[num_cols].fillna(0)
        
        # التحقق إذا كان الجدول يحتوي على أرقام موجبة
        has_data = has_positive_data(df)

        # اختيار دالة التلوين المناسبة للنقاط
        if is_castle:
            points_highlight_func = highlight_points_castle
        else:
            points_highlight_func = highlight_points_normal

        # تنسيق الستايل
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
        
        return has_data
        
    except Exception as e:
        st.error(f"Error loading {file_name}: {e}")
        return False

# ================== Tabs (الفترات) مع ألوان متغيرة ==================
# قائمة لتخزين معلومات كل تاب
tabs_info = []

# إنشاء التابات
tab1, tab2, tab3, tab4 = st.tabs(["Period 1", "Period 2", "Period 3", "Castle Competition"])

# عرض محتوى كل تاب وتخزين معلوماتها
with tab1:
    st.markdown(
        f"<div class='tabs-date'>Last update: {get_file_modified_time('Results1.xlsx')}</div>",
        unsafe_allow_html=True
    )
    has_data_1 = load_and_display("Results1.xlsx", is_castle=False)
    tabs_info.append(("tab1", has_data_1))

with tab2:
    st.markdown(
        f"<div class='tabs-date'>Last update: {get_file_modified_time('Results2.xlsx')}</div>",
        unsafe_allow_html=True
    )
    has_data_2 = load_and_display("Results2.xlsx", is_castle=False)
    tabs_info.append(("tab2", has_data_2))

with tab3:
    st.markdown(
        f"<div class='tabs-date'>Last update: {get_file_modified_time('Results3.xlsx')}</div>",
        unsafe_allow_html=True
    )
    has_data_3 = load_and_display("Results3.xlsx", is_castle=False)
    tabs_info.append(("tab3", has_data_3))

with tab4:
    st.markdown(
        f"<div class='tabs-date'>Last update: {get_file_modified_time('Results_Castle.xlsx')}</div>",
        unsafe_allow_html=True
    )
    has_data_4 = load_and_display("Results_Castle.xlsx", is_castle=True)
    tabs_info.append(("tab4", has_data_4))

# ================== إضافة JavaScript لتغيير ألوان التابات ==================
js_code = """
<script>
// الانتظار حتى يتم تحميل الصفحة
setTimeout(function() {
    // الحصول على جميع عناصر التاب
    const tabs = document.querySelectorAll('[data-testid="stTab"]');
    
    // تعريف فئات CSS لألوان التابات
    const tabData = %s;
    
    // تطبيق الألوان على كل تاب
    tabs.forEach((tab, index) => {
        if (index < tabData.length) {
            const hasData = tabData[index][1];
            if (hasData === true) {
                // إذا كان هناك بيانات إيجابية
                tab.classList.add('tab-with-data');
            } else if (hasData === false) {
                // إذا كان هناك أصفار فقط
                tab.classList.add('tab-with-zeros');
            }
        }
    });
}, 1000); // تأخير 1 ثانية لضمان تحميل كل شيء
</script>
""" % str(tabs_info)

# إضافة JavaScript لتطبيق الألوان
st.components.v1.html(js_code, height=0)
