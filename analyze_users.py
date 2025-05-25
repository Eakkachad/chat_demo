from user_manager import UserManager
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.font_manager as fm  # เพิ่มบรรทัดนี้
import os
import json
import pandas as pd
import streamlit as st
from datetime import datetime

def setup_fonts():
    """ตั้งค่าฟอนต์สำหรับแสดงผลภาษาไทย"""
    try:
        # ลองหาฟอนต์ไทยที่ติดตั้งในระบบ
        thai_fonts = [
            f.name for f in fm.fontManager.ttflist 
            if 'thai' in f.name.lower() 
            or 'sarabun' in f.name.lower()
            or 'tahoma' in f.name.lower()
        ]
        
        if thai_fonts:
            rcParams['font.family'] = thai_fonts[0]
        else:
            # หากไม่พบฟอนต์ไทย ใช้ฟอนต์อื่นที่รองรับ Unicode
            rcParams['font.family'] = 'Tahoma'
            
        rcParams['font.size'] = 12
    except Exception as e:
        st.warning(f"ไม่สามารถตั้งค่าฟอนต์ไทยได้: {e}")
        rcParams['font.family'] = 'sans-serif'

def visualize_user_data():
    """แสดงผลวิเคราะห์ข้อมูลผู้ใช้"""
    setup_fonts()
    
    user_manager = UserManager()
    analysis = user_manager.analyze_all_users()
    
    # แสดงข้อมูลทั่วไป
    st.subheader("ข้อมูลทั่วไป")
    col1, col2 = st.columns(2)
    col1.metric("จำนวนผู้ใช้ทั้งหมด", f"{analysis['total_users']} คน")
    
    # แสดงความสนใจยอดนิยม (Top 10)
    st.subheader("10 ความสนใจยอดนิยม")
    if analysis['common_interests']:
        interests_df = pd.DataFrame(
            sorted(analysis['common_interests'].items(), key=lambda x: x[1], reverse=True)[:10],
            columns=['ความสนใจ', 'จำนวน']
        )
        st.bar_chart(interests_df.set_index('ความสนใจ'))
    else:
        st.warning("ยังไม่มีข้อมูลความสนใจของผู้ใช้")
    
    # แสดงสไตล์การพูด
    st.subheader("สไตล์การพูดของผู้ใช้")
    if analysis['common_styles']:
        styles_df = pd.DataFrame(
            sorted(analysis['common_styles'].items(), key=lambda x: x[1], reverse=True),
            columns=['สไตล์', 'จำนวน']
        )
        st.dataframe(styles_df)
    else:
        st.warning("ยังไม่มีข้อมูลสไตล์การพูด")
    
    # แสดงตัวอย่างข้อมูลผู้ใช้
    st.subheader("ตัวอย่างข้อมูลผู้ใช้")
    user_files = user_manager.get_all_user_files()[:3]  # แสดง 3 รายการแรก
    for file in user_files:
        with open(os.path.join(user_manager.data_dir, file), 'r', encoding='utf-8') as f:
            user_data = json.load(f)
            with st.expander(f"ผู้ใช้: {file.replace('user_', '').replace('.json', '')}"):
                st.json(user_data)

if __name__ == "__main__":
    st.set_page_config(
        page_title="แดชบอร์ดวิเคราะห์ผู้ใช้แชทบอท",
        layout="wide"
    )
    st.title("📊 แดชบอร์ดวิเคราะห์ผู้ใช้แชทบอท")
    visualize_user_data()