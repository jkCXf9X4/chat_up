#! /usr/bin/python3

import argparse
import os
import sys
import time

from chat_handler import ChatHandler
from addons.addon_handler import AddonHandler

from ui import ChatWidget


from PySide6.QtWidgets import QApplication


if __name__ == "__main__":

    default_dir = "/home/erik/src/int_chat/test_chat/"
    parser = argparse.ArgumentParser(description="DevSim chat")
    parser.add_argument('-r', "--room", help='the room name, no spaces allowed')
    parser.add_argument('-d', "--directory", default=default_dir,
                        help='the directory where the chat is stored')
    parser.add_argument('-n', "--nick", default="", help='Custom nickname')
    args = parser.parse_args()
    
    user = os.getenv('USER')

    chat_handler = ChatHandler(user, args.room, args.directory, args.nick)
    addon_handler = AddonHandler(default_dir=args.directory)

    #Init gui
    app = QApplication([])

    title = f"Devsim chat, room {args.room}, user {user}"
    widget = ChatWidget(title, chat_handler, addon_handler)
    widget.show()

    sys.exit(app.exec())
