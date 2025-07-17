from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class CheckPNRWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        self.label = QLabel("Nhập mã giữ chỗ (PNR) để kiểm tra")
        self.label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.input_pnr = QLineEdit()
        self.input_pnr.setPlaceholderText("Ví dụ: ABC123")
        self.input_pnr.setFont(QFont("Segoe UI", 11))
        layout.addWidget(self.input_pnr)

        self.check_btn = QPushButton("Kiểm tra")
        self.check_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.check_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 5px;")
        self.check_btn.clicked.connect(self.handle_check_pnr)
        layout.addWidget(self.check_btn)

        self.result_label = QLabel("")
        self.result_label.setFont(QFont("Segoe UI", 10))
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def handle_check_pnr(self):
        pnr_code = self.input_pnr.text().strip().upper()
        if not pnr_code:
            QMessageBox.warning(self, "Lỗi", "Mã giữ chỗ không được để trống")
            return

        # TODO: Gọi API kiểm tra PNR ở đây
        # response = requests.get(f"https://api.myservice/check_pnr/{pnr_code}")
        # if response.status_code == 200:
        #     data = response.json()
        #     self.result_label.setText(f"Chuyến bay: {data['flight']}\nGiờ bay: {data['time']}")
        # else:
        #     self.result_label.setText("Không tìm thấy mã PNR")

        # Dùng fake data cho test:
        self.result_label.setText(f"✅ Tìm thấy PNR {pnr_code}\nChuyến bay: VJ123\nGiờ bay: 10:00 20/07/2025")
