from PyQt5.QtWidgets import (
    QDialog, QWidget, QFormLayout, QLineEdit, QPushButton,
    QVBoxLayout, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

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
        form_layout.addRow("🔗 URL:", self.input_url)
        form_layout.addRow("🆔 ID:", self.input_id)

        # 🔘 Nút
        self.btn_save = QPushButton("💾 Lưu")
        self.btn_save.setObjectName("saveBtn")
        self.btn_save.clicked.connect(self.accept)

        self.btn_cancel = QPushButton("❌ Hủy")
        self.btn_cancel.setObjectName("cancelBtn")
        self.btn_cancel.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.btn_cancel)
        button_layout.addWidget(self.btn_save)

        # 📦 Layout chính trong widget
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(title_label)
        layout.addSpacing(5)
        layout.addLayout(form_layout)
        layout.addStretch()
        layout.addLayout(button_layout)

    def get_data(self):
        return self.input_url.text().strip(), self.input_id.text().strip()
