__author__ = 'Carlo.R'
import csv
'''
--------globaal te gebruiken variabelen--------------
userdata = een lijst met alle gegevens van de gebruiker
username = gebruikersnaam
email = emailadres van gebruiker
'''
def getdata():
    global userdata
    global email
    userdata = []
    with open('logingegevens.csv', mode='r') as f:
        reader = csv.reader(f)
        for num, row in enumerate(reader):
            if username in row[0]:
                #print(num, row)
                email = row[0].split(";")[3]
def LogIn():
    global loggedin
    global username
    loggedin = 0
    database = open("logingegevens.csv", encoding='utf-8')
    data = (database.read())
    username = input("Username: ")
    password = input("Password: ")
    logindatanormal = ";".join((username,password,"0"))
    logindataprovider = ";".join((username,password,"1"))
    if logindatanormal in data:
        loggedin = 1
        print("Welkom " + username + ". \nFunctie: gebruiker")
        getdata()
        pass
    elif logindataprovider in data:
        loggedin = 2
        print("Welkom, " + username + ". \nFunctie: aanbieder")
        getdata()
        pass
    else:
        loggedin = 0
        print("De gegevens zijn onjuist.")
        LogIn()
    database.close()
LogIn()