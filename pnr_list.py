from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QHBoxLayout, QLineEdit, QMessageBox
)
from PyQt5.QtCore import QTimer, Qt


class PNRListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.data = []
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # Tiêu đề
        self.title = QLabel("Danh sách PNR")
        self.title.setStyleSheet("color: #222; font-size: 20px; font-weight: bold;")
        main_layout.addWidget(self.title)

        # Khu vực nút
        button_layout = QHBoxLayout()

        self.add_btn = QPushButton("Thêm")
        self.remove_btn = QPushButton("Xoá")
        self.check_btn = QPushButton("Check")
        self.autocheck_btn = QPushButton("AutoCheck")
        self.minutes_input = QLineEdit()
        self.minutes_input.setPlaceholderText("Phút...")
        self.minutes_input.setFixedWidth(80)

        for btn in [self.add_btn, self.remove_btn, self.check_btn, self.autocheck_btn]:
            btn.setStyleSheet("padding: 6px 12px; font-weight: bold;")

        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.remove_btn)
        button_layout.addWidget(self.check_btn)
        button_layout.addWidget(self.autocheck_btn)
        button_layout.addWidget(self.minutes_input)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        # Bảng PNR
        self.table = QTableWidget()
        self.table.setColumnCount(13)
        self.table.setHorizontalHeaderLabels([
            "PNR", "Nơi đi", "Nơi đến", "Ngày đi", "Ngày về", "Giờ đi", "Giờ về",
            "Giá gốc tổng", "Giá gốc đi", "Giá gốc về",
            "Giá mới tổng", "Giá mới đi", "Giá mới về"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("font-size: 13px; color: #111;")
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        # Sự kiện
        self.add_btn.clicked.connect(self.add_row)
        self.remove_btn.clicked.connect(self.remove_selected)
        self.autocheck_btn.clicked.connect(self.setup_auto_check)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.mock_price_update)

        self.mock_data()

    def add_row(self):
        row_pos = self.table.rowCount()
        self.table.insertRow(row_pos)
        for col in range(13):
            self.table.setItem(row_pos, col, QTableWidgetItem(""))

    def remove_selected(self):
        selected = self.table.currentRow()
        if selected >= 0:
            self.table.removeRow(selected)

    def setup_auto_check(self):
        try:
            mins = int(self.minutes_input.text())
            if mins <= 0:
                raise ValueError
            self.timer.start(mins * 60 * 1000)
            QMessageBox.information(self, "AutoCheck", f"Đã bật auto check mỗi {mins} phút.")
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Số phút không hợp lệ")

    def mock_price_update(self):
        row_count = self.table.rowCount()
        for row in range(row_count):
            try:
                old_total = int(self.table.item(row, 7).text().replace(",", "").replace(" đ", ""))
                old_di = int(self.table.item(row, 8).text().replace(",", "").replace(" đ", ""))
                old_ve = int(self.table.item(row, 9).text().replace(",", "").replace(" đ", ""))

                new_di = max(500000, old_di - 50000)
                new_ve = max(500000, old_ve - 70000)
                new_total = new_di + new_ve

                self.table.setItem(row, 10, QTableWidgetItem(f"{new_total:,} đ"))
                self.table.setItem(row, 11, QTableWidgetItem(f"{new_di:,} đ"))
                self.table.setItem(row, 12, QTableWidgetItem(f"{new_ve:,} đ"))
            except:
                continue

    def mock_data(self):
        # Dữ liệu mẫu
        mock_rows = [
            ["A21GAF", "HAN", "SGN", "20/08/2025", "22/08/2025", "10:00", "13:00", "2,500,000 đ", "1,200,000 đ", "1,300,000 đ", "", "", ""],
            ["B33HJK", "SGN", "DAD", "25/08/2025", "28/08/2025", "09:00", "14:00", "2,000,000 đ", "1,000,000 đ", "1,000,000 đ", "", "", ""],
        ]
        for row_data in mock_rows:
            row_pos = self.table.rowCount()
            self.table.insertRow(row_pos)
            for col, val in enumerate(row_data):
                self.table.setItem(row_pos, col, QTableWidgetItem(val))
