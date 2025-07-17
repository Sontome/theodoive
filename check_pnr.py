import requests
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
)
from PyQt5.QtCore import Qt


class CheckPNRWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        self.label = QLabel("Nhập mã PNR để kiểm tra:")
        self.label.setStyleSheet("font-weight: bold; font-size: 14px; color: #111827;")

        self.input_pnr = QLineEdit()
        self.input_pnr.setPlaceholderText("Ví dụ: ABC123")
        self.input_pnr.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
        """)

        self.btn_check = QPushButton("Kiểm tra")
        self.btn_check.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.btn_check.clicked.connect(self.check_pnr)  # 👈 Gắn hàm xử lý

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setStyleSheet("""
            QTextEdit {
                background-color: #f9fafb;
                color: #111827;
                border: 1px solid #d1d5db;
                padding: 10px;
                border-radius: 6px;
                font-size: 13px;
            }
        """)

        layout.addWidget(self.label)
        layout.addWidget(self.input_pnr)
        layout.addWidget(self.btn_check)
        layout.addWidget(self.result, stretch=1)

        self.setLayout(layout)

    def check_pnr(self):
        pnr_code = self.input_pnr.text().strip().upper()
        if not pnr_code:
            self.result.setText("❌ Vui lòng nhập mã PNR.")
            return

        url = f"https://thuhongtour.com/vj/checkpnr?pnr={pnr_code}"
        try:
            response = requests.post(url, headers={"accept": "application/json"}, data="")
            if response.status_code == 200:
                data = response.json()
                formatted = json.dumps(data, indent=2, ensure_ascii=False)
                self.result.setText(formatted)
            else:
                self.result.setText(f"⚠️ Lỗi {response.status_code}: Không thể kiểm tra vé.")
        except Exception as e:
            self.result.setText(f"❌ Gặp lỗi: {str(e)}")
