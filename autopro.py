import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- إعدادات النظام العيا ---
st.set_page_config(page_title="AutoPro ERP v1.0", layout="wide", initial_sidebar_state="expanded")

# --- محاكاة قاعدة البيانات (8000 صنف) ---
if 'db_products' not in st.session_state:
    st.session_state.db_products = pd.DataFrame([
        {"ID": 1, "الصنف": "تيل فرامل تويوتا كوري", "SKU": "BK-2024", "الرف": "A1-01", "التكلفة": 450, "البيع": 650, "المخزن": 45},
        {"ID": 2, "الصنف": "فلتر زيت هيونداي أصلي", "SKU": "OF-992", "الرف": "B2-10", "التكلفة": 120, "البيع": 180, "المخزن": 120},
        {"ID": 3, "الصنف": "طقم بوجيهات ليزر NGK", "SKU": "SP-771", "الرف": "C1-05", "التكلفة": 850, "البيع": 1200, "المخزن": 12},
        {"ID": 4, "الصنف": "مساعد خلفي تويوتا", "SKU": "SH-550", "الرف": "D4-02", "التكلفة": 1100, "البيع": 1600, "المخزن": 8},
    ])

if 'sales_history' not in st.session_state:
    st.session_state.sales_history = []

# --- التصميم الخارجي (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .css-1r6slb0 { background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_value=True)

# --- القائمة الجانبية ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3003/3003184.png", width=100)
    st.title("AutoPro ERP")
    st.info("فرع: القاهرة الرئيسي")
    menu = st.radio("القائمة الرئيسية", ["📊 لوحة التحكم", "🛒 نقطة البيع (POS)", "📦 المخازن والأصناف", "👥 الموظفين والرواتب", "💰 التقارير المالية"])
    st.divider()
    if st.button("تسجيل الخروج"):
        st.stop()

# --- 1. لوحة التحكم ---
if menu == "📊 لوحة التحكم":
    st.title("التقرير اللحظي للأداء")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("مبيعات اليوم", "12,850 ج.م", "+15%")
    c2.metric("أرباح اليوم", "3,200 ج.م", "+8%")
    c3.metric("عدد الفواتير", "24", "4+")
    c4.metric("نقدية الخزينة", "8,400 ج.م")

    st.divider()
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("تحليل المبيعات الأسبوعي")
        df_chart = pd.DataFrame({'يوم': ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء'], 'مبيعات': [5000, 8000, 6500, 12000, 9500]})
        fig = px.bar(df_chart, x='يوم', y='مبيعات', color='مبيعات', color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("الأصناف الأكثر طلباً")
        st.table(st.session_state.db_products[['الصنف', 'المخزن']].sort_values(by='المخزن').head(4))

# --- 2. نقطة البيع (POS) ---
elif menu == "🛒 نقطة البيع (POS)":
    st.title("نقطة بيع سريعة")
    
    col_pos_left, col_pos_right = st.columns([2, 1])
    
    with col_pos_left:
        search_q = st.text_input("🔍 ابحث عن صنف بالاسم أو الكود أو الرف...", placeholder="مثال: تيل فرامل")
        filtered_products = st.session_state.db_products[st.session_state.db_products['الصنف'].str.contains(search_q) | st.session_state.db_products['SKU'].str.contains(search_q)]
        
        st.write("### النتائج")
        for i, row in filtered_products.iterrows():
            c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
            c1.write(f"**{row['الصنف']}**")
            c2.write(f"{row['البيع']} ج.م")
            c3.write(f"📦 {row['المخزن']}")
            if c4.button("إضافة", key=f"add_{row['ID']}"):
                st.toast(f"تم إضافة {row['الصنف']}")

    with col_pos_right:
        st.markdown("### الفاتورة الحالية")
        st.info("العميل: عميل نقدي")
        st.write("---")
        st.write("1x تيل فرامل تويوتا = 650 ج.م")
        st.write("2x فلتر زيت هيونداي = 360 ج.م")
        st.divider()
        total = 1010
        st.subheader(f"الإجمالي: {total} ج.م")
        tax = total * 0.14
        st.write(f"ضريبة (14%): {tax:.2f} ج.م")
        st.markdown(f"## الصافي: {total + tax:.2f} ج.م")
        
        pay_method = st.selectbox("طريقة الدفع", ["كاش", "فيزا"])
        if st.button("حفظ وطباعة الفاتورة (F10)"):
            st.success("تم الحفظ بنجاح وجاري إرسالها للضرائب...")

# --- 3. المخازن ---
elif menu == "📦 المخازن والأصناف":
    st.title("إدارة المخازن (8000 صنف)")
    
    tab1, tab2 = st.tabs(["قائمة الأصناف", "إدخال مشتريات جديدة"])
    
    with tab1:
        st.dataframe(st.session_state.db_products, use_container_width=True)
        st.download_button("تصدير المخزن لملف Excel", data="data", file_name="inventory.csv")
        
    with tab2:
        st.subheader("رفع أصناف من ملف Excel")
        st.file_uploader("اختر الملف لرفعه فوراً للمخزن")
        st.button("بدء المعالجة")

# --- 4. الموظفين ---
elif menu == "👥 الموظفين والرواتب":
    st.title("الموارد البشرية")
    st.table(pd.DataFrame([
        {"الموظف": "أحمد محمد", "الوظيفة": "كاشير", "المبيعات": "120,000 ج.م", "العمولة": "1,200 ج.م", "صافي الراتب": "6,200 ج.م"},
        {"الموظف": "محمود علي", "الوظيفة": "مسؤول مخزن", "المبيعات": "0", "العمولة": "0", "صافي الراتب": "5,500 ج.م"},
    ]))

# --- 5. التقارير ---
elif menu == "💰 التقارير المالية":
    st.title("التقارير الختامية")
    st.date_input("اختر الفترة")
    col_f1, col_f2 = st.columns(2)
    col_f1.success(f"إجمالي الأرباح: 45,000 ج.م")
    col_f2.error(f"إجمالي المصاريف: 12,000 ج.م")
