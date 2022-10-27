from addons.addon_base import AddonBase
from addons.screen_share import ScreenShare

class AddonHandler:

    def __init__(self, default_dir) -> None:
        self.addons: list[AddonBase] = [ScreenShare]
        self.default_dir = default_dir
        self.running_addons = {}

    def run_addon(self, text, text_to_user_callback, text_to_all_users_callback):
        for addon in self.addons:
            if addon.command in text:
                a : AddonBase = addon(text, self.default_dir, text_to_user_callback,
                      text_to_all_users_callback)
                # a.set_removal_callback(self.remove_addon)
                self.running_addons[addon.command] = a

    # def remove_addon(self, command):
    #     # remove reference to garbage collect
    #     self.running_addons[command] = None
    #     print(self.running_addons)
