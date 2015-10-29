__author__ = 'Tjeerd'

import csv


klantnaam = 'klantcodesaanbieder1.csv'


#KAARTCODE CONTROLEREN
def kaartje_controleren():
    kaartcode = input('Wat is de code van uw kaartje?: ')
    try:
        f = open(klantnaam, 'r')
        reader = csv.DictReader(f, delimiter=';')
        tjeerd = False
        for row in reader:
            if row['kaartcode'] == str(kaartcode):
                tjeerd = True
        if tjeerd == True:
            print('Uw code klopt, veel plezier met de film')
        elif tjeerd == False:
            print('Uw code klopt niet')
    finally:
        f.close()





#KLANTEN VAN 1 AANBIERDER CONTROLEREN
def klanten_overzicht():
    try:
        k = open(klantnaam, 'r')
        reader = csv.DictReader(k, delimiter=';')
        for row in reader:
            print(row['klantnaam'], end=' - ')
            print(row['tijd'])
    finally:
        k.close()


def klanten_per_tijd():
    inputtijd = input('Van welke tijd wilt u weten wie er allemaal komen?: ')
    try:
        k = open(klantnaam, 'r')
        reader = csv.DictReader(k, delimiter=';')
        for row in reader:
            if row['tijd'] == inputtijd:
                print(row['klantnaam'], end=' - ')
                print(row['tijd'])
    finally:
        k.close()

klanten_per_tijd()