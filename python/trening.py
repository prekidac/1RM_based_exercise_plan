#! /usr/bin/python3
import os
from pathlib import Path
import json

if os.name == "posix":
    config_file = ".config/trening.config.json"

class Trening(object):
    """
    docstring
    """
    def __init__(self) -> None:
        self.load_conf()

    def load_conf(self) -> None:
        with open(os.path.join(Path.home(), config_file)) as f:
            self.config = json.load(f)
        for i in self.config:
            print(i)
    def determine_exercise(self) -> None:
        pass

    def print_exercise(self) -> None:
        pass

    def update_config(self) -> None:
        pass


if __name__ == "__main__":
    trening = Trening()
