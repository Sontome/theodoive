from PyQt5.QtWidgets import (
    QDialog, QWidget, QFormLayout, QLineEdit, QPushButton,
    QVBoxLayout, QLabel, QHBoxLayout,QGraphicsOpacityEffect
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt,QPropertyAnimation,QPoint,QEasingCurve

class SettingDialog(QDialog):
    def __init__(self, url='', id_text=''):
        super().__init__()
        self.setWindowTitle("⚙️ Cài đặt cấu hình")
        self.setFixedSize(360, 220)

        # ⚙️ Không viền & nền trong suốt
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # ✅ Widget chính bên trong (bo góc + nền trắng)
        self.main_widget = QWidget(self)
        self.main_widget.setObjectName("mainWidget")
        self.main_widget.setGeometry(0, 0, 360, 220)
        self.main_widget.setStyleSheet("""
            QWidget#mainWidget {
                background-color: #ffffff;
                border-radius: 20px;
                font-family: 'Segoe UI';
                font-size: 13px;
                border: 2px solid #ced4da;                           
            }
            QLineEdit {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 8px;
                font-weight: bold;
            }

            /* ===== SAVE BUTTON ===== */
            QPushButton#saveBtn {
                background-color: #00c853;
                color: white;
            }
            QPushButton#saveBtn:hover {
                background-color: #009624;
            }
            QPushButton#saveBtn:pressed {
                background-color: #007e3a;  /* Màu đậm hơn khi nhấn */
                padding-top: 9px; padding-bottom: 7px; /* Ảo giác nhấn */
            }

            /* ===== CANCEL BUTTON ===== */
            QPushButton#cancelBtn {
                background-color: #e53935;
                color: white;
            }
            QPushButton#cancelBtn:hover {
                background-color: #b71c1c;
            }
            QPushButton#cancelBtn:pressed {
                background-color: #8e0000;
                padding-top: 9px; padding-bottom: 7px;
            }
        """)
        
        
        # 💡 Tiêu đề
        title_label = QLabel("💡 Nhập thông tin cấu hình")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 12, QFont.Bold))

        # 📝 Form
        self.input_url = QLineEdit(url)
        self.input_id = QLineEdit(id_text)
        form_layout = QFormLayout()
        form_layout.addRow(" URL API tele:", self.input_url)
        form_layout.addRow(" ID room tele:", self.input_id)

        # 🔘 Nút
        self.btn_save = QPushButton("Lưu Lại")
        self.btn_save.setObjectName("saveBtn")
        self.btn_save.clicked.connect(self.accept)

        self.btn_cancel = QPushButton("Hủy")
        self.btn_cancel.setObjectName("cancelBtn")
        self.btn_cancel.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_cancel)
        

        # 📦 Layout chính trong widget
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(title_label)
        layout.addSpacing(5)
        layout.addLayout(form_layout)
        layout.addStretch()
        layout.addLayout(button_layout)
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
    def get_data(self):
        return self.input_url.text().strip(), self.input_id.text().strip()
