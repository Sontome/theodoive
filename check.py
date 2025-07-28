import requests
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

def convert_date_format(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except:
        return date_str

def loc_chuyen_bay_theo_gio(list_danh_sach, gio_di_chieu_di, gio_di_chieu_ve=""):
    result = None
    for chuyen_bay in list_danh_sach:
        gio_cat_canh_chieu_di = chuyen_bay.get("chiều_đi", {}).get("giờ_cất_cánh", "")
        gio_cat_canh_chieu_ve = chuyen_bay.get("chiều_về", {}).get("giờ_cất_cánh", "")
        if (gio_cat_canh_chieu_di == gio_di_chieu_di and gio_cat_canh_chieu_ve == gio_di_chieu_ve):
            result = chuyen_bay
            break
    return result

def process_item(item):
    try:
        hang = item.get("hang", "")
        giờ_đi_chiều_đi = item.get("giodi", "")
        giờ_đi_chiều_về = item.get("giove", "")
        depdate0 = convert_date_format(item.get("ngaydi", ""))
        depdate1 = convert_date_format(item.get("ngayve", ""))
        dep0 = item.get("noidi", "")
        arr0 = item.get("noiden", "")

        sochieu = "OW" if not depdate1 else "RT"

        payload = {
            "dep0": dep0, "arr0": arr0,
            "depdate0": depdate0, "depdate1": depdate1,
            "adt": "1", "chd": "0", "inf": "0",
            "sochieu": sochieu
        }

        payloadvna = {
            **payload,
            "activedVia": "0",
            "activedIDT": "ADT,VFR",
            "page": "1",
            "filterTimeSlideMin0": "5",
            "filterTimeSlideMax0": "2355",
            "filterTimeSlideMin1": "5",
            "filterTimeSlideMax1": "2355",
            "session_key": ""
        }

        urlvj = "https://thuhongtour.com/vj/check-ve-v2"
        urlvna = "https://thuhongtour.com/vna/check-ve-v2"

        if hang == "VJ":
            res = requests.post(urlvj, json=payload, timeout=10)
        else:
            res = requests.post(urlvna, json=payloadvna, timeout=25)

        if not res.ok:
            return item, f"❌ {item.get('pnr')} -> Lỗi response: {res.status_code}"

        ress = res.json()
        listchuyenbay = []

        if hang == "VJ":
            listchuyenbay = ress.get("body", [])
        else:
            ve_vfr = [ve for ve in ress["body"] if ve["thông_tin_chung"]["hành_lý_vna"] == "VFR"]
            ve_adt = [ve for ve in ress["body"] if ve["thông_tin_chung"]["hành_lý_vna"] == "ADT"]
            listchuyenbay = ve_vfr if ve_vfr else ve_adt

        if not listchuyenbay:
            return item, f"❌ {item.get('pnr')} -> Không có chuyến bay phù hợp"

        result = loc_chuyen_bay_theo_gio(listchuyenbay, giờ_đi_chiều_đi, giờ_đi_chiều_về)
        if result is None:
            result = listchuyenbay[0]

        giacu = int(item.get("giatong", 0))
        giamoi = int(result.get("thông_tin_chung", {}).get("giá_vé", 0))

        if result is None or giamoi >= giacu:
            result1 = listchuyenbay[0]
            giamoi_0 = int(result1.get("thông_tin_chung", {}).get("giá_vé", 0))
            if giamoi_0 < giacu:
                result = result1

        if giờ_đi_chiều_đi == "" or giacu == 0:
            item["giodi"] = result.get("chiều_đi", {}).get("giờ_cất_cánh", "")
            if depdate1:
                item["giove"] = result.get("chiều_về", {}).get("giờ_cất_cánh", "")
            item["hanh_ly"] = result.get("thông_tin_chung", {}).get("hành_lý_vna", "")
            item["giatong"] = result.get("thông_tin_chung", {}).get("giá_vé", 0)
            item["hang"] = hang
        else:
            item["giacu_cunggio_moitong"] = result.get("thông_tin_chung", {}).get("giá_vé", 0)
            item["giodi_moi"] = result.get("chiều_đi", {}).get("giờ_cất_cánh", "")
            if depdate1:
                item["giove_moi"] = result.get("chiều_về", {}).get("giờ_cất_cánh", "")
            item["hanh_ly_moi"] = result.get("thông_tin_chung", {}).get("hành_lý_vna", "")

        return item, result
    except Exception as e:
        return item, f"❌ {item.get('pnr')} -> Lỗi xử lý: {e}"

def check_all_pnrs(data_file="data.json"):
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return f"Lỗi đọc file dữ liệu: {e}"

    if not data:
        return "Không có dữ liệu để check."

    datanew = []
    result_lines = []

    with ThreadPoolExecutor(max_workers=10) as executor:  # max 10 luồng, chỉnh tăng nếu mạng khỏe
        futures = [executor.submit(process_item, item) for item in data]

        for future in as_completed(futures):
            item, result = future.result()
            datanew.append(item)
            result_lines.append(str(result))

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(datanew, f, ensure_ascii=False, indent=4)

    with open("log.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(result_lines))

    return result_lines
