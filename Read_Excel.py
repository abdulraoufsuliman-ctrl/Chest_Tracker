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

# ================== معلومات الفترات (إضافة جديدة) ==================
# قاموس لتواريخ جميع الفترات - يمكن تعديله بسهولة
PERIODS_INFO = {
    "Period 1": {
        "start_date": "2024-01-01",
        "end_date": "2024-01-31",
        "status": "ended",  # ended, active, upcoming
        "description": "الفترة الأولى من المنافسة"
    },
    "Period 2": {
        "start_date": "2024-02-01",
        "end_date": "2024-02-29",
        "status": "active",  # ended, active, upcoming
        "description": "الفترة الثانية من المنافسة"
    },
    "Period 3": {
        "start_date": "2024-03-01",
        "end_date": "2024-03-31",
        "status": "upcoming",  # ended, active, upcoming
        "description": "الفترة الثالثة من المنافسة"
    },
    "Castle Competition": {
        "start_date": "2024-02-15",
        "end_date": "2024-02-28",
        "status": "active",  # ended, active, upcoming
        "description": "منافسة القلعة الخاصة"
    }
}

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

/* ================== إضافات جديدة لمعلومات الفترات ================== */

/* تنسيق معلومات الفترة تحت التبويب */
.period-info-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding: 10px 15px;
    background-color: #f8f9fa;
    border-radius: 8px;
    border-left: 4px solid #4f8cff;
}

.period-dates {
    font-size: 14px;
    color: #555;
    display: flex;
    align-items: center;
    gap: 10px;
}

.period-status {
    font-size: 13px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 20px;
}

.status-active {
    background-color: #e6f4ea;
    color: #1e7f43;
    border: 1px solid #a8d5ba;
}

.status-ended {
    background-color: #fce8e6;
    color: #c5221f;
    border: 1px solid #f4c7c3;
}

.status-upcoming {
    background-color: #fef3c7;
    color: #92400e;
    border: 1px solid #fcd34d;
}

/* زر المعلومات */
.info-btn {
    background: none;
    border: none;
    color: #4f8cff;
    cursor: pointer;
    font-size: 16px;
    padding: 5px;
    border-radius: 50%;
    transition: all 0.2s;
}

.info-btn:hover {
    background-color: rgba(79, 140, 255, 0.1);
    transform: scale(1.1);
}

/* نافذة المعلومات المنبثقة */
.info-popup {
    background-color: white;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    margin: 10px 0;
    border: 1px solid #e0e0e0;
}

.info-popup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 2px solid #4f8cff;
}

.info-popup-title {
    font-size: 18px;
    font-weight: bold;
    color: #1e3a8a;
}

.info-popup-close {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    color: #666;
}

.info-popup-close:hover {
    color: #333;
}

.info-popup-content {
    font-size: 14px;
    line-height: 1.6;
    color: #444;
}

.info-detail-row {
    display: flex;
    margin-bottom: 8px;
    padding: 5px 0;
}

.info-detail-label {
    font-weight: 600;
    min-width: 100px;
    color: #555;
}

.info-detail-value {
    flex: 1;
    color: #222;
}

/* أيقونة التقويم */
.calendar-icon {
    font-size: 14px;
    margin-right: 5px;
    color: #4f8cff;
}

