from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QApplication,
    QHBoxLayout, QLabel, QMainWindow,QMessageBox
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint,QUrl
from PyQt5.QtGui import QPainterPath, QRegion
from ui_main import MainApp
import configparser 
from datetime import datetime
import os,sys
from PyQt5.QtMultimedia import QSoundEffect
from supabase_helper import create_account, check_login




def get_user_data_path(filename):
        """Lấy đường dẫn file khi chạy dạng .py hoặc đã build .exe"""
        if getattr(sys, 'frozen', False):
            return os.path.join(os.path.dirname(sys.executable), filename)
        else:
            return os.path.join(os.path.dirname(__file__), filename)

class LoginApp(QWidget):
    
    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập đầy đủ tài khoản và mật khẩu.")
            return

        success, message = create_account(username, password)
        if success:
            QMessageBox.information(self, "Thành công", message)
        else:
            QMessageBox.critical(self, "Thất bại", message)

    def check_and_clear_data_if_expired(self):
        config_path = get_user_data_path("config.ini")
        data_path = get_user_data_path("data.json")
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        config = configparser.ConfigParser()

        # 🔧 Nếu chưa có config.ini thì tạo mặc định
        if not os.path.exists(config_path):
            config["AutoCheck"] = {"enabled": "true", "minutes": "5"}
            config["API"] = {"url": "7359295123:AAGz0rHge3L5gM-XJmyzNq6sayULdHO4-qE", "id": ""}
            config["LOGIN"] = {"username": "1"}
            config["UPDATETIME"] = {"time": "13:52"}
            config["DATA"] = {"daydate": today_str}  # Set today là mặc định

            with open(config_path, "w", encoding="utf-8") as f:
                config.write(f)
            print("⚙️ Đã tạo file config.ini mặc định")
            return

        # ✅ Đọc config hiện có
        config.read(config_path)

        try:
            if "DATA" not in config:
                config["DATA"] = {}

            daydate_str = config["DATA"].get("daydate", today_str)  # Nếu không có thì set today
            daydate = datetime.strptime(daydate_str, "%Y-%m-%d").date()
            today = datetime.now().date()

            if daydate < today:
                # 🧨 Xoá file data.json nếu có
                if os.path.exists(data_path):
                    os.remove(data_path)
                    print("💥 Đã xoá file data.json vì quá hạn")

                # ✍️ Cập nhật lại ngày mới vào config.ini
                config["DATA"]["daydate"] = today_str
                with open(config_path, "w", encoding="utf-8") as f:
                    config.write(f)
                print("🔄 Đã cập nhật daydate mới vào config.ini")

        except Exception as e:
            print("❌ Lỗi xử lý config/data:", e)
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 300)
        self.click_sound = QSoundEffect()
        self.click_sound.setSource(QUrl.fromLocalFile("clicknut.wav"))
        self.click_sound.setVolume(0.5)
        self.init_ui()
        self.load_username_from_config()
        self.fade_in()
        self.check_and_clear_data_if_expired()

        self._drag_pos = None  # để kéo cửa sổ
    def load_username_from_config(self):
        try:
            config = configparser.ConfigParser()
            config.read("config.ini")
            if "LOGIN" in config and "username" in config["LOGIN"]:
                self.username_input.setText(config["LOGIN"]["username"])
        except Exception as e:
            print("Không đọc được username từ config.ini:", e)    
    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.content = QWidget()
        self.content.setStyleSheet("""
            
            border-radius: 15px; 
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f0f4f8, stop:1 #dbeafe);
        """)
        self.main_layout.addWidget(self.content)

        layout = QVBoxLayout(self.content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        top_bar = QHBoxLayout()
        top_bar.addStretch()
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: black;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #d1d5db;
                border-radius: 5px;
                color: black;  
                font-weight: bold;              
            }
            QPushButton:pressed {
                background-color: #f9f4f8;
                border-radius: 5px;
                color: black;  
                font-weight: bold;              
            }
        """)
        close_btn.clicked.connect(self.close)
        top_bar.addWidget(close_btn)
        layout.addLayout(top_bar)
        title_label = QLabel("Tool Check Giá")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #1e293b;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Tên đăng nhập")
        self.username_input.setStyleSheet(self.input_style())
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.input_style())
        layout.addWidget(self.password_input)

        login_btn = QPushButton("Đăng nhập")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #5865F2;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4752C4;
            }
            QPushButton:pressed {
                background-color: #5865F2;
            }                    
        """)
        register_btn = QPushButton("Tạo tài khoản")
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:pressed {
                background-color: #10b981;
            }                    
        """)
        register_btn.clicked.connect(self.handle_register)
        
        def handle_click():
            self.click_sound.play()  # Phát âm thanh
            self.login()
        login_btn.clicked.connect(handle_click)
        layout.addWidget(login_btn)
        layout.addWidget(register_btn)

    def input_style(self):
        return """
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #202225;
                border-radius: 5px;
                padding: 8px;
                color: black;
            }
            QLineEdit:focus {
                border: 1px solid #7289da;
            }
        """

    def fade_in(self):
        self.setWindowOpacity(0)
        self.show()
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(400)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()

    def login(self):
        user = self.username_input.text()
        pw = self.password_input.text()
        
        if check_login(user, pw):
            print("✅ Đăng nhập thành công")
            self.main_app = MainApp()
            self.main_app.show()
            self.close()
        else:
            print("❌ Sai tài khoản hoặc mật khẩu")
            self.shake()

    def shake(self):
        animation = QPropertyAnimation(self, b"pos")
        animation.setDuration(300)
        animation.setKeyValueAt(0, self.pos())
        animation.setKeyValueAt(0.25, self.pos() + QPoint(-10, 0))
        animation.setKeyValueAt(0.5, self.pos() + QPoint(10, 0))
        animation.setKeyValueAt(0.75, self.pos() + QPoint(-10, 0))
        animation.setKeyValueAt(1, self.pos())
        animation.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
