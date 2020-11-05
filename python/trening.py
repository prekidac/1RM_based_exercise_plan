#! /usr/bin/python3

# Linux CLI workout assistant 

from pathlib import Path
import os, json

class Trening(object):

    def __init__(self, config_path) -> None:
        self.config_path = config_path
        self.clear_terminal = lambda : os.system("clear")
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
        self.clear_terminal()
        for w in self.weights[0:-1]:
            if self.current_cycle == 'neural':
                print(f"\t\t{w}\tx {self.cycle_rms[-1]}")
            else:
                reps = self.cycle_rms[-1] - self.config["metabolic_rep_dec"]
                print(f"\t\t{w}\tx {reps}")
        
        red_bold = "\033[31m" + "\033[01m"
        green_bold = "\033[32m" + "\033[01m"
        end = "\033[0m"
        if self.current_cycle == 'neural':
            exercise = red_bold + self.current_exercise.title() + ":" + end
            print(f"\n  {exercise:<10}\t{self.weights[-1]}\tx max")
        else:
            exercise = green_bold + self.current_exercise.title() + ":" + end
            reps = self.cycle_rms[-1] - self.config["metabolic_rep_dec"]
            print(f"\n  {exercise:<10}\t{self.weights[-1]}\tx {reps}")
    
    def calculate_new_one_rm(self) -> None:
        pass

    def update_config(self) -> None:
        self.calculate_new_one_rm()
        self.config["last_exercise"] = self.current_exercise
        self.config["last_cycle"] = self.current_cycle
        #self.config["exercises"][self.current_exercise]["1RM"] = self.new_one_rm
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)


if __name__ == "__main__":
    if os.name == "posix":
        config_file = ".config/trening.config.json"
    else:
        raise OSError("Linux only")
    config_path = os.path.join(Path.home(), config_file)
    trening = Trening(config_path)
