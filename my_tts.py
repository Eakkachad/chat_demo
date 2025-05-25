from gtts import gTTS
import pyglet
import os
from typing import Optional

class TextToSpeech:
    def __init__(self, lang='th'):
        self.lang = lang
        self.temp_file = "temp_speech.mp3"
        
    def speak(self, text: str) -> Optional[str]:
        """แปลงข้อความเป็นเสียงพูดและเล่นเสียง"""
        try:
            # สร้างเสียงจากข้อความ
            tts = gTTS(text=text, lang=self.lang, slow=False)
            
            # บันทึกไฟล์ชั่วคราว
            tts.save(self.temp_file)
            
            # เล่นเสียงด้วย pyglet
            sound = pyglet.media.load(self.temp_file)
            sound.play()
            
            # รอให้เสียงเล่นจบ
            pyglet.app.run()
            
            # ลบไฟล์ชั่วคราว
            os.remove(self.temp_file)
            
            return None
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการแปลงข้อความเป็นเสียง: {e}")
            return str(e)
        finally:
            # ปิด pyglet เมื่อเสร็จสิ้น
            pyglet.app.exit()