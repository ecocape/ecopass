from random import choice
from pyperclip import copy
from time import sleep
from os import getcwd, system, name
import json
#
path = ""
#
letters = "qwertyuiopasdfghjklzxcvbnm"
numbers = "1234567890"
symbols = "~`!@#$%^&*()_-+={[}]|:;'\"<>,.?/\\"

def main():
    try:
        choice = input("i would like to\n1: generate a new password\n")           
        globals()[f"func{choice}"]()
    except KeyError:
        print(f"option \"{choice}\" doesn't exist")
        sleep(2)
        main()

def gen(length, name, selected):
    password = ""
    for _ in range(length):
        password += choice(selected)
    copy(password)
    file = open(f"{path}/passwords.txt", "a")
    file.write(f"\n{name}:\n{password}")
    file.close()
    print(f"{password} used for \"{name}\" has been copied to clipboard and saved")
    sleep(2)
    if name == "nt":
        system("cls")
    else:
        system("clear")
    main()
    
def func1():
    while True:
        try:
            name = input("Password will be used for? ")
            length = int(input("Length of password? "))
            if length < 8:
                return(print(f"bad length ({length} characters)"), func1())     
        except ValueError:
            print("invalid input")
            func1()
        else:
            gen(length, name, selected)
            
selected = ""
if path == "":
    path = getcwd()
cfg = {'includeLetters': True, 'includeNumbers': True, 'includeSymbols': True, 'enableCapitalization': True}
with open(f"{path}/config.json", "w+") as f:
    json.dump(cfg, f)
with open(f"{path}/config.json", "r") as f:
    load_cfg = json.load(f)
    if load_cfg["includeLetters"] == True:
        selected += letters
    if load_cfg["includeNumbers"] == True:
        selected += numbers
    if load_cfg["includeSymbols"] == True:
        selected += symbols
    if load_cfg["enableCapitalization"] == True:
        selected += letters.swapcase()
if __name__ == '__main__':
    main()
