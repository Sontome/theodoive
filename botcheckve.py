import gspread
import requests
import time
from datetime import datetime

# ==== Cấu hình ====
SHEET_URL = "https://docs.google.com/spreadsheets/d/1PSPIrxo7sVRz-GUKUoNPb_-yrZEUcHC-Rsg66k_lfLM/edit?usp=sharing"
API_URL = "https://thuhongtour.com/vj/check-ve-v2"
DELAY = 15 * 60  # 15 phút
SO_LAN_LAP = 10  # Số lần lặp

# ==== Kết nối Google Sheets ====
gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_url(SHEET_URL)
ws = sh.sheet1

def call_api(dep0, arr0, depdate0):
    payload = {
        "dep0": dep0,
        "arr0": arr0,
        "depdate0": depdate0,
        "depdate1": "",
        "adt": "1",
        "chd": "0",
        "inf": "0",
        "sochieu": "OW"
    }
    try:
        res = requests.post(API_URL, json=payload, headers={
            "accept": "application/json",
            "Content-Type": "application/json"
        }, timeout=20)
        res.raise_for_status()
        data = res.json()
        body = data.get("body", [])
        if body:
            vé = body[0]
            giá_vé = vé.get("thông_tin_chung", {}).get("giá_vé", "")
            booking = vé.get("chiều_đi", {}).get("BookingKey", "")
            return {
                "giá_vé": giá_vé,
                "BookingKey": booking
            }
    except Exception as e:
        print(f"💥 Lỗi gọi API với {dep0}-{arr0}-{depdate0}: {e}")
    return {}

def xử_lý_dữ_liệu(lần_thứ):
    col = 4 + lần_thứ  # cột D là 4, lần 0 -> D, lần 1 -> E,...
    label = f"Lần {lần_thứ + 1} - " + datetime.now().strftime("%Y-%m-%d %H:%M")
    ws.update_cell(1, col, label)
    rows = ws.get_all_values()
    for i in range(2, len(rows)):
        time.sleep(5) # dòng 3 trở đi (index 2)
        row = rows[i]
        if len(row) < 3 or not all(row[:3]):
            continue  # skip dòng thiếu A/B/C

        dep0, arr0, depdate0 = row[:3]
        kq = call_api(dep0, arr0, depdate0)
        if kq:
            text = f'{kq["giá_vé"]} | {kq["BookingKey"]}'
            ws.update_cell(i + 1, col, text)
        else:
            ws.update_cell(i + 1, col, "Lỗi/Không có vé")

# ==== Chạy lặp 10 lần ====
for lần in range(SO_LAN_LAP):
    print(f"🔥 Đang chạy lần {lần + 1}...")
    xử_lý_dữ_liệu(lần)
    if lần < SO_LAN_LAP - 1:
        print("⏳ Nghỉ 15 phút...")
        time.sleep(DELAY)

print("✅ Done 10 lần rồi đại ca êii!")
