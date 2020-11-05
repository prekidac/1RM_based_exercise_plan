#! /usr/bin/python3
import json, os

config_file = "trening.config.json"
class Trening(object):
    """
    docstring
    """
    def __init__(self) -> None:
        self.load_conf()

    def load_conf(self) -> None:
        with open(os.path.join(os.getcwd(), config_file)) as f:
            self.config = json.load(f)

if __name__ == "__main__":
    trening = Trening()
