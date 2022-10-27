import argparse
from addons.addon_base import AddonBase

from PySide6.QtCore import *
from PySide6.QtWidgets import *


class ScreenSaveHandler:
    def __init__(self, dir, name) -> None:
        self.dir = dir
        self.name = name

    def save_screen(self):
        pass

    def remove_save(self):
        pass


class ShareScreenWidget(QWidget):

    def __init__(self, screen_save_handler, interval):
        QWidget.__init__(self)

        self.interval = interval
        self.screen_save_handler: ScreenSaveHandler = screen_save_handler

        self.resize(QSize(200, 200))
        self.setWindowTitle("Share screen")

        self.text_area = QLabel()
        self.text_area.setText("Close window to stop sharing")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text_area)

        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.save_picture)
        self.timer.start(self.interval*1000)

        self.save_picture()

    @Slot()
    def save_picture(self):
        self.screen_save_handler.save_screen()

    def closeEvent(self, event):
        self.timer.stop()

        self.screen_save_handler.remove_save()

        self.close()


class ScreenShare(AddonBase):

    command = "share-screen"

    def __init__(self, input: str, default_dir, text_to_user_callback, text_to_all_users_callback) -> None:
        super().__init__(input, default_dir, text_to_user_callback, text_to_all_users_callback)

        self.parser.add_argument('-d', "--directory", default=default_dir,
                                 help='the directory where the pictures is stored')
        self.parser.add_argument(
            '-i', "--interval", type=int, default=5, help='Screen update interval')
        self.parser.add_argument(
            '-f', "--file", default="print_screen", help='Name of the saved print-screen')

        self.parse()

        if self.is_help():
            return

        self.text_to_user_callback("""=====================================
Starting addon share-screen, dont show anything sensitive. 
This application is file based. Use a common folder where ONLY 
the participants have access to ensure information is not 
distributed to everyone on the network
=====================================""")

        self.screen_handler = ScreenSaveHandler(
            self.args.directory, name=self.args.file)

        self.widget = ShareScreenWidget(
            self.screen_handler, self.args.interval)
        self.widget.show()
