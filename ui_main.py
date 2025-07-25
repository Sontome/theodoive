import sys
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QPoint, QEasingCurve,QUrl
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFrame, QLabel, QSizePolicy, QGraphicsDropShadowEffect
)
import os
from check_pnr import CheckPNRWidget
from giu_ve import GiuVeWidget
from pnr_list import PNRListWidget
from PyQt5.QtMultimedia import QSoundEffect

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
        self.click_sound = QSoundEffect()
        self.click_sound.setSource(QUrl.fromLocalFile("click.wav"))
        self.click_sound.setVolume(0.5)
        self.setWindowTitle("Tool Check Giá")
        self.setGeometry(200, 100, 1100, 650)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.wrapper = QWidget()
        self.setCentralWidget(self.wrapper)

        self.main_layout = QVBoxLayout(self.wrapper)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # Shadow
        self.shadow_frame = QFrame()
        self.shadow_frame.setStyleSheet(
            "border-radius: 15px; background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f0f4f8, stop:1 #dbeafe);"
        )
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
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        self.body.addWidget(self.content_area)

        # Modules
        self.modules = {
            "🔍 Check PNR": CheckPNRWidget,
            "📄 Danh sách PNR": PNRListWidget,
            "✈️ Giữ vé": GiuVeWidget
        }

        for label, widget_class in self.modules.items():
            btn = QPushButton(f"  {label}")
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
                QPushButton:pressed {
                    background-color: #d3e3fd;
                    border-radius: 6px;
                }                              
            """)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            def handle_click(cls=widget_class):
                self.click_sound.play()  # Phát âm thanh
                self.switch_module(cls())
            btn.clicked.connect(lambda checked, cls=widget_class: handle_click(cls))
            
            
            self.sidebar_layout.addWidget(btn)
        self.fade_in()
        # Load default
        self.switch_module(CheckPNRWidget())

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def switch_module(self, widget):
        self.clear_layout(self.content_layout)

        # Đặt vị trí bắt đầu (ngoài khung nhìn bên phải)
        widget.setParent(self.content_area)
        widget.move(self.content_area.width(), 0)
        widget.show()

        self.content_layout.addWidget(widget)

        anim = QPropertyAnimation(widget, b"pos", self)
        anim.setDuration(800)
        anim.setStartValue(QPoint(self.content_area.width(), 0))
        anim.setEndValue(QPoint(0, 0))
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()

    def fade_in(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(600)  # có thể chỉnh chậm nhanh
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()