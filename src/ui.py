
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from chat_handler import ChatHandler
from addons.addon_handler import AddonHandler


class ChatWidget(QWidget):

    def __init__(self, title, chat_handler: ChatHandler, addon_handler: AddonHandler):
        super().__init__()

        self.chat_handler = chat_handler
        self.addon_handler = addon_handler

        self.resize(QSize(900, 700))
        self.setWindowTitle(title)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setFontPointSize(13)

        self.message = QTextEdit()
        self.message.setMinimumHeight(70)
        self.message.setMaximumHeight(70)
        self.message.installEventFilter(self)
        self.message.setFontPointSize(15)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text_area)
        self.layout.addWidget(self.message)

        self.setLayout(self.layout)
        self.message.setFocus()

        self.last_user = ""

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_new_messages)
        self.timer.start(5000)

        self.display_new_messages()

    @Slot()
    def display_new_messages(self):
        for m in self.chat_handler.get_new_messages():
            # print(f"New message {m}")
            if m.user != self.last_user:
                self.text_area.append("------------------------------")
                self.last_user = m.user
            self.text_area.append(m.get_chat_str())

    @Slot()
    def send_message(self):
        m = self.message.toPlainText()

        if m[0] == "#":
            self.addon_handler.run_addon(
                m[1:], self.text_area.append, self.chat_handler.add_message)
        else:
            self.chat_handler.add_message(m)
        self.message.clear()

    def closeEvent(self, event):
        self.chat_handler.close()

    def eventFilter(self, obj, event):
        if obj is self.message and event.type() == QEvent.KeyPress:
            modifiers = event.modifiers()
            # ctrl = bool(modifiers & Qt.ControlModifier)
            shift = bool(modifiers & Qt.ShiftModifier)
            # alt = bool(modifiers & Qt.AltModifier)
            enter_key = event.key() in (Qt.Key_Return, Qt.Key_Enter)

            if not shift and enter_key:
                self.send_message()
                return True
        return super(ChatWidget, self).eventFilter(obj, event)
