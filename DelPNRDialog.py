from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox,
    QPushButton, QHBoxLayout, QMessageBox,QWidget  , QGraphicsOpacityEffect,QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QPropertyAnimation,QPoint,QEasingCurve
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
class DelPNRDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set giao diện màu sáng
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 8px;
                background: white;
                           
                color: black;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: #f44336;
                selection-color: white;
                border: 1px solid #ccc;
                outline: none;
            }
            QPushButton {
                background-color: #00c853;
                color: white;
                padding: 6px 12px;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #009624;
            }
            QPushButton:pressed {
                background-color: #007e3a;  /* Màu đậm hơn khi nhấn */
                padding-top: 9px; padding-bottom: 7px; /* Ảo giác nhấn */
            }   
            QPushButton#Huy {
                background-color: #e53935;
                color: white;
            }
            QPushButton#Huy:hover {
                background-color: #b71c1c;
            }
            QPushButton#Huy:pressed {
                background-color: #8e0000;
                padding-top: 9px; padding-bottom: 7px;
            }                           
        """)

        
        # Ẩn khung cửa sổ mặc định
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedSize(320, 160)

        container = QWidget(self)
        container.setObjectName("container")
        container.setStyleSheet("""
            QWidget#container {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f0f4f8, stop:1 #dbeafe);
                border-radius: 15px;
                border: 2px solid #ced4da;                
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(15, 15, 15, 15)

        self.combo = QComboBox()
        self.data = self.load_data()
        #print("DATA ĐÃ LOAD:", self.data)
        if not self.data:
            QMessageBox.information(self, "Thông báo", "Không có PNR nào để xóa.")
            self.reject()
            return

        self.combo.addItems([item["pnr"] for item in self.data])
        layout.addWidget(QLabel("Chọn mã PNR cần xóa:"))
        layout.addWidget(self.combo)

        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("Xóa")
        self.btn_ok.setObjectName("Xoa")
        self.btn_cancel = QPushButton("Hủy")
        self.btn_cancel.setObjectName("Huy")
        

        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.btn_ok.clicked.connect(self.on_ok_clicked)
        self.btn_cancel.clicked.connect(self.reject)

        self.fade_in_animation()
        self.slide_in_animation()
    def slide_in_animation(self):
        screen_geometry = self.screen().availableGeometry()
        screen_center = screen_geometry.center()

        # Điểm bắt đầu: ở dưới màn hình
        start_pos = QPoint(screen_center.x() - self.width() // 2, screen_geometry.bottom())
        # Điểm kết thúc: ở giữa màn hình
        end_pos = QPoint(screen_center.x() - self.width() // 2, screen_center.y() - self.height() // 2)

        self.move(start_pos)

        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(600)
        self.anim.setStartValue(start_pos)
        self.anim.setEndValue(end_pos)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.start()
    def fade_in_animation(self):
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        self.fade_anim = QPropertyAnimation(self.effect, b"opacity")
        self.fade_anim.setDuration(300)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.finished.connect(self.clear_opacity_effect)
        self.fade_anim.start()

    def clear_opacity_effect(self):
        self.setGraphicsEffect(None)
    def on_ok_clicked(self):
        if not self.combo.currentText():
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn mã PNR cần xóa.")
            return
        self.accept()
   
    def load_data(self):
        if not os.path.exists(get_user_data_path("data.json")):
            return []
        

        with open(get_user_data_path("data.json"), "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def get_deleted_data(self):
        pnr = self.combo.currentText()
        new_data = [item for item in self.data if item["pnr"] != pnr]
        return pnr, new_data
