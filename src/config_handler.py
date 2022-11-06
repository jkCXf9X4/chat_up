import os
import xml.etree.ElementTree as ET


class ChatConfig:
    def __init__(self, path, nickname) -> None:
        self.path = path
        self.nickname = nickname
        self.dir, self.filename = os.path.split(path)
        self.name, self.ext = os.path.splitext(self.filename)

    def __str__(self) -> str:
        return f"{self.dir} {self.name} {self.ext} {self.nickname}"


class ConfigHandler:

    def __init__(self, path) -> None:
        self.path = path
        self.chats: list[ChatConfig] = []
        self.parse_config()

        # for i in self.chats:
        #     print(i)

    def parse_config(self):
        tree = ET.parse(self.path)
        root = tree.getroot()
        for chat in root:
            path = chat.find("path").text
            nick = chat.find("nickname").text
            self.chats.append(ChatConfig(path, nick))
