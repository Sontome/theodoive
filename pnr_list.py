from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QSizePolicy
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from pnr_toolbar import PNRToolbar 
import json
import os,sys
def get_user_data_path(filename):
    """Lưu file cấu hình/data trong cùng thư mục với .exe hoặc file .py"""
    if getattr(sys, 'frozen', False):
        # Nếu chạy từ file .exe (frozen = True)
        return os.path.join(os.path.dirname(sys.executable), filename)
    else:
        # Khi chạy file .py
        return os.path.join(os.path.dirname(__file__), filename)
def resource_path(relative_path):
    """Lấy path chuẩn cho file resource (dùng được cả khi run .py và khi đã build .exe)"""
    try:
        base_path = sys._MEIPASS  # Khi chạy từ .exe
    except AttributeError:
        base_path = os.path.abspath(".")  # Khi chạy từ source .py

    return os.path.join(base_path, relative_path)
class PNRListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.toolbar = PNRToolbar()
        self.toolbar.check_clicked.connect(self.refresh)
        self.layout.addWidget(self.toolbar)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.setup_table()
        self.load_data()

    def setup_table(self):
        self.table.setColumnCount(26)
        self.table.setRowCount(2)

        self.table.setSpan(0, 0, 2, 1)       
        self.table.setSpan(0, 1, 1, 9)      
        self.table.setSpan(0, 10, 1, 4)      
        self.table.setSpan(0, 14, 1, 6)      

        self.table.setItem(0, 0, QTableWidgetItem("PNR"))
        self.table.setItem(0, 1, QTableWidgetItem("Chuyến gốc"))
        self.table.setItem(0, 10, QTableWidgetItem("Chuyến cùng ngày mới rẻ hơn"))
        self.table.setItem(0, 14, QTableWidgetItem("Chuyến gần ngày rẻ hơn"))

        headers_row2 = [
            "Nơi đi", "Nơi về", "Ngày đi", "Ngày về", "Giờ đi", "Giờ về",
            "Hành lý", "Giá tổng", "Hãng",

            "Giá mới tổng", "Giờ đi", "Giờ về", "Hành lý",

            "Giá mới tổng", "Ngày đi", "Ngày về", "Giờ đi", "Giờ về",
            "Số máy bay"
        ]
        for i, text in enumerate(headers_row2, start=1):
            self.table.setItem(1, i, QTableWidgetItem(text))

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setWordWrap(True)
        self.table.setHorizontalScrollMode(self.table.ScrollPerPixel)
        self.table.setVerticalScrollMode(self.table.ScrollPerPixel)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.table.setRowHeight(0, 30)
        self.table.setRowHeight(1, 30)

    def load_data(self):
        # Xoá dòng cũ trước khi load lại
        while self.table.rowCount() > 2:
            self.table.removeRow(2)

        
        if not os.path.exists(get_user_data_path("data.json")):
            print("File data.json không tồn tại!")
            return
        
        try:
            with open(get_user_data_path("data.json"), 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print("Lỗi khi đọc file JSON:", e)
            return

        for item in data:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # Map field theo đúng thứ tự cột
            columns = [
                item.get("pnr", ""),
                item.get("noidi", ""),
                item.get("noiden", ""),
                item.get("ngaydi", ""),
                item.get("ngayve", ""),
                item.get("giodi", ""),
                item.get("giove", ""),
                item.get("hanh_ly", ""),
                item.get("giatong", ""),
                
                item.get("hang", ""),

                item.get("giacu_cunggio_moitong", ""),
                item.get("giodi_moi", ""),
                item.get("giove_moi", ""),
                item.get("hanh_ly_moi", ""),
                

                item.get("giacu_ngaygan_moitong", ""),
                item.get("ngaydi_moi", ""),
                item.get("ngayve_moi", ""),
                item.get("giodi_ngaygan", ""),
                item.get("giove_ngaygan", ""),
                item.get("somb_ngaygan", "")
               
            ]

            for col, val in enumerate(columns):
                cell = QTableWidgetItem(str(val))

                # 👉 Check màu cho cột "giacu_cunggio_moitong" (col index 12) so với "giatong" (col index 8)
                if col == 10:
                    try:
                        giacu = item.get("giatong", 0)
                        
                        giatong = item.get("giacu_cunggio_moitong", 10000000)
                        if giatong == 0 :
                            giatong = 10000000
                        #print (giacu,giatong)
                        if int(giacu) > int(giatong):
                            cell.setBackground(QColor(0, 255, 0, 100))  # xanh lá nhạt
                        elif int(giacu) == int(giatong):
                            cell.setBackground(QColor(200, 200, 200, 100))  # xám nhạt
                        else:
                            cell.setBackground(QColor(255, 0, 0, 100))  # đỏ nhạt
                    except Exception as e:
                        print("Lỗi so sánh giá:", e)
                if col == 0:
                    hang = item.get("hang", "").upper()
                    if hang == "VJ":
                        cell.setBackground(QColor(216, 19, 39, 150))  # đỏ nhạt
                    elif hang == "VNA":
                        cell.setBackground(QColor(65, 139, 179, 150))  # xanh dương nhạt
                self.table.setItem(row, col, cell)
                if col == 11 :
                    giacu = item.get("giatong", 0)
                    giodi =   item.get("giodi", "")
                    giove = item.get("giove", "")
                    giodimoi =   item.get("giodi_moi", "")
                    giovemoi = item.get("giove_moi", "")
                    giatong = item.get("giacu_cunggio_moitong", 10000000)
                    if giatong == 0 :
                        giatong = 10000000
                    if int(giacu) > int(giatong):
                        if giodi == giodimoi:
                            cell.setBackground(QColor(0, 255, 0, 100)) 
                        else :
                            cell.setBackground(QColor(255, 0, 0, 100))
                    else:
                        cell.setBackground(QColor(200, 200, 200, 100))  # xám nhạt
                if col == 12 :
                    giacu = item.get("giatong", 0)
                    giodi =   item.get("giodi", "")
                    giove = item.get("giove", "")
                    giodimoi =   item.get("giodi_moi", "")
                    giovemoi = item.get("giove_moi", "")
                    giatong = item.get("giacu_cunggio_moitong", 10000000)
                    if giatong == 0 :
                        giatong = 10000000
                    if int(giacu) > int(giatong):
                        if giove == giovemoi:
                            cell.setBackground(QColor(0, 255, 0, 100)) 
                        else :
                            cell.setBackground(QColor(255, 0, 0, 100))
                    else:
                        cell.setBackground(QColor(200, 200, 200, 100))  # xám nhạt


    def refresh(self):
        self.load_data()
