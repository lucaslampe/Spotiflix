__author__ = 'Tjeerd'


#CODE CONTROLEREN
'''
import csv

kaartbestand = 'kaartcodes1.csv'

def kaartje_controleren():
    kaartcode = input('Wat is de code van uw kaartje?: ')
    try:
        f = open(kaartbestand, 'r')
        reader = csv.DictReader(f, delimiter=';')
        tjeerd = False
        for row in reader:
            if row['kaartnummer'] == str(kaartcode):
                tjeerd = True
            else:
                tjeerd = False
        if tjeerd == True:
            print('Uw code klopt, veel plezier met de film')
        elif tjeerd == False:
            print('Uw code klopt niet')
    finally:
        f.close()

kaartje_controleren()

'''