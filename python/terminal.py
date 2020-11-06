import os
import psutil
import subprocess

HEADER = "\033[95m"
OKBLUE = "\033[94m"
OKCYAN = "\033[96m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RED_BOLD = "\033[31m" + "\033[01m"
GREEN_BOLD = "\033[32m" + "\033[01m"
END = "\033[0m"

class Color(object):

    def RED_BOLD(self)-> str:
        return RED_BOLD + self.string + END

    def GREEN_BOLD(self)-> str:
        return GREEN_BOLD + self.string + END

    def WARNING(self)-> str:
        return WARNING + self.string + END

    def OKBLUE(self)-> str:
        return OKBLUE + self.string + END

    def OKCYAN(self)-> str:
        return OKCYAN + self.string + END

class Terminal(object):

    def __init__(self):
        self.color = Color()

    def isblock(self) -> bool:
        """
        Check if blocking app is running
        """
        if os.name != "nt":
            target = "xtrlock"
        else:
            target = ""
        return target in (p.name() for p in psutil.process_iter())

    def clear(self) -> None:
        """
        Clear screen
        """
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def block(self) -> None:
        """
        Blocking keyboard and mouse 
        """
        if os.name != "nt":
            os.system("xtrlock &")
    
    def unblock(self) -> None:
        """
        Kill terminal blocker
        """
        sub = subprocess.Popen(["ps", "-A"], stdout=subprocess.PIPE)
        output = sub.communicate()[0]

        target = "xtrlock"
        target.split()
        for line in output.splitlines():

            if target in str(line):
                pid = int(line.split(None, 1)[0])
                os.kill(pid, 9)

    def paint(self, text: any) -> Color:
        self.color.string = str(text)
        return self.color