#! /usr/bin/python3

# Linux CLI workout assistant 

from pathlib import Path
import os, json, sys
from terminal import Terminal

config_file = "trening.config.json"

class Trening(object):

    def __init__(self) -> None:
        self.terminal = Terminal()
        self.load_conf()
        self.print_exercise()
        self.update_config()

    def load_conf(self) -> None:
        self.config_path = os.path.join(os.path.dirname(sys.argv[0]), config_file)
        with open(self.config_path) as f:
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
        self.terminal.clear()

        for w in self.weights[0:-1]:
            if self.current_cycle == 'neural':
                print(f"\t\t{w:>5}\tx {self.cycle_rms[-1]}")
            else:
                reps = self.cycle_rms[-1] - self.config["metabolic_rep_dec"]
                print(f"\t\t{w:>5}\tx {reps}")

        if self.current_cycle == 'neural':
            exercise = self.terminal.paint(self.current_exercise.title() + ":").RED_BOLD()
            print(f"\n  {exercise:<10}\t{self.weights[-1]:>5}\tx max")
        else:
            exercise = self.terminal.paint(self.current_exercise.title() + ":").GREEN_BOLD()
            reps = self.cycle_rms[-1] - self.config["metabolic_rep_dec"]
            print(f"\n  {exercise:<10}\t{self.weights[-1]:>5}\tx {reps}")
    
    def calculate_new_1rm(self) -> None:
        if self.current_cycle == "neural":
            while True:
                reps = input("\n  Puta podigao: ")
                if reps.isdigit() and 0 <= int(reps) < 10: break

            if self.current_exercise == "chin-up":
                weight = (self.config["exercises"]["chin-up"]["1RM"] + self.config["my_weight"])
                ratio = self.config["percents"][self.cycle_rms[-1]] / self.config["percents"][int(reps)]
                self.new_1rm = weight * ratio - self.config["my_weight"]
            else:
                weight = self.config["exercises"][self.current_exercise]["1RM"]
                ratio = self.config["percents"][self.cycle_rms[-1]] / self.config["percents"][int(reps)]
                self.new_1rm = weight * ratio
            self.new_1rm = round(self.new_1rm, 2)

            maximum = self.has_max()
            if maximum and self.new_1rm > maximum :
                self.new_1rm = maximum
        else:
            input("\n")
        
    def has_max(self) -> bool:
        return self.config["exercises"][self.current_exercise]["max"]

    def update_config(self) -> None:
        self.calculate_new_1rm()
        self.config["last_exercise"] = self.current_exercise
        self.config["last_cycle"] = self.current_cycle
        try:
            self.config["exercises"][self.current_exercise]["1RM"] = self.new_1rm
        except:
            pass
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)


if __name__ == "__main__":
    trening = Trening()