/* أيقونة الساعة */
.clock-icon {
    font-size: 14px;
    margin-right: 5px;
    color: #666;
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

# ================== دالة حساب الأيام المتبقية (إضافة جديدة) ==================
def calculate_remaining_days(start_date_str, end_date_str):
    """حساب الأيام المتبقية في الفترة"""
    try:
        today = datetime.now().date()
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        
        if today < start_date:
            return f"تبدأ بعد {(start_date - today).days} يوم"
        elif today > end_date:
            return "انتهت"
        else:
            remaining = (end_date - today).days + 1
            return f"متبقي {remaining} يوم"
    except:
        return "غير محسوب"

# ================== دالة لعرض معلومات الفترة (إضافة جديدة) ==================
def display_period_info(period_name):
    """عرض معلومات الفترة تحت كل تبويب"""
    if period_name in PERIODS_INFO:
        info = PERIODS_INFO[period_name]
        
        # تنسيق التواريخ
        start_date = datetime.strptime(info["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(info["end_date"], "%Y-%m-%d")
        start_formatted = start_date.strftime("%d/%m/%Y")
        end_formatted = end_date.strftime("%d/%m/%Y")
        
        # حساب الأيام المتبقية
        remaining_days = calculate_remaining_days(info["start_date"], info["end_date"])
        
        # تحديد لون الحالة
        status_class = ""
        status_icon = ""
        if info["status"] == "active":
            status_class = "status-active"
            status_icon = "🟢"
        elif info["status"] == "ended":
            status_class = "status-ended"
            status_icon = "🔴"
        elif info["status"] == "upcoming":
            status_class = "status-upcoming"
            status_icon = "🟡"
        
        # إنشاء HTML لعرض المعلومات
        st.markdown(f"""
        <div class="period-info-container">
            <div class="period-dates">
                <span class="calendar-icon">📅</span>
                <span>{start_formatted} - {end_formatted}</span>
                <span class="clock-icon">⏳</span>
                <span>{remaining_days}</span>
            </div>
            <div class="period-status {status_class}">
                {status_icon} {info["status"].upper()}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # زر المعلومات (سيتم التعامل معه لاحقاً)
        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button("ⓘ", key=f"info_{period_name}"):
                st.session_state[f"show_info_{period_name}"] = True
        
        # عرض نافذة المعلومات إذا طلبها المستخدم
        if f"show_info_{period_name}" in st.session_state and st.session_state[f"show_info_{period_name}"]:
            with st.container():
                st.markdown(f"""
                <div class="info-popup">
                    <div class="info-popup-header">
                        <div class="info-popup-title">معلومات الفترة</div>
                        <button class="info-popup-close" onclick="document.getElementById('close_{period_name}').click()">×</button>
                    </div>
                    <div class="info-popup-content">
                        <div class="info-detail-row">
                            <span class="info-detail-label">اسم الفترة:</span>
                            <span class="info-detail-value">{period_name}</span>
                        </div>
                        <div class="info-detail-row">
                            <span class="info-detail-label">تاريخ البدء:</span>
                            <span class="info-detail-value">{start_formatted}</span>
                        </div>
                        <div class="info-detail-row">
                            <span class="info-detail-label">تاريخ الانتهاء:</span>
                            <span class="info-detail-value">{end_formatted}</span>
                        </div>
                        <div class="info-detail-row">
                            <span class="info-detail-label">المدة:</span>
                            <span class="info-detail-value">{(end_date - start_date).days + 1} يوم</span>
                        </div>
                        <div class="info-detail-row">
                            <span class="info-detail-label">الحالة:</span>
                            <span class="info-detail-value">{remaining_days}</span>
                        </div>
                        <div class="info-detail-row">
                            <span class="info-detail-label">الوصف:</span>
                            <span class="info-detail-value">{info["description"]}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # زر إغلاق خفي
                if st.button("إغلاق", key=f"close_{period_name}"):
                    st.session_state[f"show_info_{period_name}"] = False
                    st.rerun()

# ================== تهيئة حالة الجلسة للأزرار (إضافة جديدة) ==================
for period in PERIODS_INFO.keys():
    if f"show_info_{period}" not in st.session_state:
        st.session_state[f"show_info_{period}"] = False

# =============================================
def get_file_modified_time(file_name):
    ts = os.path.getmtime(file_name)
    dt = datetime.fromtimestamp(ts) + timedelta(hours=2)
    return dt.strftime("%Y-%m-%d %H:%M (UTC+2)")

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

# ================== دالة تحميل وعرض البيانات ==================
def load_and_display(file_name, is_castle=False):
    try:
        # قراءة البيانات
        df = pd.read_excel(file_name, sheet_name="Results")
        
        # تحويل الأعمدة الرقمية وتنسيقها
        num_cols = df.select_dtypes(include="number").columns
        for col in num_cols:
            # تحويل القيم إلى أعداد صحيحة (بدون فاصلة عشرية)
            df[col] = df[col].fillna(0).astype(int)

        # اختيار دالة التلوين المناسبة للنقاط
        if is_castle:
            points_highlight_func = highlight_points_castle
        else:
            points_highlight_func = highlight_points_normal

        # تنسيق الستايل
        styled_df = (
            df.style
            .format("{:,}", subset=num_cols)
        
            # تلوين عمود Points بشروط خاصة
            .applymap(points_highlight_func, subset=["Points"])
        
            # تلوين بقية الأعمدة الرقمية
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
        st.error(f"Error loading {file_name}: {e}")

# ================== Tabs (الفترات) ==================
# تأكدنا هنا أن أسماء الفترات مكتوبة بوضوح
tab1, tab2, tab3, tab4 = st.tabs(["Period 1", "Period 2",  "Period 3", "Castle Competition"])

with tab1:
    # عرض معلومات الفترة (إضافة جديدة)
    display_period_info("Period 1")
    
    st.markdown(
        f"<div class='tabs-date'>Last update: {get_file_modified_time('Results1.xlsx')}</div>",
        unsafe_allow_html=True
    )
    load_and_display("Results1.xlsx", is_castle=False)

with tab2:
    # عرض معلومات الفترة (إضافة جديدة)
    display_period_info("Period 2")
    
    st.markdown(
        f"<div class='tabs-date'>Last update: {get_file_modified_time('Results2.xlsx')}</div>",
        unsafe_allow_html=True
    )
    load_and_display("Results2.xlsx", is_castle=False)

with tab3:
    # عرض معلومات الفترة (إضافة جديدة)
    display_period_info("Period 3")
    
    st.markdown(
        f"<div class='tabs-date'>Last update: {get_file_modified_time('Results3.xlsx')}</div>",
        unsafe_allow_html=True
    )
    load_and_display("Results3.xlsx", is_castle=False)

with tab4:
    # عرض معلومات الفترة (إضافة جديدة)
    display_period_info("Castle Competition")
    
    st.markdown(
        f"<div class='tabs-date'>Last update: {get_file_modified_time('Results_Castle.xlsx')}</div>",
        unsafe_allow_html=True
    )
    load_and_display("Results_Castle.xlsx", is_castle=True)

# ================== كيفية التعديل على تواريخ الفترات (إضافة جديدة) ==================
with st.expander("⚙️ كيفية تعديل تواريخ الفترات"):
    st.markdown("""
    ### لتعديل تواريخ الفترات:
    
    1. ابحث عن قسم **معلومات الفترات** في بداية الكود
    2. ستجد قاموس باسم `PERIODS_INFO`
    3. قم بتعديل القيم كما يلي:
    
    ```python
    PERIODS_INFO = {
        "Period 1": {
            "start_date": "2024-01-01",  # تاريخ البدء (سنة-شهر-يوم)
            "end_date": "2024-01-31",    # تاريخ الانتهاء
            "status": "ended",           # الحالة: ended, active, upcoming
            "description": "وصف الفترة"   # وصف الفترة
        },
        # ... باقي الفترات
    }
    ```
    
    4. احفظ التغييرات وأعد تشغيل التطبيق
    
    ### ملاحظات:
    - استخدم التنسيق: `YYYY-MM-DD` (سنة-شهر-يوم)
    - الحالات المتاحة:
      - `"active"`: الفترة نشطة حالياً
      - `"ended"`: الفترة انتهت
      - `"upcoming"`: الفترة لم تبدأ بعد
    """)
