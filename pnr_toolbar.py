import os
import configparser
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLineEdit, QLabel, QCheckBox, QVBoxLayout
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from setting import SettingDialog
class PNRToolbar(QWidget):
    check_clicked = pyqtSignal()
    def open_settings_dialog(self):
        # Load config URL và ID nếu có
        url = self.config.get('API', 'url', fallback='')
        id_text = self.config.get('API', 'id', fallback='')

        dialog = SettingDialog(url, id_text)
        if dialog.exec_():  # OK
            new_url, new_id = dialog.get_data()
            if not self.config.has_section('API'):
                self.config.add_section('API')
            self.config.set('API', 'url', new_url)
            self.config.set('API', 'id', new_id)

            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)
    def __init__(self):
        super().__init__()
        self.config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        self.config = configparser.ConfigParser()

        # Layout chính
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        btn_style = """
            QPushButton {
                
                font-weight: bold;
                
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d6d6d6;
            }
        """
        # Hàng nút chức năng
        button_layout = QHBoxLayout()
        self.btn_add = QPushButton("➕ Thêm")
        self.btn_delete = QPushButton("❌ Xóa")
        self.btn_check = QPushButton("✅ Check")
        self.btn_settings = QPushButton("⚙️ Cài đặt")
        self.btn_settings.setStyleSheet(btn_style)
        self.btn_check.setStyleSheet(btn_style)
        self.btn_delete.setStyleSheet(btn_style)
        self.btn_add.setStyleSheet(btn_style)
        for btn in [self.btn_add, self.btn_delete, self.btn_check, self.btn_settings]:
            btn.setFixedHeight(36)
            button_layout.addWidget(btn)
        self.btn_settings.clicked.connect(self.open_settings_dialog)
        # Hàng AutoCheck
        auto_layout = QHBoxLayout()
        self.toggle_autocheck = QCheckBox("AutoCheck")
        self.toggle_autocheck.setStyleSheet("""
            QCheckBox::indicator {
                width: 40px;
                height: 20px;
            }
            QCheckBox::indicator:unchecked {
                background-color: lightgray;
                border-radius: 10px;
            }
            QCheckBox::indicator:checked {
                background-color: #00c853;
                border-radius: 10px;
            }
        """)
        self.input_minutes = QLineEdit()
        self.input_minutes.setPlaceholderText("Phút")
        self.input_minutes.setFixedWidth(50)
        self.input_minutes.setAlignment(Qt.AlignCenter)
        self.label_countdown = QLabel("⏳ --:--")
        self.label_countdown.setStyleSheet("font-weight: bold; color: #d32f2f;")

        self.btn_check.clicked.connect(self.check_clicked.emit)

        auto_layout.addWidget(self.toggle_autocheck)
        auto_layout.addWidget(QLabel("Mỗi"))
        auto_layout.addWidget(self.input_minutes)
        auto_layout.addWidget(QLabel("phút"))
        auto_layout.addWidget(self.label_countdown)
        auto_layout.addStretch()

        main_layout.addLayout(button_layout)
        main_layout.addLayout(auto_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.remaining_seconds = 0

        # Load config từ file
        self.load_config()

        # Connect sau khi load xong
        self.toggle_autocheck.stateChanged.connect(self.handle_autocheck_toggle)
        self.input_minutes.textChanged.connect(self.save_config)

    def handle_autocheck_toggle(self, state):
        self.save_config()  # Lưu config ngay khi toggle
        if state == Qt.Checked:
            try:
                minutes = int(self.input_minutes.text())
                self.remaining_seconds = minutes * 60
                self.timer.start(1000)
                self.update_countdown()
            except ValueError:
                self.remaining_seconds = 0
                self.label_countdown.setText("⏳ Lỗi!")
        else:
            self.timer.stop()
            self.label_countdown.setText("⏳ --:--")

    def update_countdown(self):
        if self.remaining_seconds > 0:
            minutes = self.remaining_seconds // 60
            seconds = self.remaining_seconds % 60
            self.label_countdown.setText(f"⏳ {minutes:02}:{seconds:02}")
            self.remaining_seconds -= 1
        else:
            self.timer.stop()
            self.label_countdown.setText("⏳ Đang xử lý...")
            self.restart_timer()

    def restart_timer(self):
        try:
            minutes = int(self.input_minutes.text())
            self.remaining_seconds = minutes * 60
            self.timer.start(1000)
        except ValueError:
            self.label_countdown.setText("⏳ Lỗi!")

    def load_config(self):
        if os.path.exists(self.config_path):
            self.config.read(self.config_path)
        else:
            self.config['AutoCheck'] = {
                'enabled': 'false',
                'minutes': '5'
            }
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)

        auto_config = self.config['AutoCheck']
        enabled = auto_config.getboolean('enabled', fallback=False)
        minutes = auto_config.getint('minutes', fallback=5)

        self.toggle_autocheck.setChecked(enabled)
        self.input_minutes.setText(str(minutes))

        # Nếu enable thì khởi động lại
        if enabled:
            self.remaining_seconds = minutes * 60
            self.timer.start(1000)
            self.update_countdown()

    def save_config(self):
        self.config['AutoCheck'] = {
            'enabled': str(self.toggle_autocheck.isChecked()).lower(),
            'minutes': self.input_minutes.text() or "5"
        }
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)
