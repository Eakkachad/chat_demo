import json
import os
from typing import Dict, Any, List
from datetime import datetime

class UserManager:
    def __init__(self, data_dir: str = "user_data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
    
    def get_user_filepath(self, user_id: str) -> str:
        """สร้าง path ไฟล์จาก user_id"""
        return os.path.join(self.data_dir, f"user_{user_id}.json")
    
    def load_user_profile(self, user_id: str) -> Dict[str, Any]:
        """โหลดข้อมูลผู้ใช้จากไฟล์"""
        filepath = self.get_user_filepath(user_id)
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "styles": [],
                "interests": [],
                "history": [],
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat()
                }
            }
    
    def save_user_profile(self, user_id: str, profile: Dict[str, Any]) -> bool:
        filepath = self.get_user_filepath(user_id)
        print(f"\n=== DEBUG SAVE PATH ===")
        print(f"กำลังบันทึกที่: {os.path.abspath(filepath)}")

        try:
            # ตรวจสอบโครงสร้างข้อมูล
            required = {
                'styles': [],
                'interests': [],
                'history': [],
                'metadata': {'created_at': '', 'last_updated': ''}
            }
            for key, default in required.items():
                if key not in profile:
                    profile[key] = default

            # บันทึกไฟล์
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(profile, f, ensure_ascii=False, indent=2)
            
            print("✅ บันทึกไฟล์สำเร็จ!")
            return True
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดขณะบันทึก: {e}")
            return False
    
    def get_all_user_files(self) -> List[str]:
        """ดึงรายการไฟล์ผู้ใช้ทั้งหมด"""
        return [f for f in os.listdir(self.data_dir) 
                if f.startswith("user_") and f.endswith(".json")]
    
    def analyze_all_users(self) -> Dict[str, Any]:
        """วิเคราะห์ข้อมูลผู้ใช้ทั้งหมด"""
        user_files = self.get_all_user_files()
        analysis = {
            "total_users": len(user_files),
            "common_interests": {},
            "common_styles": {},
            "active_users": []
        }
        
        for file in user_files:
            try:
                with open(os.path.join(self.data_dir, file), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # นับความสนใจ
                    for interest in data.get("interests", []):
                        analysis["common_interests"][interest] = analysis["common_interests"].get(interest, 0) + 1
                    
                    # นับสไตล์การพูด
                    for style in data.get("styles", []):
                        analysis["common_styles"][style] = analysis["common_styles"].get(style, 0) + 1
                    
                    # เก็บข้อมูลผู้ใช้ที่ active
                    last_updated = datetime.fromisoformat(data['metadata']['last_updated'])
                    if (datetime.now() - last_updated).days < 30:  # active ใน 30 วัน
                        analysis["active_users"].append({
                            "user_id": file.replace("user_", "").replace(".json", ""),
                            "last_active": data['metadata']['last_updated'],
                            "message_count": len(data.get("history", []))
                        })
            except Exception as e:
                print(f"Error processing {file}: {e}")
        
        return analysis  # เพิ่มการ return ค่า analysis
    
    def get_conversation_history(self, user_id: str, limit: int = 5) -> List[str]:
        """ดึงประวัติการสนทนาย้อนหลัง"""
        profile = self.load_user_profile(user_id)
        return profile.get("history", [])[-limit:]
    
    def get_user_interests(self, user_id: str) -> List[str]:
        """ดึงความสนใจของผู้ใช้ (ไม่ซ้ำกัน)"""
        profile = self.load_user_profile(user_id)
        return list(set(profile.get("interests", [])))
    
    def get_user_style(self, user_id: str) -> str:
        """ดึงสไตล์การพูดล่าสุดของผู้ใช้"""
        profile = self.load_user_profile(user_id)
        return profile.get("styles", ["neutral"])[-1]