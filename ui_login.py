from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QApplication,
    QHBoxLayout, QLabel, QMainWindow
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint
from PyQt5.QtGui import QPainterPath, QRegion
from ui_main import MainApp
import configparser 

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 300)

        self.init_ui()
        self.load_username_from_config()
        self.fade_in()

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
                background-color: #f0f4f8;
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
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)

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
        if user == "1" and pw == "1":
            print("Login thành công")

            # 👉 Mở giao diện chính
            self.main_app = MainApp()
            self.main_app.show()
            

            self.close()  # đóng cửa sổ login
            
        else:
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
