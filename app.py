import streamlit as st
import pandas as pd
import os
from pathlib import Path

# ---------------------------------------------------
# 📦 Load custom CSS
# ---------------------------------------------------
def local_css(file_name):
    css_path = Path(__file__).parent / file_name
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# ---------------------------------------------------
# مسیر فایل CSV
# ---------------------------------------------------
FILE_PATH = "team_data.csv"

# ساخت فایل در صورت نبود
if not os.path.exists(FILE_PATH):
    df = pd.DataFrame(columns=[
        "نام و نام خانوادگی",
        "شماره تماس",
        "رشته تحصیلی",
        "درجه امدادگری",
        "شماره تیم"
    ])
    df.to_csv(FILE_PATH, index=False, encoding="utf-8-sig")

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
        df = pd.read_csv(FILE_PATH)
        new_row = pd.DataFrame([[full_name, phone, major, degree, num_tim]], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(FILE_PATH, index=False, encoding="utf-8-sig")
        st.markdown(
            '<div class="alert alert-success">✅ اطلاعات با موفقیت ذخیره شد!</div>',
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

MASTER_PASSWORD = os.getenv("MASTER_PASSWORD")

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

    df = pd.read_csv(FILE_PATH)
    st.markdown('<p class="table-title">📄 اطلاعات فعلی ثبت‌شده:</p>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    # دکمه دانلود فایل CSV
    st.download_button(
        label="📁 دانلود فایل CSV اعضا",
        data=open(FILE_PATH, "rb").read(),
        file_name="team_members.csv",
        mime="text/csv",
        use_container_width=True,
        key="download_btn"
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
