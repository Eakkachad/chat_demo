import speech_recognition as sr
from typing import Optional

class VoiceInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def listen(self) -> Optional[str]:
        """ฟังก์ชันรับเสียงและแปลงเป็นข้อความ"""
        with sr.Microphone() as source:
            print("\nกำลังฟัง... (พูดได้เลย)")
            try:
                # ปรับเสียงรบกวนอัตโนมัติ
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                # ใช้ Google Web Speech API
                text = self.recognizer.recognize_google(audio, language="th-TH")
                print(f"คุณพูดว่า: {text}")
                return text
            except sr.WaitTimeoutError:
                print("ไม่พบเสียงพูด กรุณาลองอีกครั้ง")
            except sr.UnknownValueError:
                print("ไม่สามารถเข้าใจเสียงพูด")
            except Exception as e:
                print(f"เกิดข้อผิดพลาด: {e}")
            return None

if __name__ == "__main__":
    # ทดสอบการทำงาน
    vi = VoiceInput()
    while True:
        input("กด Enter เพื่อเริ่มพูด...")
        result = vi.listen()
        if result:
            print(f"ข้อความที่ได้: {result}")