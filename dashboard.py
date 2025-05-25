import streamlit as st
from user_manager import UserManager
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os
import json

# ตั้งค่าฟอนต์ไทย
def setup_fonts():
    try:
        rcParams['font.family'] = 'Sarabun'
        rcParams['font.size'] = 12
    except:
        rcParams['font.family'] = 'Tahoma'

def main():
    setup_fonts()
    st.set_page_config(
        page_title="แดชบอร์ดวิเคราะห์ผู้ใช้",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📊 แดชบอร์ดวิเคราะห์ผู้ใช้แชทบอท")
    st.markdown("---")
    
    user_manager = UserManager()
    
    # ส่วนแสดงข้อมูลทั่วไป
    st.header("ข้อมูลทั่วไป")
    user_files = user_manager.get_all_user_files()
    col1, col2 = st.columns(2)
    col1.metric("จำนวนผู้ใช้ทั้งหมด", len(user_files))
    
    # ส่วนวิเคราะห์ความสนใจ
    st.header("ความสนใจยอดนิยม")
    interests = {}
    for file in user_files:
        with open(os.path.join(user_manager.data_dir, file), 'r', encoding='utf-8') as f:
            data = json.load(f)
            for interest in data.get('interests', []):
                interests[interest] = interests.get(interest, 0) + 1
    
    if interests:
        df_interests = pd.DataFrame.from_dict(interests, orient='index', columns=['จำนวน']).sort_values('จำนวน', ascending=False)
        st.bar_chart(df_interests.head(10))
    else:
        st.warning("ยังไม่มีข้อมูลความสนใจของผู้ใช้")
    
    # ส่วนวิเคราะห์สไตล์การพูด
    st.header("สไตล์การพูด")
    styles = {}
    for file in user_files:
        with open(os.path.join(user_manager.data_dir, file), 'r', encoding='utf-8') as f:
            data = json.load(f)
            for style in data.get('styles', []):
                styles[style] = styles.get(style, 0) + 1
    
    if styles:
        df_styles = pd.DataFrame.from_dict(styles, orient='index', columns=['จำนวน']).sort_values('จำนวน', ascending=False)
        st.dataframe(df_styles)
    else:
        st.warning("ยังไม่มีข้อมูลสไตล์การพูด")
    
    # ส่วนแสดงข้อมูลผู้ใช้ตัวอย่าง
    st.header("ข้อมูลผู้ใช้ตัวอย่าง")
    if user_files:
        selected_file = st.selectbox("เลือกผู้ใช้", user_files[:10])
        with open(os.path.join(user_manager.data_dir, selected_file), 'r', encoding='utf-8') as f:
            user_data = json.load(f)
            st.json(user_data)
    else:
        st.warning("ยังไม่มีข้อมูลผู้ใช้")

if __name__ == "__main__":
    main()