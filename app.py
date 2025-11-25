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
st.markdown('<div class="header-section">', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">📋 فرم ثبت اطلاعات اعضای تیم</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">لطفاً مشخصات خود را کامل وارد کنید:</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="form-container">', unsafe_allow_html=True)

# فیلدهای ورودی با لیبل‌های سفارشی
st.markdown('<label class="field-label">نام و نام خانوادگی <span class="required">*</span></label>', unsafe_allow_html=True)
full_name = st.text_input("نام و نام خانوادگی", label_visibility="collapsed", key="name")

st.markdown('<label class="field-label">شماره تماس <span class="required">*</span></label>', unsafe_allow_html=True)
phone = st.text_input("شماره تماس", label_visibility="collapsed", key="phone")

st.markdown('<label class="field-label">رشته تحصیلی <span class="required">*</span></label>', unsafe_allow_html=True)
major = st.text_input("رشته تحصیلی", label_visibility="collapsed", key="major")

st.markdown('<label class="field-label">درجه امدادگری (اختیاری)</label>', unsafe_allow_html=True)
degree = st.text_input("درجه امدادگری", label_visibility="collapsed", key="degree")

st.markdown('<label class="field-label">شماره تیم خود را وارد کنید (عدد وارد کنید) <span class="required">*</span></label>', unsafe_allow_html=True)
num_tim = st.text_input("شماره تیم", placeholder="مثلاً 7", label_visibility="collapsed", key="team")

# ----- دکمه ثبت -----
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("📨 ثبت اطلاعات", use_container_width=True):
        if not full_name or not phone or not major or not num_tim:
            st.markdown('<div class="error-message">⚠️ لطفاً همه فیلدهای اجباری را پر کنید.</div>', unsafe_allow_html=True)
        else:
            df = pd.read_csv(FILE_PATH)
            new_row = pd.DataFrame([[full_name, phone, major, degree, num_tim]], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(FILE_PATH, index=False, encoding="utf-8-sig")
            st.markdown('<div class="success-message">✅ اطلاعات با موفقیت ذخیره شد!</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ---------------------------------------------------
# 🔐 بخش مخصوص مدیر (با رمز عبور)
# ---------------------------------------------------
st.markdown('<div class="admin-section">', unsafe_allow_html=True)
st.markdown('<h2 class="admin-title">🛡️ بخش مدیریت</h2>', unsafe_allow_html=True)

MASTER_PASSWORD = os.getenv("MASTER_PASSWORD")

admin_pass = st.text_input("رمز عبور مدیر را وارد کنید:", type="password", key="admin_pass")

if admin_pass == MASTER_PASSWORD:
    st.markdown('<div class="success-message">✅ خوش آمدی! دسترسی مدیر فعال است.</div>', unsafe_allow_html=True)

    df = pd.read_csv(FILE_PATH)
    st.markdown('<p class="data-title">📄 اطلاعات فعلی ثبت‌شده:</p>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    # دکمه دانلود فایل CSV
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📁 دانلود فایل CSV اعضا",
            data=open(FILE_PATH, "rb").read(),
            file_name="team_members.csv",
            mime="text/csv",
            use_container_width=True
        )

elif admin_pass != "":
    st.markdown('<div class="error-message">❌ رمز اشتباه است. دسترسی ندارید.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# 👣 امضای پایین صفحه
# ---------------------------------------------------
st.markdown(
    """
    <div class="footer">
        <p>🛠️ طراحی و توسعه توسط <strong>مهندس ابوالفضل عابدی</strong></p>
    </div>
    """,
    unsafe_allow_html=True,
)
