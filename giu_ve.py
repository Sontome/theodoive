from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class GiuVeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Giữ vé máy bay")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        form_layout = QFormLayout()

        self.ma_chuyen_bay_input = QLineEdit()
        self.hanh_khach_input = QLineEdit()
        self.email_input = QLineEdit()

        form_layout.addRow("Mã chuyến bay:", self.ma_chuyen_bay_input)
        form_layout.addRow("Tên hành khách:", self.hanh_khach_input)
        form_layout.addRow("Email liên hệ:", self.email_input)

        layout.addLayout(form_layout)

        self.submit_btn = QPushButton("Giữ vé")
        self.submit_btn.setStyleSheet("padding: 8px; font-weight: bold;")
        self.submit_btn.clicked.connect(self.handle_submit)
        layout.addWidget(self.submit_btn)

        self.result_label = QLabel("")
        self.result_label.setStyleSheet("color: lightgreen;")
        layout.addWidget(self.result_label)

    def handle_submit(self):
        ma_cb = self.ma_chuyen_bay_input.text()
        hanh_khach = self.hanh_khach_input.text()
        email = self.email_input.text()

        # TODO: Gọi API giữ vé tại đây
        self.result_label.setText(f"Đã gửi yêu cầu giữ vé cho {hanh_khach} - chuyến {ma_cb}")
