import os,sys
import configparser
import json
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLineEdit, QLabel,QDialog, QCheckBox, QVBoxLayout,QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal,QThread,QUrl
from setting import SettingDialog
from AddPNRDialog import AddPNRDialog
from DelPNRDialog import DelPNRDialog
from PyQt5.QtMultimedia import QSoundEffect
from check import check_all_pnrs
from pushnoti import PushNotiTelegram
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
class CheckPNRThread(QThread):
    finished = pyqtSignal(str)  # Trả kết quả dạng string

    def run(self):
        from check import check_all_pnrs
        check_all_pnrs()  # chạy hàm chính
        self.finished.emit("✅ Check xong rồi đại ca!")
        
class PNRToolbar(QWidget):
    check_clicked = pyqtSignal()
    
    def handle_delete_clicked(self):
        
        self.btn_sound.play()
        dialog = DelPNRDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            pnr, new_data = dialog.get_deleted_data()

            with open(get_user_data_path("data.json"), "w", encoding="utf-8") as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)

            
        else:
            print("Đại ca hủy xóa rồi 😅")
    def handle_add_clicked(self):
        self.btn_sound.play()

        dialog = AddPNRDialog(self)
        if dialog.exec_() == dialog.Accepted:
            new_data = dialog.get_data()
            

            # Đọc file data.json nếu có, không thì tạo mới
            if os.path.exists(get_user_data_path("data.json")):
                with open(get_user_data_path("data.json"), "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = []
            else:
                data = []

            # Append dữ liệu mới
            data.append(new_data)

            # Ghi lại file
            with open(get_user_data_path("data.json"), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print("Đã lưu thành công vl 🛫")
        else:
            print("Đại ca cancel rồi, không lưu gì hết nha 🛑")
    def open_settings_dialog(self):
        self.btn_sound.play()
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

            with open(get_user_data_path("config.ini"), 'w') as configfile:
                self.config.write(configfile)
    def check_ve_clicked(self):
        self.btn_sound.play()
        self.btn_check.setEnabled(False)
        self.btn_check.setText("⏳ Đang check...")

        self.thread = CheckPNRThread()
        self.thread.finished.connect(self.check_done)
        self.thread.start()

    def check_done(self, message):
        self.btn_check.setEnabled(True)
        self.btn_check.setText("✅ Check")

        # Cập nhật thời gian sau khi check xong
        self.update_last_update_time()

        

        # Nếu đang auto-check thì khởi động lại timer
        if self.toggle_autocheck.isChecked():
            self.restart_timer()
        self.click_sound.play()
        self.check_clicked.emit()
        url = self.config.get('API', 'url', fallback='')
        id_text = self.config.get('API', 'id', fallback='')
        if url and id_text:
            PushNotiTelegram(url, id_text).push_from_data()
    def update_last_update_time(self):
        """Cập nhật thời gian hiện tại vào config và hiển thị"""
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M")
        
        if not self.config.has_section('UPDATETIME'):
            self.config.add_section('UPDATETIME')
        
        self.config.set('UPDATETIME', 'time', current_time)
        
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)
        
        # Cập nhật label hiển thị
        self.label_last_update.setText(f"🕐 Cập nhật lần cuối: {current_time}")
    
    def load_last_update_time(self):
        """Đọc thời gian cập nhật gần nhất từ config"""
        last_time = self.config.get('UPDATETIME', 'time', fallback='--:--')
        self.label_last_update.setText(f"🕐 Cập nhật lần cuối: {last_time}")

    def __init__(self):
        super().__init__()
        self.config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        self.config = configparser.ConfigParser()
        self.click_sound = QSoundEffect()
        self.click_sound.setSource(QUrl.fromLocalFile("ding.wav"))
        self.click_sound.setVolume(1)
        self.btn_sound = QSoundEffect()
        self.btn_sound.setSource(QUrl.fromLocalFile("clicknut.wav"))
        self.btn_sound.setVolume(1)
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
        self.btn_delete.clicked.connect(self.handle_delete_clicked)    
        self.btn_settings.clicked.connect(self.open_settings_dialog)
        self.btn_add.clicked.connect(self.handle_add_clicked)
        self.btn_add.clicked.connect(self.check_clicked.emit)
        self.btn_delete.clicked.connect(self.check_clicked.emit)
        self.btn_check.clicked.connect(self.check_ve_clicked)
        
        
        # Hàng hiển thị thời gian cập nhật gần nhất
        update_time_layout = QHBoxLayout()
        self.label_last_update = QLabel("🕐 Cập nhật lần cuối: --:--")
        self.label_last_update.setStyleSheet("font-weight: bold; color: #1976d2;")
        update_time_layout.addWidget(self.label_last_update)
        update_time_layout.addStretch()
        
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
        main_layout.addLayout(update_time_layout)  # Thêm layout hiển thị thời gian
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
            # Khi timer hết, tự động check và cập nhật thời gian
            self.check_ve_clicked()
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
            # Tạo section UPDATETIME mặc định
            self.config['UPDATETIME'] = {
                'time': '--:--'
            }
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)

        auto_config = self.config['AutoCheck']
        enabled = auto_config.getboolean('enabled', fallback=False)
        minutes = auto_config.getint('minutes', fallback=5)

        self.toggle_autocheck.setChecked(enabled)
        self.input_minutes.setText(str(minutes))

        # Load thời gian cập nhật gần nhất
        self.load_last_update_time()

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