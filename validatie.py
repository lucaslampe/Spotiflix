import csv

csvbestand = 'gegevens.csv'


def search(email, naam, bestand):
    for acc in bestand:
        if acc["Gebruikersnaam"].lower() == naam.lower() and acc["Email"].lower() == email.lower():
            return True
    return False


def valideren(naam, email):
    bestand = []
    try:
        f = open(csvbestand, 'r')
        reader = csv.DictReader(f, delimiter=';')
        for i in reader:
            bestand.append(i)
    except BaseException as e:
        print('fout'+str(e))
    finally:
        f.close()
    if not search(email, naam, bestand):
        print("Bestaat niet")
        bestand.append({'Rol': '0', 'Gebruikersnaam': naam, 'Email': email})
    else:
        for j in bestand:
            if j['Email'].lower() == email.lower() and j["Gebruikersnaam"].lower() == naam.lower():
                print("Bestaat wel")
                return j['Rol']
    try:
        f = open(csvbestand, 'w', newline='')
        veldnamen = ['Gebruikersnaam', 'Rol', 'Email']
        writer = csv.DictWriter(f,fieldnames=veldnamen, delimiter=';')

        writer.writeheader()
        for i in bestand:
            writer.writerow(i)
    finally:
        f.close()