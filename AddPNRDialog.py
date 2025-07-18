from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QLabel,
    QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt

class AddPNRDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)  # ← bỏ viền cửa sổ mặc định
        self.setFixedSize(400, 420)

        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Tạo input fields
        self.input_pnr = QLineEdit()
        self.input_noidi = QLineEdit()
        self.input_noiden = QLineEdit()
        self.input_ngaydi = QLineEdit()
        self.input_giodi = QLineEdit()
        self.input_ngayve = QLineEdit()
        self.input_giove = QLineEdit()
        self.input_somb = QLineEdit()
        self.input_giatong = QLineEdit()
        self.input_giadi = QLineEdit()
        self.input_giave = QLineEdit()
        self.input_hang = QLineEdit()

        # Add fields vào layout
        form_layout.addRow("Mã PNR:", self.input_pnr)
        form_layout.addRow("Nơi đi:", self.input_noidi)
        form_layout.addRow("Nơi đến:", self.input_noiden)
        form_layout.addRow("Ngày đi:", self.input_ngaydi)
        form_layout.addRow("Giờ đi:", self.input_giodi)
        form_layout.addRow("Ngày về:", self.input_ngayve)
        form_layout.addRow("Giờ về:", self.input_giove)
        form_layout.addRow("Số hiệu bay:", self.input_somb)
        form_layout.addRow("Giá tổng:", self.input_giatong)
        form_layout.addRow("Giá đi:", self.input_giadi)
        form_layout.addRow("Giá về:", self.input_giave)
        form_layout.addRow("Hãng:", self.input_hang)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("💾 Lưu")
        btn_cancel = QPushButton("❌ Hủy")
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)

        # Gộp lại
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)

        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                color: #212529;
                border: 2px solid #ced4da;
                border-radius: 12px;
            }

            QLabel {
                font-size: 14px;
                font-weight: bold;
            }

            QLineEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ced4da;
                border-radius: 5px;
                background-color: #ffffff;
            }

            QPushButton {
                font-size: 14px;
                padding: 6px 12px;
                background-color: #6c757d;
                color: white;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #5a6268;
            }
        """)

    def get_data(self):
        return {
            "pnr": self.input_pnr.text().strip(),
            "noidi": self.input_noidi.text().strip(),
            "noiden": self.input_noiden.text().strip(),
            "ngaydi": self.input_ngaydi.text().strip(),
            "ngayve": self.input_ngayve.text().strip(),
            "giodi": self.input_giodi.text().strip(),
            "giove": self.input_giove.text().strip(),
            "somb": self.input_somb.text().strip(),
            "giatong": self.input_giatong.text().strip(),
            "giadi": self.input_giadi.text().strip(),
            "giave": self.input_giave.text().strip(),
            "hang": self.input_hang.text().strip()
        }
