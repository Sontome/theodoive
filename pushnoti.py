import requests
import json
import os,sys
import configparser

def get_user_data_path(filename):
    """Lưu file cấu hình/data trong cùng thư mục với .exe hoặc file .py"""
    if getattr(sys, 'frozen', False):
        # Nếu chạy từ file .exe (frozen = True)
        return os.path.join(os.path.dirname(sys.executable), filename)
    else:
        # Khi chạy file .py
        return os.path.join(os.path.dirname(__file__), filename)
class PushNotiTelegram:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        

    def send(self, message: str):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            print("🔔 Noti đã gửi tới Telegram cho đại ca rồi 😎")
        except Exception as e:
            print("❌ Lỗi gửi Telegram:", e)

    def push_from_data(self):
        if not os.path.exists(get_user_data_path("data.json")):
            return ("")
        
        # Load config.ini
        config = configparser.ConfigParser()
        config.read(get_user_data_path("config.ini"))
        notify_cfg = config["NOTIFY"] if config.has_section("NOTIFY") else {}

        same_hour = notify_cfg.get("same_hour", "true").lower() == "true"
        diff_hour = notify_cfg.get("diff_hour", "true").lower() == "true"
        print(same_hour,diff_hour)

        data = []
        with open(get_user_data_path("data.json"), "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return ("")

        message = ""
        for chuyen in data:
            try:
                giacu = int(chuyen.get("giatong", 0))
                giatong = int(chuyen.get("giacu_cunggio_moitong", 0))
                if giacu <= giatong:
                    continue  # Không rẻ hơn thì skip

                giodi = chuyen.get("giodi", "")
                giove = chuyen.get("giove", "")
                giodi_moi = chuyen.get("giodi_moi", "")
                giove_moi = chuyen.get("giove_moi", "")
                ngaydi = chuyen.get("ngaydi", "")
                ngayve = chuyen.get("ngayve", "")
                pnr = chuyen.get("pnr", "???")
                noidi = chuyen.get("noidi", "???")
                noiden = chuyen.get("noiden", "???")

                
                if giodi != giodi_moi or giove != giove_moi:
                    time = "khác giờ"
                    if  diff_hour:
                        message += f"✈️ Chuyến bay {pnr}: {noidi}-{noiden} {ngaydi}-{ngayve} có giá vé rẻ hơn ({time})\n"
                else:
                    time = "cùng giờ"
                    if same_hour:
                        message += f"✈️ Chuyến bay {pnr}: {noidi}-{noiden} {ngaydi}-{ngayve} có giá vé rẻ hơn ({time})\n"

                

                

            except Exception as e:
                print(f"⚠️ Lỗi xử lý chuyến bay: {e}")
                continue

        if message:
            print(message)
            self.send(message)
        else:
            print("chưa có chuyến rẻ hơn")