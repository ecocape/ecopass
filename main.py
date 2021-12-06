from random import randint, choice
from pyperclip import copy
from time import sleep
from os import getcwd
secure_mode = False
path = ""
a = "qwertyuiopasdfghjklzxcvbnm1234567890~`!@#$%^&*()_-+={[}]|:;'\"<>,.?/"
a2 = lambda: randint(33, 250)
password = ""

def main():
    try:
        choice = input("i would like to\n1: generate a new password\n")           
        globals()[f"func{choice}"]()
    except KeyError:
        print(f"option \"{choice}\" doesn't exist")
        sleep(2)
        main()
def gen(length, name, path):
    password = ""
    for _ in range(length):
      password += choice(chr(a2()) if secure_mode else a)
      #copy(password)
    try: 
        if path == "":
            path = getcwd()
        v = open(f"{path}/passwords.txt", "a")
        v.write(f"\n{name}:\n{password}")
        v.close()
        print(f"{password} used for \"{name}\" has been copied to clipboard and saved")
    except UnicodeEncodeError:
        print(f"{password} used for \"{name}\" has been copied to clipboard and not saved, set secure_mode to False")
    return(sleep(2), main())
    
    
def func1():
    while True:
        try:
            name = input("Password will be used for? ")
            length = int(input("Length of password? "))
            if length < 8 or length > 100 and secure_mode == False: 
                return(print(f"bad length ({length} characters)"), func1())
            elif length < 14 or length > 100 and secure_mode == True: 
                return(print(f"bad length ({length}) characters)"), func1())       
        except ValueError:
            print("invalid input")
            func1()
        else:
            gen(length, name, path)
            continue

if __name__ == '__main__':
    main()

