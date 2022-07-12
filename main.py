import pyclip
import os
import json
import sqlite3
from random import choice
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
        
def key_continue():
    input("Press Enter to continue")
    return

def main():
    choice = input("I would like to:\n1: Generate a new password\n2: Manage .db passwords\n3: Exit\n> ")
    match choice:
        case "1":
            pwinput()
        case "2":
            pwmanage()
        case "3":
            conn.close()
            exit()
        case _:
            print(f"Option \"{choice}\" doesn't exist")
            main()

def save(usedfor, generated):
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
    print(f"Password used for \"{usedfor}\" has been copied to clipboard and saved")
    key_continue()
    if os.name == "posix":
        os.system("clear")
    if os.name == "nt":
         os.system("cls")
    main()

def gen(length):
    generated = ""
    for _ in range(length):
        generated += choice(selected) 
    return generated

def pwinput():
    usedfor = input("Password will be used for?\n> ")
    length = int(input("Length of password?\n> "))
    if length < 8:
        inpt = input("Are you sure? Every site advises against using a password under 8 characters. (y/n)\n> ")
        match inpt.lower():
            case "y":
                pass
            case "n":
                pwinput()
            case _:
                print(f"Option \"{inpt}\" doesn't exist")
    else:
        generated = gen(length) 
        save(usedfor=usedfor, generated=generated)   

def pwmanage():
    def search_pw():
        inpt = input("Password's full or partial name:\n> ")
        c.execute(f"SELECT * FROM cr WHERE name LIKE '%{inpt}%'")
        results = c.fetchall()
        for i in results:
            print(f"Name: {i[0]}\nPassword: {i[1]}\n")

    def delete_pw():
        inpt = input("Password's full name:\n> ")
        c.execute(f"DELETE FROM cr WHERE name LIKE :inpt", {'inpt': inpt})
        print("Deleted")

    def edit_pw():
        def update_name():
            inpt_current = input("Current name:\n> ")
            inpt_new = input("New name:\n> ")
            c.execute("UPDATE cr SET name = :inpt_new WHERE name LIKE :inpt_current", {'inpt_new': inpt_new, 'inpt_current': inpt_current})
        def update_pw():
            inpt = input("Password's full name:\n> ")
            inpt_length = int(input("New password's length?\n> "))
            new_pass = gen(length=inpt_length, selected=selected)
            c.execute("UPDATE cr SET created = :new_pw WHERE name LIKE :inpt", {'new_pw': new_pass, 'inpt': inpt})
    
        inpt_choice = input("Edit\n1:Password's name\n2: Password\n> ")
        match inpt_choice:
            case "1":
                update_name()
            case "2":
                update_pw()
            case _:
                print(f"Option \"{inpt_choice}\" doesn't exist")
        print("Updated")

    input_manage = input("How would you like to manage your passwords?\n1: Search passwords\n2: Delete passwords\n3: Edit passwords\n> ")
    match input_manage:
        case "1":
            search_pw()
        case "2":
            delete_pw()
        case "3":
            edit_pw()
        case _:
            print(f"Option \"{input_manage}\" doesn't exist")
    conn.commit()
    key_continue()
    print("Returning...\n")
    main()

if __name__ == '__main__':
    main()
