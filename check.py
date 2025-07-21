# check.py
import requests
import json
from datetime import datetime

def convert_date_format(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except:
        return date_str  # fallback nếu lỗi

def check_all_pnrs(data_file="data.json"):
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return f"Lỗi đọc file dữ liệu: {e}"

    if not data:
        return "Không có dữ liệu để check."

    result_lines = []
    datanew = []
    for item in data:
        try:
            giờ_đi_chiều_đi = item.get("giodi", "")
            giờ_đi_chiều_về = item.get("giove", "")
            depdate0 = convert_date_format(item.get("ngaydi", ""))
            depdate1 = convert_date_format(item.get("ngayve", ""))
            dep0= item.get("noidi", "")
            arr0= item.get("noiden", "")
            if depdate1 =="":
                sochieu = "OW"
            else:
                sochieu = "RT"
            payload = {
                
                "dep0": dep0,
                "arr0": arr0,
                "depdate0": depdate0,
                "depdate1": depdate1,
                "adt": "1",
                "chd": "0",
                "inf": "0",
                "sochieu": sochieu
                
            }
            
            res = requests.post("https://thuhongtour.com/vj/check-ve-v2", json=payload, timeout=10)
            
            if res.ok:
                ress = res.json()
                print (item)
                
                listchuyenbay = ress.get("body",[])
                print (listchuyenbay)
                result = loc_chuyen_bay_theo_gio(listchuyenbay,giờ_đi_chiều_đi,giờ_đi_chiều_về)
                #print(result)
                if result == None:
                    result = listchuyenbay[0]  
                print(result)  
                giacu= item.get("giatong",0)
                print(giacu)
                giamoi = result.get("thông_tin_chung","").get("giá_vé",0)
                
                
                if result == None or int(giamoi) >= int(giacu) :
                    result = listchuyenbay[0]
                    
                    giamoi = result.get("thông_tin_chung","").get("giá_vé",0)
                    
                
                result_lines.append(result)
                
                if giờ_đi_chiều_đi == "" or giacu =="" or giacu == 0:
                    item["giodi"]= result.get("chiều_đi","").get("giờ_cất_cánh","")
                    if depdate1:
                        item["giove"]= result.get("chiều_về",{}).get("giờ_cất_cánh","")
                        item["giave"]= result.get("chiều_về",{}).get("giá_vé_gốc",0)
                    item["somb"]= ""
                    item["giatong"]= result.get("thông_tin_chung",{}).get("giá_vé",0)
                    item["giadi"]= result.get("chiều_đi",{}).get("giá_vé_gốc",0)
                    
                    item["hang"]= "VJ"
                else  :
                    item["giacu_cunggio_moitong"] = result.get("thông_tin_chung","").get("giá_vé",0)
                    item["giodi_moi"] = result.get("chiều_đi","").get("giờ_cất_cánh","")
                    if depdate1:
                        item["giove_moi"] = result.get("chiều_về",{}).get("giờ_cất_cánh","")
                        item["giave_moi"] = result.get("chiều_về",{}).get("giá_vé_gốc","")
                    item["somb_moi"] = ""
                    item["giadi_moi"] = result.get("chiều_đi","").get("giá_vé_gốc","")
                    
                   



                datanew.append(item)
            else:
                result_lines.append(res.status_code)
                datanew.append(item)
            print (item)
        except Exception as e:
            
            result_lines.append(f'❌ {item.get("pnr")} -> Lỗi: {e}')
    with open("data.json", "w", encoding="utf-8") as f:
                json.dump(datanew, f, ensure_ascii=False, indent=4)
    with open("log.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(str(item) for item in result_lines))

    return result_lines
def loc_chuyen_bay_theo_gio(list_danh_sach, gio_di_chieu_di, gio_di_chieu_ve=""):
    """
    Lọc chuyến bay theo giờ cất cánh của chiều đi và chiều về
    
    Args:
        list_danh_sach (list): Danh sách các chuyến bay
        gio_di_chieu_di (str): Giờ cất cánh chiều đi (format: "HH:MM")
        gio_di_chieu_ve (str): Giờ cất cánh chiều về (format: "HH:MM")
    
    Returns:
        list: Danh sách các chuyến bay khớp điều kiện
    """
    
    
    for chuyen_bay in list_danh_sach:
        gio_cat_canh_chieu_ve =""
        # Kiểm tra xem chuyến bay có đủ thông tin chiều đi và chiều về không
        if 'chiều_đi' in chuyen_bay :
            # Lấy giờ cất cánh chiều đi và chiều về
            gio_cat_canh_chieu_di = chuyen_bay['chiều_đi'].get('giờ_cất_cánh', '')
            if "chiều_về" in chuyen_bay:
                gio_cat_canh_chieu_ve = chuyen_bay['chiều_về'].get('giờ_cất_cánh', '')
            #print(chuyen_bay)
            # So sánh với điều kiện lọc
            print (gio_di_chieu_di,gio_di_chieu_ve,gio_cat_canh_chieu_di,gio_cat_canh_chieu_ve)
            if (gio_cat_canh_chieu_di == gio_di_chieu_di and 
                gio_cat_canh_chieu_ve == gio_di_chieu_ve):
                
                
                return chuyen_bay
            return None
    
    
def loc_chuyen_bay_theo_ngay(list_danh_sach):
    
    
    
    
    return list_danh_sach[0]
    
    