#! /usr/bin/env python3

# Linux CLI workout assistant

import termios
import questionary
from questionary import Style
from color_schema import questionary_style
from columnar import columnar
import json
import os
import sys
from posixpath import expanduser
import subprocess
import argparse
from pathlib import Path
from colored import fg, attr
import logging

FORMAT = f"%(filename)s: {attr('bold')}%(levelname)s {fg(3)+attr('bold')}%(message)s{attr('reset')} line: %(lineno)s, %(relativeCreated)dms"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

logging.disable(logging.WARNING)

data_path = os.path.join(Path.home(), ".local/share/trening.json")
style = Style(questionary_style)


class Trening(object):

    def __init__(self) -> None:
        self.data_path = data_path
        self.load_conf()

    def load_conf(self) -> None:
        with open(self.data_path) as f:
            self.config = json.load(f)

        self.determine_exercise()
        self.cycle_rms = self.config[self.current_cycle + "_RMs"]
        self.one_rm = self.config["exercises"][self.current_exercise]["1RM"]
        self.maximum = self.config["exercises"][self.current_exercise]["max"]
        self.record = self.config["exercises"][self.current_exercise]["record"]
        self.energy = self.config["energy_per_set"]
        self.rest_min = self.config["rest_minutes"]
        self.calculate_set_weights()

    def determine_exercise(self) -> None:
        index = self.config["exercise_order"].index(
            self.config["last_exercise"])
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

    def calculate_set_weights(self) -> None:
        self.weights = []
        for rm in self.cycle_rms:
            if self.current_exercise == "chin-up":
                weight = self.config["percents"][rm] * \
                    self.one_rm - self.config["my_weight"]
                if weight < 0:
                    weight = 0
            else:
                weight = self.config["percents"][rm] * self.one_rm

            weight = weight // self.config["weight_inc"] * \
                self.config["weight_inc"]
            self.weights.append(weight)

    def print_exercise(self, current: int) -> None:
        os.system("clear")

        i = 0
        for w in self.weights[:-1]:
            if self.current_cycle == 'neural':
                reps = self.cycle_rms[-1]
            else:
                reps = self.cycle_rms[-1] - self.config["metabolic_rep_dec"]
            if i == current:
                w = fg("2") + str(w) + attr("reset")
            if i == len(self.weights) // 2:
                print(f"\t\t{w}\tx {reps}")
            else:
                print(f"\t\t{w}\t")
            i += 1

        w = self.weights[-1]
        if i == current:
            w = fg(2) + str(w) + attr("reset")

        if self.current_cycle == 'neural':
            exercise = fg(1) + attr(1) + \
                self.current_exercise.title() + ":" + attr("reset")
            print(f"\n  {exercise:<10}\t{w}\tx max")
        else:
            exercise = fg(2) + attr(1) + \
                self.current_exercise.title() + ":" + attr("reset")
            print(f"  {exercise:<10}\t{w}\t")
        print(flush=True)

    def calculate_new_1rm(self) -> float:
        def check(x):
            try:
                if 0 <= int(x) <= 10:
                    return True
                else:
                    return "0-10"
            except:
                return "0-10"

        reps = questionary.text("Reps lifted:", qmark=" ", validate=check, style=style).ask()
        if not reps:
            exit(1)
        ratio = self.config["percents"][self.cycle_rms[-1]
                                        ] / self.config["percents"][int(reps)]
        return round(self.one_rm * ratio, 2)

    def update_config(self, new_1rm: float = None) -> None:
        self.config["last_exercise"] = self.current_exercise
        self.config["last_cycle"] = self.current_cycle

        if new_1rm:
            if self.maximum:
                self.config["exercises"][self.current_exercise]["1RM"] = min(
                    new_1rm, self.maximum)
            self.config["exercises"][self.current_exercise]["record"] = max(
                self.record, new_1rm)
        else:
            logging.debug(f"1RM and record not changed")

        with open(self.data_path, "w") as f:
            json.dump(self.config, f, indent=4)
        energy = self.energy * len(self.cycle_rms)
        logging.debug(f"Energy: {energy}")
        p = subprocess.Popen(["energy", "-e", "trening", f"{energy}"])
        p.wait()

    def print_stats(self) -> None:
        exercises = self.config["exercises"]
        weight = self.config["my_weight"]
        logging.debug(f"Exercises: {exercises}")
        logging.debug(f"Weight: {weight}")
        headers = [""]
        data = []
        rms = ["1RM"]
        records = ["Record"]
        percents = ["1RM/weight"]
        for i in exercises:
            logging.debug(f"{i} - {exercises[i]}")
            headers.append(i.capitalize())
            if exercises[i]["1RM"] == exercises[i]["max"]:
                rms.append(
                    f"{attr('bold')+fg(2)}{round(exercises[i]['1RM'])}{attr('reset')}")
            else:
                rms.append(round(exercises[i]["1RM"]))
            percents.append(round(exercises[i]["1RM"]/weight, 2))
            records.append(round(exercises[i]["record"]))
        data.append(rms)
        data.append(records)
        data.append(percents)
        table = columnar(data, headers, min_column_width=10, justify="c")
        print(table)

    def _rest(self) -> None:
        p = subprocess.Popen(["pauza", "-b", "-t", "Prepare", f"{self.rest_min}m"])
        p.wait()

    def run(self) -> None:
        new_1rm = None
        for i in range(len(self.cycle_rms)):
            self.print_exercise(i)
            if i > 0:
                self._rest()
                self.print_exercise(i)
            if i == len(self.cycle_rms) - 1 and self.current_cycle == 'neural':
                new_1rm = self.calculate_new_1rm()
            else:
                termios.tcflush(sys.stdin,termios.TCIFLUSH)
                if questionary.text("Done:", qmark=" ", style=style).ask() == None:
                    exit(1)
        else:
            self.update_config(new_1rm)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--stats", action="store_true",
                        help="display workout statistics")
    args = parser.parse_args()
    trening = Trening()
    if args.stats:
        trening.print_stats()
    else:
        trening.run()
