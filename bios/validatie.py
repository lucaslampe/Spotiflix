__author__ = 'jeroendevries'
import csv


def valideren(naam, wachtwoord):
    """
    Geeft True terug als combinatie juist is.
    False indien onjuist.
    Zoekt gegevens op in CSV bestand
    """
    bestand = open("gegevens.csv", "r")
    lezen = csv.DictReader(bestand, delimiter=';')
    gevonden = False
    for row in lezen:
        if row['Gebruikersnaam'] == naam and row['Wachtwoord'] == wachtwoord:
            gevonden = True
    bestand.close()
    return gevonden

