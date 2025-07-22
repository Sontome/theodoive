from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QLabel,QGraphicsOpacityEffect,
    QPushButton, QHBoxLayout,QComboBox  ,QDateEdit,QCalendarWidget,QWidget
)
from PyQt5.QtCore import Qt,QPropertyAnimation,QPoint,QEasingCurve,QDate
class CalendarLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Chọn ngày")

        # Tạo lịch nhưng ẩn
        self.calendar = QCalendarWidget()
        self.calendar.setWindowFlags(Qt.Popup)  # Cho popup như kiểu dropdown
        self.calendar.clicked.connect(self.set_date_from_calendar)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        # Tính vị trí popup dưới lineedit
        pos = self.mapToGlobal(QPoint(0, self.height()))
        self.calendar.move(pos)
        self.calendar.show()

    def set_date_from_calendar(self, date: QDate):
        self.setText(date.toString("dd/MM/yyyy"))
        self.calendar.hide()
class AddPNRDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)  # ← bỏ viền cửa sổ mặc định
        self.setFixedSize(400, 420)

        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        airport_codes = ["ICN", "PUS", "HAN", "SGN", "DAD", "CXR", "VCL", "PQC"]
        airlines = ["VJ", "VNA"]
        # Tạo input fields
        self.input_pnr = QLineEdit()
        self.input_noidi = QComboBox()
        self.input_noidi.addItems(airport_codes)
        self.input_noiden = QComboBox()
        self.input_noiden.addItems(airport_codes)
        self.input_noiden.setCurrentText("HAN")
        self.input_ngaydi = CalendarLineEdit()
        
        self.input_giodi = QLineEdit()
        self.input_ngayve = CalendarLineEdit()
        self.input_giove = QLineEdit()
        self.input_somb = QLineEdit()
        self.input_giatong = QLineEdit()
        self.input_giadi = QLineEdit()
        self.input_giave = QLineEdit()
        self.input_hang = QComboBox()
        self.input_hang.addItems(airlines)

        # Add fields vào layout
        form_layout.addRow("Mã PNR:", self.input_pnr)
        form_layout.addRow("Nơi đi:", self.input_noidi)
        form_layout.addRow("Nơi đến:", self.input_noiden)
        form_layout.addRow("Ngày đi:", self.input_ngaydi)
        form_layout.addRow("Giờ đi:", self.input_giodi)
        form_layout.addRow("Ngày về (tuỳ chọn):", self.input_ngayve)
        form_layout.addRow("Giờ về:", self.input_giove)
        form_layout.addRow("Số hiệu bay:", self.input_somb)
        form_layout.addRow("Giá tổng:", self.input_giatong)
        form_layout.addRow("Giá đi:", self.input_giadi)
        form_layout.addRow("Giá về:", self.input_giave)
        form_layout.addRow("Hãng:", self.input_hang)
        

        # Buttons
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("Lưu")
        self.btn_cancel = QPushButton("Hủy")
        self.btn_cancel.setObjectName("Huy")
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(self.btn_cancel)

        # Gộp lại
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)

        btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f0f4f8, stop:1 #dbeafe);
                color: #212529;
                border: 2px solid #ced4da;
                border-radius: 12px;
            }

            QLabel {
                font-size: 14px;
                font-weight: bold;
            }

            QLineEdit {
                font-size: 12px;
                padding: 5px;
                border: 1px solid #ced4da;
                border-radius: 5px;
                background-color: #ffffff;
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
            QComboBox {
                font-size: 12px;
                padding: 5px;
                border: 1px solid #ced4da;
                border-radius: 5px;
                background-color: #ffffff;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                selection-background-color: #dbeafe;
                color: #000000;
                border-radius: 5px
            } 
            QDateEdit {
                font-size: 12px;
                padding: 5px;
                border: 1px solid #ced4da;
                border-radius: 5px;
                background-color: #ffffff;
            }
            QCalendarWidget QToolButton {
                height: 24px;
                width: 80px;
                color: #ffffff;
                font-weight: bold;
                background-color: transparent;
            }
            QCalendarWidget QMenu {
                background-color: #ffffff;
            }
            QCalendarWidget QSpinBox {
                width: 40px;
            }
            QCalendarWidget QWidget {
                alternate-background-color: #ffffff;
            }
            QCalendarWidget QAbstractItemView:enabled {
                font-size: 10px;
                color: black;
                background-color: #ffffff;
                selection-background-color: #ffffff;
                selection-color: ffffff;
            }                             
        """)
        self.fade_in_animation()
        self.slide_in_animation()

    def get_data(self):
        def safe_int(text):
            try:
                return int(text.replace(",", "").strip())
            except:
                return 0
        text_ngaydi = self.input_ngaydi.text().strip()
        ngaydi = QDate.fromString(text_ngaydi, "dd/MM/yyyy") if text_ngaydi else None
        text_ngayve = self.input_ngayve.text().strip()
        ngayve = QDate.fromString(text_ngayve, "dd/MM/yyyy") if text_ngayve else None
        return {
            "pnr": self.input_pnr.text().strip(),
            "noidi": self.input_noidi.currentText().strip(),
            "noiden": self.input_noiden.currentText().strip(),
            "ngaydi": ngaydi.toString("dd/MM/yyyy") if ngaydi and ngaydi.isValid() else None,
            "ngayve": ngayve.toString("dd/MM/yyyy") if ngayve and ngayve.isValid() else "",
            "giodi": self.input_giodi.text().strip(),
            "giove": self.input_giove.text().strip(),
            "somb": self.input_somb.text().strip(),
            "giatong": safe_int(self.input_giatong.text().strip()),
            "giadi": safe_int(self.input_giadi.text().strip()),
            "giave": safe_int(self.input_giave.text().strip()),
            "hang": self.input_hang.currentText().strip(),
            "giacu_cunggio_moitong": 0,
            
            "giadi_moi": 0,
            "giave_moi": 0
        }
    def clear_opacity_effect(self):
        self.setGraphicsEffect(None)
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
