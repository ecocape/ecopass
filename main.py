import pyclip
import os
import json
import sqlite3
from random import choice
from time import sleep
from pathlib import Path, PosixPath, WindowsPath

try:
    linux_cfg_path = PosixPath(os.environ["HOME"], ".config", "ecopass").resolve()
except NotImplementedError:
    windows_cfg_path = WindowsPath(os.environ["HOME"], "AppData", "Roaming", "ecopass").resolve()
if os.name == "posix":
    use_cfg_path = linux_cfg_path
if os.name == "nt":
    use_cfg_path = windows_cfg_path

pwpath = ""
using_sqlite = False
letters = "qwertyuiopasdfghjklzxcvbnm"
numbers = "1234567890"
symbols = "~`!@#$%^&*()_-+={[}]|:;'\"<>,.?/\\"
cfg = {
    'generation': {
        'includeLetters': True,
        'includeNumbers': True,
        'includeSymbols': True,
        'enableCapitalization': True
    }, 'other': {
        'pw_path': '',
        'use_sqlite': True
    }
}

def checkcfg(use_cfg_path):
    try:
        if Path.is_file(Path(f"{use_cfg_path}", "config.json")) == False:
            with open(Path(f"{use_cfg_path}", "config.json"), "w+") as f:
                json.dump(cfg, f, indent=4)
    except FileNotFoundError:
        os.mkdir(use_cfg_path)
        checkcfg(use_cfg_path)
    except json.decoder.JSONDecodeError:
        json.load(f.truncate())
        json.dump(cfg, f, indent=4)
checkcfg(use_cfg_path)

with open(Path(f"{use_cfg_path}", "config.json"), "r+") as f:
    selected = ""
    load_cfg = json.load(f)
    if load_cfg["generation"]["includeLetters"] == True:
        selected += letters
    if load_cfg["generation"]["includeNumbers"] == True:
        selected += numbers
    if load_cfg["generation"]["includeSymbols"] == True:
        selected += symbols
    if load_cfg["generation"]["enableCapitalization"] == True:
        selected += letters.swapcase()
    if load_cfg["other"]["pw_path"] == "":
        pwpath = os.getcwd()
    elif load_cfg["other"]["pw_path"] != "":
        pwpath = load_cfg["other"]["pw_path"]
    if load_cfg["other"]["use_sqlite"] == True:
        using_sqlite = True
        try:
            conn = sqlite3.connect(f"{pwpath}/saved.db")
            c = conn.cursor()
            c.execute("""
            CREATE TABLE cr(
                name text,
                created text         
            )""")
        except sqlite3.OperationalError:
            pass

def main():
    try:
        choice = input("i would like to\n1: generate a new password\n2: manage .db passwords\n> ")
        match choice:
            case "1":
                pwinput()
            case "2":
                pwmanage()
    except KeyError:
        print(f"option \"{choice}\" doesn't exist")
        sleep(2)
        main()

def pwmanage():
    inpt = input("What is the password used for?\n> ")
    c.execute(f"SELECT * FROM cr WHERE name LIKE '%{inpt}%'")
    print(c.fetchall())

def gen(length, usedfor, selected):
    generated = ""
    for _ in range(length):
        generated += choice(selected)
    try:
        pyclip.copy(generated)
    except pyclip.base.ClipboardSetupException:
        print("\nYour system may not have the needed utilities to copy the password. Please check the following link:\nhttps://github.com/spyoungtech/pyclip#platform-specific-notesissues")
        exit()
    if using_sqlite == False:
        file = open(f"{pwpath}/saved.txt", "a")
        file.write(f"\n{usedfor}:\n{generated}")
        file.close()
    elif using_sqlite == True:
        c.execute("INSERT INTO cr VALUES (:name, :created)", {'name': usedfor, 'created': generated})
        conn.commit()
    print(f"{generated} used for \"{usedfor}\" has been copied to clipboard and saved")
    sleep(4)
    os.system("clear")
    main()

def pwinput():
    while True:
        try:
            usedfor = input("Password will be used for?\n> ")
            length = int(input("Length of password?\n> "))
            if length < 8:
                inpt = input("Are you sure? Every site advises against using a password under 8 characters. (y/n)\n> ")
                match inpt.lower():
                    case "y":
                        pass
                    case "n":
                        pwinput()
        except ValueError:
            print("invalid input")
            pwinput()
        else:
            gen(length, usedfor, selected)

if __name__ == '__main__':
    main()
