
from email import message
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from chat_handler import ChatHandler, Message
from stylesheet import *

import time


diff_position = 50

BUBBLE_PADDING = QMargins(15, 20, diff_position+25, 5)
TEXT_PADDING = QMargins(25, 40, diff_position+35, 15)


class MessageDelegate(QStyledItemDelegate):

    def __init__(self, current_user) -> None:
        super().__init__()

        self.current_user = current_user

    _font = None

    def get_color(self, user):
        if user == self.current_user:
            return "#4ab1d8"
        else:
            return "#527cbc"

    def get_trans(self, user):
        if user == self.current_user:
            return QPoint(10, 0)
        else:
            return QPoint(diff_position, 0)

    def get_doc(self, rectangle, text):
        text_option = QTextOption()
        text_option.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

        font = QFont("Helvetica [Cronyx]", 14, QFont.Bold)
        doc = QTextDocument(text)
        doc.setTextWidth(rectangle.width())
        doc.setDefaultTextOption(text_option)
        doc.setDefaultFont(font)
        doc.setDocumentMargin(0)
        return doc

    def paint(self, painter, option, index):
        painter.save()
        message: Message = index.model().data(index, Qt.DisplayRole)
        user = message.user
        text = message.message

        trans = self.get_trans(user)
        painter.translate(trans)

        bubble_rect = option.rect.marginsRemoved(BUBBLE_PADDING)
        text_rect = option.rect.marginsRemoved(TEXT_PADDING)

        # draw the bubble, changing color
        painter.setPen(Qt.NoPen)
        color = QColor(self.get_color(user))
        painter.setBrush(color)
        painter.drawRoundedRect(bubble_rect, 7, 7)

        # draw the timestamp
        font = painter.font()
        font.setPointSize(10)
        font.setItalic(True)
        painter.setFont(font)
        painter.setPen(Qt.black)

        time_str = time.strftime(
            '%y-%m-%d %H:%M:%S', time.localtime(message.time))
        painter.drawText(bubble_rect.topRight() -
                         QPoint(200, 0) + QPoint(0, 20), time_str)

        user_string = f"{message.user} << {message.nick} >> wrote:"

        painter.drawText(bubble_rect.topLeft() - QPoint(0, 5), user_string)

        doc = self.get_doc(text_rect, text)

        painter.translate(text_rect.topLeft())
        doc.drawContents(painter)
        painter.restore()

    def sizeHint(self, option, index):
        message: Message = index.model().data(index, Qt.DisplayRole)
        text = message.message

        text_rect = option.rect.marginsRemoved(TEXT_PADDING)
        doc = self.get_doc(text_rect, text)

        text_rect.setHeight(doc.size().height())
        text_rect = text_rect.marginsAdded(TEXT_PADDING)
        return text_rect.size()


class MessageModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super(MessageModel, self).__init__(*args, **kwargs)
        self.messages = []
        self.last_message_sender = ""

    def data(self, index, role) -> Message:
        if role == Qt.DisplayRole:
            return self.messages[index.row()]

    def rowCount(self, index):
        return len(self.messages)

    def add_message(self, message: Message):
        if message.user != self.last_message_sender:
            self.last_message_sender = message.user
        self.messages.append(message)
        self.layoutChanged.emit()


class ChatWidget(QWidget):

    def __init__(self, chat_handler: ChatHandler, button: QPushButton):
        super().__init__()

        self.chat_handler = chat_handler
        self.channel_button = button

        self.messages = QListView()
        self.messages.setResizeMode(QListView.Adjust)
        self.messages.setItemDelegate(MessageDelegate(self.chat_handler.user))
        self.messages.setStyleSheet(list_view_style)
        self.messages.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.model = MessageModel()
        self.messages.setModel(self.model)

        self.new_message = QTextEdit()
        self.new_message.installEventFilter(self)
        self.new_message.setStyleSheet(qtext_edit_style)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        chat_layout = QVBoxLayout()
        chat_layout.setContentsMargins(0, 0, 0, 0)
        chat_layout.addWidget(self.messages)
        chat_layout.addWidget(self.new_message)

        user_layout = QVBoxLayout()
        user_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        user_frame = QFrame()
        user_frame.setLayout(user_layout)

        user_online_label = QLabel("Online users")
        user_online_label.setStyleSheet(users_style)
        self.users = QLabel("Placeholder")
        user_layout.addWidget(user_online_label)
        user_layout.addWidget(self.users)

        main_layout.addLayout(chat_layout)
        main_layout.addWidget(user_frame)

        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        self.new_message.setFocus()

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_new_messages)
        self.timer.start(5000)

        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.get_users)
        self.timer2.start(25000)

        self.display_new_messages()
        self.get_users()

    def display_new_messages(self):
        for m in self.chat_handler.get_new_messages():
            self.model.add_message(m)
            self.messages.scrollToBottom()

    def get_users(self):
        self.chat_handler.set_user_online()
        users = self.chat_handler.get_online_users()
        s = ""
        for i in users:
            s += f"{i}\n"
        self.users.setText(s)

    def send_message(self):
        m = self.new_message.toPlainText()
        if m != "":
            self.chat_handler.add_message(m)
            self.display_new_messages()
            self.new_message.clear()

    def closeEvent(self, event):
        self.chat_handler.close()

    # dont send when pressing shift + enter
    def eventFilter(self, obj, event):
        if obj is self.new_message and event.type() == QEvent.KeyPress:
            modifiers = event.modifiers()
            # ctrl = bool(modifiers & Qt.ControlModifier)
            shift = bool(modifiers & Qt.ShiftModifier)
            # alt = bool(modifiers & Qt.AltModifier)
            enter_key = event.key() in (Qt.Key_Return, Qt.Key_Enter)

            if not shift and enter_key:
                self.send_message()
                return True
        return super(ChatWidget, self).eventFilter(obj, event)
