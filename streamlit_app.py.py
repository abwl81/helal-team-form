import streamlit as st
import pandas as pd
import os

# مسیر فایل CSV (در لوکال یا Streamlit Cloud)
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
# رابط کاربری فرم برای تمام کاربران
# ---------------------------------------------------
st.title("📋 فرم ثبت اطلاعات اعضای تیم")
st.write("لطفاً مشخصات خود را کامل وارد کنید:")

full_name = st.text_input("نام و نام خانوادگی *")
phone = st.text_input("شماره تماس *")
major = st.text_input("رشته تحصیلی *")
degree = st.text_input("درجه امدادگری (اختیاری)")
num_tim = st.text_input("شماره تیم خود را وارد کنید *", placeholder="مثلاً 7")

# ----- دکمه ثبت -----
if st.button("📨 ثبت اطلاعات"):
    if not full_name or not phone or not major or not num_tim:
        st.error("⚠️ لطفاً همه فیلدهای اجباری را پر کنید.")
    else:
        df = pd.read_csv(FILE_PATH)
        new_row = pd.DataFrame(
            [[full_name, phone, major, degree, num_tim]], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(FILE_PATH, index=False, encoding="utf-8-sig")
        st.success("✅ اطلاعات با موفقیت ذخیره شد!")

# ---------------------------------------------------
st.markdown("---")

# ---------------------------------------------------
# 🔐 بخش مخصوص مدیر (رمز عبور)
# ---------------------------------------------------
st.subheader("🛡️ بخش مدیریت (فقط مخصوص سرتیم)")

# رمز را به‌صورت دستی یا از st.secrets بخوان
# برای امنیت بالاتر در Streamlit Cloud، بعداً این خط را با st.secrets جایگزین کن

MASTER_PASSWORD = st.secrets["MASTER_PASSWORD"]

admin_pass = st.text_input("رمز عبور مدیر را وارد کنید:", type="password")

if admin_pass == MASTER_PASSWORD:
    st.success("✅ خوش آمدی! دسترسی مدیر فعال است.")

    # نمایش داده‌ها
    df = pd.read_csv(FILE_PATH)
    st.write("📄 اطلاعات فعلی ثبت‌شده:")
    st.dataframe(df)

    # دکمه دانلود فقط برای مدیر
    st.download_button(
        label="📁 دانلود فایل CSV اعضا",
        data=open(FILE_PATH, "rb").read(),
        file_name="team_members.csv",
        mime="text/csv"
    )
elif admin_pass != "":
    st.error("❌ رمز اشتباه است. دسترسی ندارید.")

# ---------------------------------------------------
# پایان برنامه
# ---------------------------------------------------
