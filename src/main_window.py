#! /usr/bin/python3

import sys
import os
from venv import create

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from chat_handler import ChatHandler
from chat_widget import ChatWidget
from config_handler import ConfigHandler, ChatConfig
from stylesheet import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        main_widget = QWidget()
        main_widget.setStyleSheet(qwidget_style)
        self.resize(QSize(1100, 900))

        self.user = os.getenv('USER')
        self.nick = self.user

        self.setWindowTitle(f"")

        main_layout = QHBoxLayout()
        button_frame = QFrame()
        button_frame.setStyleSheet(qframe_style)
        self.buttons = QVBoxLayout()
        self.buttons.setAlignment(Qt.AlignmentFlag.AlignTop)
        title = QLabel("ACSIM")
        self.button_group = QButtonGroup()
        title.setStyleSheet(title_style)
        self.buttons.addWidget(title)
        self.stacked_layout = QStackedLayout()

        main_layout.setContentsMargins(0, 0, 0, 0)
        self.stacked_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(button_frame)
        main_layout.addLayout(self.stacked_layout)
        button_frame.setLayout(self.buttons)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.config_handler = ConfigHandler(
            "/home/erik/src/int_chat/test_chat/.chat_config.xml")
        self.load_config()

    def load_config(self):
        for chat_conf in self.config_handler.chats:
            chat_handler = ChatHandler(
                self.user, chat_conf.nickname, chat_conf.name, chat_conf.dir)
            self.create_chat(chat_handler, chat_conf.name)

    def create_chat(self, chat_handler, channel):

        button = QPushButton(channel)
        button.setCheckable(True)
        widget = ChatWidget(chat_handler, button)
        self.button_group.addButton(button)
        button.setStyleSheet(channel_buttons_style)

        self.buttons.addWidget(button)
        index = self.stacked_layout.addWidget(widget)

        def channel_pressed(index, button):
            self.stacked_layout.setCurrentIndex(index)

        button.pressed.connect(lambda: channel_pressed(index, button))

        button.click()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
