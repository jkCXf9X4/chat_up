import argparse


class AddonBase:
    
    command = "command"

    def __init__(self, input: str, default_dir, text_to_user_callback, text_to_all_users_callback) -> None:

        self.raw_input = input
        self.input_array = input.split(" ")
        self.name = self.input_array[0]
        self.raw_args = self.input_array[1:]

        self.default_dir = default_dir
        self.text_to_user_callback = text_to_user_callback
        self.text_to_all_users_callback = text_to_all_users_callback

        self.parser = argparse.ArgumentParser(prog=self.name)

    def set_removal_callback(self, removal_callback):
        self.removal_callback = removal_callback
        
    def call_removal_callback(self):
        self.removal_callback(self.command)

    def parse(self):
        
        try:
            self.args = self.parser.parse_args(self.raw_args)
        except SystemExit:
            pass

    def is_help(self):
        if ("-h" in self.raw_args or "--help" in self.raw_args):
            return True
        return False