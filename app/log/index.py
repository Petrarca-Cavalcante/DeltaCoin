"""_"""

import os
from datetime import datetime


class Log:
    """LogPrinter is the class used to register
    every log in it. \n
    Receives:\n
    f_name = class name\n
    params = class params\n
    print_else = Tells the methods if the log should else be printed to terminal.\n
    """

    dir_reports = os.path.normpath("docs_generated")


    def __init__(self, cls_name: str, params= None, print_else:bool = False):
        self.cls_name = cls_name
        self.params = params
        self.else_print = print_else
        self.log_file = os.path.normpath(os.path.join("docs_generated", f"{datetime.now().strftime('%d-%m-%Y')}_log.txt"))


    def write(self, message: str, level:str= " ", f_log: bool = False):
        """Writes a log in the following format\n
        [ TIMESTAMP ] [ CLASS NAME ] LEVEL OR INFO - MESSAGE.  \n_
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[ {timestamp} ] [{self.cls_name.center(23)}] {level.center(13)} - {message}"

        if f_log:
            log_entry = "\n" + log_entry

        if self.else_print:
            print(log_entry)

        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(log_entry + "\n")


    def init_log(self, message:str):
        """Writes the first log of a class"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"\n\n\n[ {timestamp} ] [{25*'='} {message.center(25)} {30*'='}] \n"
        if self.else_print:
            print(log_entry)

        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(log_entry + "\n")