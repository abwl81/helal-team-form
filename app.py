import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime
import pytz  # اضافه شد
# ---------------------------------------------------
# 📦 Load custom CSS
# ---------------------------------------------------
def local_css(file_name):
    css_path = Path(__file__).parent / file_name
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# ---------------------------------------------------
# اتصال به دیتابیس SQLite
# ---------------------------------------------------
DB_PATH = "team_data.db"

def init_db():
    """ایجاد دیتابیس و جدول در صورت نبود"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            major TEXT NOT NULL,
            first_aid_degree TEXT,
            team_number TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def insert_member(full_name, phone, major, degree, team_number):
    """درج عضو جدید با زمان ایران"""
    # تنظیم timezone ایران
    iran_tz = pytz.timezone('Asia/Tehran')
    now = datetime.now(iran_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO team_members (full_name, phone, major, first_aid_degree, team_number, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (full_name, phone, major, degree, team_number, now))
    conn.commit()
    conn.close()


def get_all_members():
    """دریافت همه اعضا"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT 
            full_name as 'نام و نام خانوادگی',
            phone as 'شماره تماس',
            major as 'رشته تحصیلی',
            first_aid_degree as 'درجه امدادگری',
            team_number as 'شماره تیم',
            created_at as 'تاریخ ثبت'
        FROM team_members
        ORDER BY id DESC
    """, conn)
    conn.close()
    return df

# ایجاد دیتابیس در اولین اجرا
init_db()

# ---------------------------------------------------
# 📋 رابط کاربری فرم برای عموم کاربران
# ---------------------------------------------------

# هدر با آیکون
st.markdown(
    """
    <div class="header-container">
        <div class="header-icon">📋</div>
        <h1 class="main-title">فرم ثبت اطلاعات اعضای تیم</h1>
        <p class="subtitle">لطفاً مشخصات خود را کامل وارد کنید</p>
    </div>
    """,
    unsafe_allow_html=True
)

# شروع باکس فرم
st.markdown('<div class="form-box">', unsafe_allow_html=True)

# فیلدهای ورودی
st.markdown('<div class="input-group">', unsafe_allow_html=True)
st.markdown('<label class="input-label">نام و نام خانوادگی <span class="required">*</span></label>', unsafe_allow_html=True)
full_name = st.text_input("نام", label_visibility="collapsed", key="name", placeholder="نام و نام خانوادگی خود را وارد کنید")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="input-group">', unsafe_allow_html=True)
st.markdown('<label class="input-label">شماره تماس <span class="required">*</span></label>', unsafe_allow_html=True)
phone = st.text_input("موبایل", label_visibility="collapsed", key="phone", placeholder="مثال: 09123456789")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="input-group">', unsafe_allow_html=True)
st.markdown('<label class="input-label">رشته تحصیلی <span class="required">*</span></label>', unsafe_allow_html=True)
major = st.text_input("رشته", label_visibility="collapsed", key="major", placeholder="رشته تحصیلی خود را وارد کنید")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="input-group">', unsafe_allow_html=True)
st.markdown('<label class="input-label">درجه امدادگری <span class="optional">(اختیاری)</span></label>', unsafe_allow_html=True)
degree = st.text_input("درجه", label_visibility="collapsed", key="degree", placeholder="در صورت داشتن وارد کنید")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="input-group">', unsafe_allow_html=True)
st.markdown('<label class="input-label">شماره تیم <span class="required">*</span></label>', unsafe_allow_html=True)
num_tim = st.text_input("تیم", label_visibility="collapsed", key="team", placeholder="مثال: 7")
st.markdown('</div>', unsafe_allow_html=True)

# دکمه ثبت
if st.button("📨 ثبت اطلاعات", use_container_width=True, key="submit_btn"):
    if not full_name or not phone or not major or not num_tim:
        st.markdown(
            '<div class="alert alert-error">⚠️ لطفاً همه فیلدهای اجباری را پر کنید.</div>',
            unsafe_allow_html=True
        )
    else:
        try:
            insert_member(full_name, phone, major, degree, num_tim)
            st.markdown(
                '<div class="alert alert-success">✅ اطلاعات با موفقیت ذخیره شد!</div>',
                unsafe_allow_html=True
            )
        except Exception as e:
            st.markdown(
                f'<div class="alert alert-error">❌ خطا در ذخیره‌سازی: {str(e)}</div>',
                unsafe_allow_html=True
            )

# پایان باکس فرم
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ---------------------------------------------------
# 🔐 بخش مخصوص مدیر (با رمز عبور)
# ---------------------------------------------------
st.markdown('<div class="admin-container">', unsafe_allow_html=True)
st.markdown('<h2 class="admin-title">🛡️ بخش مدیریت</h2>', unsafe_allow_html=True)

import os
MASTER_PASSWORD = os.getenv("MASTER_PASSWORD")  # رمز پیش‌فرض

# فیلد رمز عبور داخل باکس
st.markdown('<div class="input-group">', unsafe_allow_html=True)
st.markdown('<label class="input-label">رمز عبور مدیر</label>', unsafe_allow_html=True)
admin_pass = st.text_input(
    "رمز",
    type="password",
    key="admin_pass",
    placeholder="رمز عبور",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

if admin_pass == MASTER_PASSWORD:
    st.markdown(
        '<div class="alert alert-success">✅ خوش آمدی! دسترسی مدیر فعال است.</div>',
        unsafe_allow_html=True
    )

    df = get_all_members()
    
    if len(df) > 0:
        st.markdown('<p class="table-title">📄 اطلاعات فعلی ثبت‌شده:</p>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

        # دکمه دانلود CSV
        csv_data = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="📁 دانلود فایل CSV اعضا",
            data=csv_data,
            file_name=f"team_members_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
            key="download_btn"
        )
        
        # دکمه دانلود Excel
        from io import BytesIO
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='اعضا')
        buffer.seek(0)
        
        st.download_button(
            label="📊 دانلود فایل Excel اعضا",
            data=buffer,
            file_name=f"team_members_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="download_excel_btn"
        )
    else:
        st.markdown(
            '<div class="alert alert-error">📭 هنوز داده‌ای ثبت نشده است.</div>',
            unsafe_allow_html=True
        )

elif admin_pass != "":
    st.markdown(
        '<div class="alert alert-error">❌ رمز اشتباه است. دسترسی ندارید.</div>',
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# 👣 امضای پایین صفحه
# ---------------------------------------------------
st.markdown(
    """
    <div class="footer-signature">
        <p>🛠️ طراحی و توسعه توسط <strong>مهندس ابوالفضل عابدی</strong></p>
    </div>
    """,
    unsafe_allow_html=True,
)


