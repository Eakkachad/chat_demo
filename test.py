from user_manager import UserManager
from datetime import datetime
import os

def test():
    manager = UserManager()
    test_id = "debug_user"
    test_data = {
        "styles": ["formal"],
        "interests": ["AI"],
        "history": ["test message"],
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
    }
    
    # ทดสอบบันทึก
    if manager.save_user_profile(test_id, test_data):
        print("\n=== TEST PASSED ===")
        print(f"ตรวจสอบไฟล์ที่: {os.path.abspath(manager.get_user_filepath(test_id))}")
    else:
        print("\n=== TEST FAILED ===")

if __name__ == "__main__":
    test()