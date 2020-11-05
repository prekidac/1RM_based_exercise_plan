#! /usr/bin/python3

# Linux CLI workout assistant 

import os
from pathlib import Path
import json


class Trening(object):

    def __init__(self, config_path) -> None:
        self.config_path = config_path
        self.load_conf()
        self.print_exercise()
        self.update_config()

    def load_conf(self) -> None:
        with open(config_path) as f:
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
        self.cycle_rms = self.config[self.current_cycle + "_RMs"]
        self.one_rm = self.config["exercises"][self.current_exercise]["1RM"]

    def calculate_set_weights(self) -> None:
        self.weights = []
        for rm in self.cycle_rms:
            if self.current_exercise == "chin-up":
                weight = self.config["percents"][rm] * ( self.one_rm + self.config["my_weight"] ) - self.config["my_weight"]
                if weight < 0: weight = 0
                weight = weight // self.config["weight_inc"] * self.config["weight_inc"]
            else:
                weight = self.config["percents"][rm] * self.one_rm
                weight = weight // self.config["weight_inc"] * self.config["weight_inc"]
            self.weights.append(weight)


    def print_exercise(self) -> None:
        self.determine_exercise()
        self.calculate_set_weights()
        # print exercise
        pass

    def update_config(self) -> None:
        pass


if __name__ == "__main__":
    if os.name == "posix":
        config_file = ".config/trening.config.json"
    else:
        raise OSError("Linux only")
    config_path = os.path.join(Path.home(), config_file)
    trening = Trening(config_path)
