#! /usr/bin/python3
import sys, os
import json

config_file = "trening.config.json"

class Trening(object):
    """
    docstring
    """
    def __init__(self) -> None:
        self.load_conf()

    def load_conf(self) -> None:
        with open(os.path.join(os.path.dirname(sys.argv[0]), config_file)) as f:
            self.config = json.load(f)
        
    def determine_exercise(self) -> None:
        pass

    def print_exercise(self) -> None:
        pass

    def update_config(self) -> None:
        pass


if __name__ == "__main__":
    trening = Trening()
