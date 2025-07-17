from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import QTimer, Qt
import random

class PNRListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.mock_data()
        self.setup_auto_update()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.title = QLabel("Danh sách PNR")
        self.title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["PNR", "Giờ bay", "Ngày bay", "Chiều", "Giá", "Trạng thái"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("color: white;")
        layout.addWidget(self.table)

        self.setLayout(layout)

    def mock_data(self):
        self.data = [
            {"pnr": "ABC123", "gio": "10:00", "ngay": "20/08/2025", "chieu": "HAN-SGN", "gia": 1200000},
            {"pnr": "DEF456", "gio": "13:30", "ngay": "21/08/2025", "chieu": "SGN-HAN", "gia": 950000},
            {"pnr": "XYZ789", "gio": "17:15", "ngay": "22/08/2025", "chieu": "DAD-HAN", "gia": 1100000},
        ]
        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(len(self.data))
        for row, item in enumerate(self.data):
            self.table.setItem(row, 0, QTableWidgetItem(item["pnr"]))
            self.table.setItem(row, 1, QTableWidgetItem(item["gio"]))
            self.table.setItem(row, 2, QTableWidgetItem(item["ngay"]))
            self.table.setItem(row, 3, QTableWidgetItem(item["chieu"]))
            self.table.setItem(row, 4, QTableWidgetItem(f"{item['gia']:,} đ"))
            self.table.setItem(row, 5, QTableWidgetItem("✓"))

    def setup_auto_update(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.auto_update)
        self.timer.start(5 * 60 * 1000)  # 5 phút

    def auto_update(self):
        for item in self.data:
            # random giảm giá giả lập
            if random.random() < 0.5:
                old_price = item['gia']
                new_price = old_price - random.randint(50000, 200000)
                item['gia'] = max(500000, new_price)
        self.refresh_table()
