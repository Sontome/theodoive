import sys
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect,QSize
from PyQt5.QtGui import QColor, QIcon, QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFrame, QLabel, QSizePolicy, QStackedLayout, QGraphicsDropShadowEffect
)
import os 
from check_pnr import CheckPNRWidget
from giu_ve import GiuVeWidget
from pnr_list import PNRListWidget


class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(50)
        self.setStyleSheet("""
            background-color: #f3f4f6; 
            border-top-left-radius: 15px; 
            border-top-right-radius: 15px;
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 10, 0)

        self.title = QLabel("Tool Check Giá")
        self.title.setStyleSheet("color: #111827; font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title)

        layout.addStretch()

        self.minBtn = QPushButton("—")
        self.closeBtn = QPushButton("✕")
        for btn in (self.minBtn, self.closeBtn):
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #374151;
                    border: none;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #d1d5db;
                    border-radius: 5px;
                }
            """)
            layout.addWidget(btn)

        self.minBtn.clicked.connect(parent.showMinimized)
        self.closeBtn.clicked.connect(parent.close)

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.old_pos
        self.parent.move(self.parent.x() + delta.x(), self.parent.y() + delta.y())
        self.old_pos = event.globalPos()

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tool Check Giá")
        self.setGeometry(200, 100, 1100, 650)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.wrapper = QWidget()
        self.wrapper.setObjectName("mainWindow")
        self.setCentralWidget(self.wrapper)

        self.main_layout = QVBoxLayout(self.wrapper)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # Shadow
        self.shadow_frame = QFrame()
        self.shadow_frame.setStyleSheet("border-radius: 15px; background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f0f4f8, stop:1 #dbeafe);")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.shadow_frame.setGraphicsEffect(shadow)

        self.main_layout.addWidget(self.shadow_frame)

        self.container_layout = QVBoxLayout(self.shadow_frame)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(0)

        # Title Bar
        self.titlebar = TitleBar(self)
        self.container_layout.addWidget(self.titlebar)

        # Body
        self.body = QHBoxLayout()
        self.body.setContentsMargins(0, 0, 0, 0)
        self.container_layout.addLayout(self.body)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("""
            background-color: #e5e7eb;
            border-bottom-left-radius: 15px;
        """)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(10, 20, 10, 10)
        self.sidebar_layout.setSpacing(15)

        self.body.addWidget(self.sidebar)

        # Content
        self.content_area = QFrame()
        self.content_area.setStyleSheet("""
            background-color: transparent;
            border-bottom-right-radius: 15px;
        """)
        self.content_layout = QStackedLayout()
        self.content_area.setLayout(self.content_layout)

        self.body.addWidget(self.content_area)

        self.modules = {
            "🔍 Check PNR": CheckPNRWidget(),
            "📄 Danh sách PNR": PNRListWidget(),
            "✈️ Giữ vé": GiuVeWidget()
        }

        

        for label, widget in self.modules.items():
            #icon_path = icon_map.get(label.replace("🔍 ", "").replace("📄 ", "").replace("✈️ ", ""), "")
            btn = QPushButton(f"  {label}")
            #btn.setIcon(QIcon(os.path.join("icons", icon_path)))
            #btn.setIconSize(QSize(18, 18))
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #1f2937;
                    font-weight: 600;
                    font-size: 14px;
                    border: none;
                    text-align: left;
                    padding: 6px 8px;
                }
                QPushButton:hover {
                    background-color: #d1d5db;
                    border-radius: 6px;
                }
            """)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(lambda checked, w=widget: self.switch_module(w))
            self.sidebar_layout.addWidget(btn)
            self.content_layout.addWidget(widget)

        # Load default module
        self.switch_module(list(self.modules.values())[0])

    def switch_module(self, widget):
        index = self.content_layout.indexOf(widget)
        if index != -1:
            anim = QPropertyAnimation(self.content_area, b"geometry")
            anim.setDuration(200)
            anim.setStartValue(QRect(self.content_area.x() + 30, self.content_area.y(), self.content_area.width(), self.content_area.height()))
            anim.setEndValue(self.content_area.geometry())
            anim.start()
            self.content_layout.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
