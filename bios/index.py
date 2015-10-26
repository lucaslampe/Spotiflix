__author__ = 'Carlo.R'
import csv
#Database = open("logingegevens.csv", encoding='utf-8')
def LogIn():
    global loggedin
    loggedin = 0
    Database = open("logingegevens.csv", encoding='utf-8')
    Data = (Database.read())
    Username = input("Username: ")
    Password = input("Password: ")
    LogIndataNormal = ";".join((Username,Password,"0"))
    LogIndataProvider = ";".join((Username,Password,"1"))
    if LogIndataNormal in Data:
        loggedin = 1
        print("Welkom, " + Username + ". \nFunctie: gebruiker")
        print()
        pass
    elif LogIndataProvider in Data:
        loggedin = 2
        print("Welkom, " + Username + ". \nFunctie: aanbieder")
        print()
        pass
    else:
        loggedin = 0
        print("De gegevens zijn onjuist.")
        LogIn()
    Database.close()
LogIn()