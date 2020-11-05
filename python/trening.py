#! /usr/bin/python3

# Linux CLI workout assistant 

import os
from pathlib import Path
import json

if os.name == "posix":
    config_file = ".config/trening.config.json"
else:
    raise OSError("Not implemented")


class Trening(object):

    def __init__(self) -> None:
        self.load_conf()
        self.determine_exercise()

    def load_conf(self) -> None:
        with open(os.path.join(Path.home(), config_file)) as f:
            self.config = json.load(f)

    def determine_exercise(self) -> None:
        index = self.config["exercise_order"].index(self.config["last_exercise"])
        if index + 1 < len(self.config["exercise_order"]):
            self.current_exercise = self.config["exercise_order"][index + 1]
            self.current_cycle = self.config["last_cycle"]
        else:
            index = self.config["cycle_order"].index(self.config["last_cycle"])
            if index + 1 < len(self.config["cycle_order"]):
                self.current_cycle = self.config["cycle_order"][index + 1]
            else:
                self.current_cycle = self.config["cycle_order"][0]
            self.current_exercise = self.config["exercise_order"][0]


    def print_exercise(self) -> None:
        pass

    def update_config(self) -> None:
        pass


if __name__ == "__main__":
    trening = Trening()
