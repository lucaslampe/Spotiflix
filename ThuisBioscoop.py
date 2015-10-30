from tkinter import *
from validatie import *
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
from urllib.request import urlopen
import time
import io
import xmltodict
import pyqrcode
import csv
import spotipy
import webbrowser
import png
import doctest



klantdatafile = 'KlantData.csv'


def get_songlinks(titel):
    """ Vraagd de links op van de soundtracks die beschikbaar zijn.
    >>> get_songlinks("Man on fire")
    ('https://open.spotify.com/track/5GFfRpAb26A57ao6nxjIIS', 'https://open.spotify.com/track/5IxaywIlITiuADtbdZBiYh')
    >>> get_songlinks("License to Bill")
    Helaas geen nummer gevonden
    >>> get_songlinks("License to Kill")
    ('https://open.spotify.com/track/6GjmlZzBt2FHgLL1x3VMc5', 'https://open.spotify.com/track/1MSqN0iVTQh8115I0Ps7CF')
    """
    spot = spotipy.Spotify()

    suggestie1 = spot.search(q=titel + " ", limit=1)
    suggestie2 = spot.search(q=titel + " " + 'From', limit=1)

    try:
        return suggestie1['tracks']['items'][0]['external_urls']['spotify'], suggestie2['tracks']['items'][0]['external_urls']['spotify']
    except:
        print("Helaas geen nummer gevonden")
    return None


def controleren_in_database(uniekecode):
    """ De aanbieder controleert de code van de bezoeker, deze geeft een popup scherm met een mededeling.
    >>> controleren_in_database("De Code Is Correct!")
    De Code Is Correct!
    """
    print(uniekecode)
    tjeerd = False
    bestand = []
    try:
        f = open(klantdatafile, 'r')
        reader = csv.DictReader(f, delimiter=',')
        for i in reader:
            bestand.append(i)
    finally:
        f.close()

    for i in bestand:
        if i['kaartcode'] == str(uniekecode):
            tjeerd = True
    if tjeerd:
        showinfo(title='', message='De Code Is Correct!')

        #REMOVE PERSON WITH EVERY INFO FROM FILE
        file = open(klantdatafile)
        data = file.readlines()
        file.close()

        writablefile = open(klantdatafile, "w")
        for row in data:
            if not str(uniekecode) == row.split(",")[2]:
                writablefile.write(row)
        writablefile.close()

    elif not tjeerd:
        showinfo(title='', message='De Code Is Incorrect!')


def klanten_overzicht():
    """ Functie dat aan de aanbieder laat zien hoelaat, wie en hoeveel mensen er aanwezig zijn bij zijn film(s).
    Kan hiervan geen doctest uitvoeren, omdat de klanten steeds per keer verschillen.
    """
    try:
        global loginName
        k = open(klantdatafile, 'r')
        reader = csv.DictReader(k, delimiter=',')
        klantenismooi = ''
        for row in reader:
            print(row["zender"].lower(),  loginName.lower())
            if row["zender"].lower() == loginName.lower():
                klantenismooi += row['klantnaam'] + ' - ' + row['tijd'] + '\n'
        return klantenismooi
    finally:
        k.close()


def open_aanbieder_interface():
    """ Opent de interface voor de aanbieders.
    Omdat een deel van de inhoud die weergegeven wordt per aanbieder en per moment verschillend is, is de output niks anders dan een error.
    >>> open_aabieder_interface()
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
    NameError: name 'open_aabieder_interface' is not defined

    """
    w = Tk()
    w.wm_title('Overzicht')
    w.config(bg="darkred")
    w.geometry("600x400")

    big_c = Canvas(w, width=580, height=380, bg="darkgreen")
    big_c.place(x=10, y=10)

    first_c = Canvas(big_c, width=275, height=360, bg="lightgreen")
    first_c.place(x=10, y=10)
    secondC = Canvas(big_c, width=275, height=360, bg="lightgreen")
    secondC.place(x=295, y=10)

    Label(first_c, text='Hieronder kunt u alle gegevens vinden:', bg="lightgreen").place(x=10, y=10)
    Label(first_c, text='Alle bezoekers + tijden:', bg="lightgreen").place(x=10, y=30)
    Label(first_c, text=klanten_overzicht(), bg="lightgreen", justify=LEFT).place(x=10, y=50)
    Label(secondC, text='Voer de unieke code in:', bg="lightgreen").place(x=10, y=10)
    uniekecode = Entry(secondC)
    uniekecode.place(x=10, y=30)

    Button(secondC, text='Voer in', command=(lambda: controleren_in_database(uniekecode.get()))).place(x=10, y=60)
    window.mainloop()

loginName = ""


def antwoord(naam, email):
    """ Deze functie controleert of er inloggegevens ingevoerd zijn en bepaalt daaruit, via de validatie functie,
    of het scherm voor de aanbieder of klant moet worden geopend.
    >>> antwoord()
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
    TypeError: antwoord() missing 2 required positional arguments: 'naam' and 'email'
    """
    global window
    global loginName
    loginName = naam
    rol = valideren(naam, email)
    if naam == "" and email is not None:
        showinfo(title='', message='U heeft geen naam ingevuld')
    elif email == "" and naam is not None:
        showinfo(title='', message='U heeft geen emailadres ingevuld')
    elif rol == '1':
        print('Het werkt')
        window.destroy()
        open_aanbieder_interface()
    elif rol == '0':
        showinfo(title='', message='U bent nu ingelogd als: '+naam)
        window.destroy()
        show_all_films_page()
    else:
        showinfo(title='', message='U bent nu aangemeld in het systeem. Klik opnieuw op "Voer in" om in te loggen.')


def show_film_details(film):
    """ Deze functie geeft het extra scherm met alle informatie van de geselecteerde film weer.
    >>> show_film_details("Licence to Kill")
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
    TypeError: string indices must be integers
    """
    w = Toplevel()
    w.config(bg="darkred")
    w.geometry("600x600")

    canvas = Canvas(w, width=580, height=580, bg="darkgreen")
    canvas.place(x=10, y=10)

    info_c = Canvas(canvas, width=290, height=300, bg="lightgreen")
    info_c.place(x=280, y=10)

    sync_c = Canvas(canvas, width=560, height=180, bg="lightgreen")
    sync_c.place(x=10, y=390)

    image = get_image(film["cover"], 260, 368)
    img = Label(canvas, image=image)
    img.place(x=10, y=10)
    img.image = image

    title = film["titel"] if film["titel"] is not None else "Geen titel gevonden"
    jaar = film["jaar"] if film["jaar"] is not None else "-1"
    genre = film["genre"] if film["genre"] is not None else "Geen genre gevonden"
    regisseur = film["regisseur"] if film["regisseur"] is not None else "-1"
    cast = film["cast"] if film["cast"] is not None else "Geen cast gevonden"
    duur = film["duur"] if film["duur"] is not None else "-"
    starttijd = film["starttijd"] if film["starttijd"] is not None else "-1"
    eindtijd = film["eindtijd"] if film["eindtijd"] is not None else "-1"
    imdb_rating = film["imdb_rating"] if film["imdb_rating"] is not None else "-1"
    imdb_votes = film["imdb_votes"] if film["imdb_votes"] is not None else "-1"
    sysnopsis = film["synopsis"] if film["synopsis"] is not None else "-1"

    Label(info_c, text="Titel: "+title, bg="lightgreen", font=("Helvetica", 15)).place(x=10, y=5)
    Label(info_c, text="Jaartal: "+jaar, bg="lightgreen", font=("Helvetica", 13)).place(x=10, y=35)
    Label(info_c, text="Genre: "+genre.replace(":","/"), bg="lightgreen", font=("Helvetica", 13)).place(x=10, y=60)
    Label(info_c, text="Regisseur: "+regisseur, bg="lightgreen", font=("Helvetica", 13)).place(x=10, y=85)
    Label(info_c, text="Duur: "+duur+ " Minuten", bg="lightgreen", font=("Helvetica", 13)).place(x=10, y=125)
    Label(info_c, text="Begintijd: "+time.ctime(int(starttijd)).split(" ")[3][:-3], bg="lightgreen", font=("Helvetica", 13)).place(x=10, y=150)
    Label(info_c, text="Eindtijd: "+time.ctime(int(eindtijd)).split(" ")[3][:-3], bg="lightgreen", font=("Helvetica", 13)).place(x=10, y=175)
    Label(info_c, text="IMDB Rating: "+imdb_rating, bg="lightgreen", font=("Helvetica", 13)).place(x=10, y=215)
    Label(info_c, text="IMDB Votes: "+imdb_votes, bg="lightgreen", font=("Helvetica", 13)).place(x=10, y=240)
    Label(info_c, text="Prijs: €5.-", bg="lightgreen", font=("Helvetica", 13)).place(x=10, y=275)
    Label(sync_c, text="Cast: "+cast.replace(":",", "), bg="lightgreen", wraplength=550, justify=LEFT).place(x=10, y=10)
    Label(sync_c, text="Synopsis: "+sysnopsis, bg="lightgreen", wraplength=550, justify=LEFT).place(x=10, y=50)

    Button(canvas, text="   Reserveer kaartje   ", font=("Helvetica", 20), command= lambda f=film: Buy_Ticket(f), bg="darkred", fg="pink").place(x=282, y=325)

    w.mainloop()


def get_image(url, w, h):
    """Deze functie zorgt ervoor dat via API de afbeeldingen kunnen worden geopend en weergeven in TKinter.
    >>> get_image()
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
    TypeError: get_image() missing 3 required positional arguments: 'url', 'w', and 'h'
    """
    image_bytes = urlopen(url).read()
    data_stream = io.BytesIO(image_bytes)
    pil_image = Image.open(data_stream)
    resized_img = pil_image.resize((w, h), Image.ANTIALIAS)
    return ImageTk.PhotoImage(resized_img)


def get_movies():
    """ Geeft een complete overzicht met informatie over de film(s).
    >>> get_movies()
    OrderedDict([('@datum', '30-10-2015'), ('film', [OrderedDict([('ft_link', 'http://www.filmtotaal.nl/film.php?id=14188'), ('titel', 'De Brief voor de Koning'), ('jaar', '2008'), ('regisseur', 'Pieter Verhoeff'), ('cast', 'Yannick van de Velde:Kees Boot:Hans Dagelet:Jonathan De Weers:Willem Drieling:Monic Hendrickx'), ('genre', 'Avontuur'), ('land', 'Nederland'), ('cover', 'http://www.filmtotaal.nl/images/covers/ynkq1oxn4a.jpg'), ('tagline', None), ('duur', '110'), ('synopsis', 'De 16-jarige schildknaap Tiuri zet zijn toekomst als ridder op het spel wanneer een stervende ridder hem een opdracht geeft. Hij moet een uiterst geheime brief voor de Koning van Unauwen bezorgen. Zijn avontuurlijke tocht leidt hem door bergen, bossen en dalen, waar het gevaar altijd op de loer ligt. De brief mag beslist niet in verkeerde handen vallen!'), ('ft_rating', '5.9'), ('ft_votes', '13'), ('imdb_id', '0490377'), ('imdb_rating', '5.8'), ('imdb_votes', '899'), ('starttijd', '1446215400'), ('eindtijd', '1446221400'), ('zender', 'NPO3'), ('filmtip', '1')]), OrderedDict([('ft_link', 'http://www.filmtotaal.nl/film.php?id=15366'), ('titel', '2012'), ('jaar', '2009'), ('regisseur', 'Roland Emmerich'), ('cast', 'John Cusack:Amanda Peet:Chiwetel Ejiofor:Thandie Newton:Oliver Platt:Thomas McCarthy'), ('genre', 'Actie:Drama:Sci-Fi:Thriller'), ('land', 'Verenigde Staten:Canada'), ('cover', 'http://www.filmtotaal.nl/images/covers/rgq7hp8eqm.jpg'), ('tagline', 'We Were Warned.'), ('duur', '158'), ('synopsis', 'Een wetenschapper ontdekt in 2009 dat er \x91iets\x92 mis is met de deeltjes die de zon uitstraalt. Dat \x91iets\x92 zal leiden tot een groot aantal allesvernietigende rampen. Die rampen zullen plaatsvinden in het jaar 2012, rond de tijd dat de Maya kalender afloopt. Omdat de grote overheden van de wereld voorkennis hebben, kan men proberen zoveel mogelijk mensen te redden. In alle tumult die ontstaat probeert Jackson Curtis samen met zijn familie de rampen te overleven.'), ('ft_rating', '6.2'), ('ft_votes', '151'), ('imdb_id', '1190080'), ('imdb_rating', '5.8'), ('imdb_votes', '263322'), ('starttijd', '1446233400'), ('eindtijd', '1446244800'), ('zender', 'RTL5'), ('filmtip', '1')]), OrderedDict([('ft_link', 'http://www.filmtotaal.nl/film.php?id=23430'), ('titel', 'Penthouse North'), ('jaar', '2013'), ('regisseur', 'Joseph Ruben'), ('cast', 'Michelle Monaghan:Michael Keaton:Barry Sloane:Andrew W. Walker:Kaniehtiio Horn:Olivier Surprenant'), ('genre', 'Thriller'), ('land', 'Verenigde Staten'), ('cover', 'http://www.filmtotaal.nl/images/covers/ismb2ilauz.jpg'), ('tagline', None), ('duur', None), ('synopsis', 'Achtervolgd door een tragische gebeurtenis uit haar verleden, ontsnapt de fotojournalist Sara Frost aan de wereld in een chique penthouse in New York. Maar de wereld komt haar achterna in de vorm van de wraakzuchtige, sadistische crimineel Hollander die op zoek is naar een fortuin aan gestolen diamanten die verborgen liggen in het appartement. Gevangen en buitengesloten van de wereld moet Sara de kracht vinden om een eindeloze nacht van fysieke en psychische marteling te overleven.'), ('ft_rating', '8'), ('ft_votes', '2'), ('imdb_id', '2055709'), ('imdb_rating', '5.5'), ('imdb_votes', '2841'), ('starttijd', '1446233400'), ('eindtijd', '1446239700'), ('zender', 'RTL8'), ('filmtip', '1')]), OrderedDict([('ft_link', 'http://www.filmtotaal.nl/film.php?id=15516'), ('titel', 'Observe and Report'), ('jaar', '2009'), ('regisseur', 'Jody Hill'), ('cast', 'Seth Rogen:Anna Faris:Ray Liotta:Patton Oswalt:Michael Pe&ntilde;a:Aziz Ansari'), ('genre', 'Komedie'), ('land', 'Verenigde Staten'), ('cover', 'http://www.filmtotaal.nl/images/covers/2bttoe46j2.jpg'), ('tagline', None), ('duur', '106'), ('synopsis', 'Ronnie Barnhardt doet altijd zijn best om het plaatstelijke winkelcentrum veilig te houden. Als het winkelcentrum geteisterd wordt door een zogenaamde flasher komt hij in actie en ziet hij de kans om bij zowel het politiekorps als bij zijn droommeisje in een positief daglicht te komen.'), ('ft_rating', '6'), ('ft_votes', '20'), ('imdb_id', '1197628'), ('imdb_rating', '5.8'), ('imdb_votes', '50632'), ('starttijd', '1446233400'), ('eindtijd', '1446239400'), ('zender', 'SBS9'), ('filmtip', '1')]), OrderedDict([('ft_link', 'http://www.filmtotaal.nl/film.php?id=501'), ('titel', 'Wall Street'), ('jaar', '1987'), ('regisseur', 'Oliver Stone'), ('cast', 'Charlie Sheen:Tamara Tunie:Franklin Cover:Chuck Pfeiffer:John C. McGinley:Hal Holbrook'), ('genre', 'Misdaad:Drama'), ('land', 'Verenigde Staten'), ('cover', 'http://www.filmtotaal.nl/images/covers/6qg5r01uk6.jpg'), ('tagline', 'Every dream has a price.'), ('duur', '125'), ('synopsis', 'Bud Fox is een ambitieuze effectenmakelaar bij een groot kantoor op Wall Street. De nerveuze, pientere jongeman is nog maar twee jaar afgestudeerd, maar het is zijn ambitie zo vlug mogelijk deel uit te maken van de absolute financi&euml;le top van New York. Zijn kruiwagen is de gehaaide beroepsspeculant Gordon Gekko. Bud denkt via de gewiekste speculant Gordon Gekko de perfecte manier naar de top te hebben gevonden.'), ('ft_rating', '7.5'), ('ft_votes', '71'), ('imdb_id', '0094291'), ('imdb_rating', '7.4'), ('imdb_votes', '112674'), ('starttijd', '1446235800'), ('eindtijd', '1446243000'), ('zender', 'Canvas'), ('filmtip', '1')]), OrderedDict([('ft_link', 'http://www.filmtotaal.nl/film.php?id=2744'), ('titel', 'The Frighteners'), ('jaar', '1996'), ('regisseur', 'Peter Jackson'), ('cast', 'Michael J. Fox:Trini Alvarado:Peter Dobson:John Astin:Jeffrey Combs:Dee Wallace'), ('genre', 'Komedie:Fantasy:Horror:Thriller'), ('land', 'Nieuw-Zeeland:Verenigde Staten'), ('cover', 'http://www.filmtotaal.nl/images/covers/x8ia9dj7iz.jpg'), ('tagline', 'No Rest for the Wicked.'), ('duur', '110'), ('synopsis', 'Frank Bannister is een medium dat met de doden kan praten. Helaas gebruikt hij zijn gave voor kleine oplichterijen. Na de dood van zijn vrouw, aan wie hij zijn occulte krachten dankt, heeft Frank zich nooit meer op zijn gemak gevoeld bij de levenden. Dan worden er onverklaarbare moorden gepleegd, waarvan Frank weet dat ze een bovennatuurlijke oorzaak hebben.'), ('ft_rating', '7.1'), ('ft_votes', '56'), ('imdb_id', '0116365'), ('imdb_rating', '7.2'), ('imdb_votes', '65235'), ('starttijd', '1446238800'), ('eindtijd', '1446246900'), ('zender', 'FOX'), ('filmtip', '1')]), OrderedDict([('ft_link', 'http://www.filmtotaal.nl/film.php?id=12387'), ('titel', 'Beerfest'), ('jaar', '2006'), ('regisseur', 'Jay Chandrasekhar'), ('cast', 'M.C. Gainey:Paul Soter:Erik Stolhanske:Cloris Leachman:J&uuml;rgen Prochnow:Cameron Scher'), ('genre', 'Komedie'), ('land', 'Verenigde Staten:Australi&euml;'), ('cover', 'http://www.filmtotaal.nl/images/covers/zqjv21669v.jpg'), ('tagline', 'Brewed in 2006'), ('duur', '110'), ('synopsis', "Twee Amerikaanse broers van Duitse komaf reizen naar Duitsland om hun grootvader te begraven. Ze maken er tevens het jaarlijkse bierfestijn, het 'Oktoberfest' in M&uuml;nchen, mee. De twee stuiten vervolgens op een eeuwenoud geheim gebruik dat het best valt te omschrijven als een 'vechtsport' onder de bierspelletjes."), ('ft_rating', '5.4'), ('ft_votes', '31'), ('imdb_id', '0486551'), ('imdb_rating', '6.3'), ('imdb_votes', '52327'), ('starttijd', '1446239400'), ('eindtijd', '1446247500'), ('zender', 'SBS9'), ('filmtip', '1')]), OrderedDict([('ft_link', 'http://www.filmtotaal.nl/film.php?id=17851'), ('titel', 'The Cabin in the Woods'), ('jaar', '2011'), ('regisseur', 'Drew Goddard'), ('cast', 'Sigourney Weaver:Kristen Connolly:Chris Hemsworth:Anna Hutchison:Fran Kranz:Jesse Williams'), ('genre', 'Horror:Thriller'), ('land', 'Verenigde Staten'), ('cover', 'http://www.filmtotaal.nl/images/covers/k23ikkpwop.jpg'), ('tagline', 'If you hear a strange sound outside... have sex.'), ('duur', '95'), ('synopsis', 'Voor degenen die bekend zijn met het eerdere werk van Joss Whedon en Drew Goddard zullen de kwaliteit en intelligentie van de film niet als verrassing komen. Whedon speelde al eerder met verwachtingen en het horrorgenre in zijn series Buffy the Vampire Slayer en Angel. Hier leerde Goddard voor het eerst de kneepjes van het vak. Meteen vanaf het begin speelt het duo open kaart: de film opent in een groot instituut waar mannen in witte jassen een groots evenement voorbereiden. Welk evenement? Vijf jonge mensen die een weekend in een afgelegen hut in een groot bos gaan doorbrengen.'), ('ft_rating', '6.7'), ('ft_votes', '69'), ('imdb_id', '1259521'), ('imdb_rating', '7'), ('imdb_votes', '252027'), ('starttijd', '1446239700'), ('eindtijd', '1446245400'), ('zender', 'NPO3'), ('filmtip', '1')]), OrderedDict([('ft_link', 'http://www.filmtotaal.nl/film.php?id=26221'), ('titel', 'Black Forest'), ('jaar', '2010'), ('regisseur', 'Gert Steinheimer'), ('cast', 'Johanna Klante:Nikola Kastner:Adrian Topol:Bernhard Bulling:Andreas Hoppe:Hans Joachim Weiser'), ('genre', 'Thriller'), ('land', 'Duitsland'), ('cover', 'http://www.filmtotaal.nl/images/covers/098uubjkah.jpg'), ('tagline', None), ('duur', '79'), ('synopsis', 'Een groep toeristen trekt een magisch bos in en belandt in een dodelijk spel, waarin alle sprookjes werkelijkheid geworden zijn.'), ('ft_rating', '2'), ('ft_votes', '1'), ('imdb_id', '1587668'), ('imdb_rating', '3.4'), ('imdb_votes', '154'), ('starttijd', '1446239700'), ('eindtijd', '1446246000'), ('zender', 'RTL8'), ('filmtip', '0')]), OrderedDict([('ft_link', 'http://www.filmtotaal.nl/film.php?id=27758'), ('titel', 'Sinatra: All or Nothing at All'), ('jaar', '2015'), ('regisseur', None), ('cast', 'Nancy Barbato:Harry Belafonte:Humphrey Bogart:Bing Crosby:Sammy Davis Jr.:Ava Gardner'), ('genre', None), ('land', None), ('cover', 'http://www.filmtotaal.nl/images/covers/bmtr1mr97p.jpg'), ('tagline', None), ('duur', '240'), ('synopsis', 'Sinatra: All or Nothing at All is een persoonlijke blik op het leven, de muziek en carri&egrave;re van de legendairsche entertainer Frank Sinatra.'), ('ft_rating', '0'), ('ft_votes', '0'), ('imdb_id', '3838978'), ('imdb_rating', '7.9'), ('imdb_votes', '402'), ('starttijd', '1446243000'), ('eindtijd', '1446250200'), ('zender', 'Canvas'), ('filmtip', '1')]), OrderedDict([('ft_link', 'http://www.filmtotaal.nl/film.php?id=3500'), ('titel', 'JFK'), ('jaar', '1991'), ('regisseur', 'Oliver Stone'), ('cast', 'Kevin Costner:Tommy Lee Jones:Kevin Bacon:Gary Oldman:Michael Rooker:Jack Lemmon'), ('genre', 'Biografie:Misdaad:Drama:Historisch:Mystery:Thriller'), ('land', 'Verenigde Staten:Frankrijk'), ('cover', 'http://www.filmtotaal.nl/images/covers/gcf8fscuuv.jpg'), ('tagline', "The Story That Won't Go Away"), ('duur', '189'), ('synopsis', 'Officier van justitie Jim Garrison onderneemt enkele jaren na de moord op president John F. Kennedy (1963) verwoede pogingen om aan te tonen dat er meerdere moordenaars waren en dat er wel degelijk sprake was van een samenzwering.'), ('ft_rating', '8'), ('ft_votes', '46'), ('imdb_id', '0102138'), ('imdb_rating', '8'), ('imdb_votes', '107919'), ('starttijd', '1446243300'), ('eindtijd', '1446254100'), ('zender', 'NPO2'), ('filmtip', '1')]), OrderedDict([('ft_link', 'http://www.filmtotaal.nl/film.php?id=13753'), ('titel', 'We Own the Night'), ('jaar', '2007'), ('regisseur', 'James Gray'), ('cast', 'Joaquin Phoenix:Eva Mendes:Danny Hoch:Alex Veadov:Oleg Taktarov:Dominic Colon'), ('genre', 'Misdaad:Drama:Thriller'), ('land', 'Verenigde Staten'), ('cover', 'http://www.filmtotaal.nl/images/covers/40s21ujczx.jpg'), ('tagline', 'One family on opposite sides of the law... Two brothers about to collide.'), ('duur', '117'), ('synopsis', 'Bobby Green (Joaquin Phoenix), de populaire manager van de legendarische nachtclub El Caribe heeft zijn familie de rug toegekeerd. Hij heeft zijn achternaam veranderd en gebroken met de familietraditie om bij de New Yorkse politie te dienen. Voor Bobby is het elke avond feest als hij zijn klanten begroet in zijn nachtclub en danst op discotunes met zijn Portoricaanse vriendin Amada (Eva Mendes). Maar het is 1988 en het dreigt te escaleren binnen de New Yorkse drugshandel. Bobby, die sterke banden heeft met de Russische maffia, komt voor een belangrijke keuze te staan wanneer de levens van zijn broer Joseph (Mark Wahlberg) en vader Burt (Robert Duvall) bedreigd worden. Kiest hij voor het goed of het kwaad?'), ('ft_rating', '7'), ('ft_votes', '32'), ('imdb_id', '0498399'), ('imdb_rating', '6.9'), ('imdb_votes', '70504'), ('starttijd', '1446244200'), ('eindtijd', '1446250800'), ('zender', 'E&eacute;n'), ('filmtip', '1')]), OrderedDict([('ft_link', 'http://www.filmtotaal.nl/film.php?id=23621'), ('titel', "La baie d'Alger"), ('jaar', '2012'), ('regisseur', 'Merzak Allouache'), ('cast', 'Catherine Jacob:Solal Forte:Anthony Sonigo:Margaux Ch&acirc;telier:Khalid Berkouz:Micha&euml;l Abiteboul'), ('genre', 'Drama'), ('land', 'Frankrijk'), ('cover', 'http://www.filmtotaal.nl/images/covers/o7tmbkok3s.jpg'), ('tagline', None), ('duur', '90'), ('synopsis', '1955. Louis, 15 jaar, woont in Algiers bij zijn oma. Op een avond, aan de baai van Algiers, realiseert hij zich dat de wereld waarin hij is opgegroeid verandert en verdwijnt. Het is het begin van de Algerijnse oorlog en voor de tiener, het einde van de onbezorgdheid ...'), ('ft_rating', '0'), ('ft_votes', '0'), ('imdb_id', '1920991'), ('imdb_rating', '6.3'), ('imdb_votes', '29'), ('starttijd', '1446246480'), ('eindtijd', '0'), ('zender', 'TV5'), ('filmtip', '1')]), OrderedDict([('ft_link', 'http://www.filmtotaal.nl/film.php?id=11776'), ('titel', 'Hollywood Homicide'), ('jaar', '2003'), ('regisseur', 'Ron Shelton'), ('cast', 'Harrison Ford:Josh Hartnett:Lena Olin:Bruce Greenwood:Isaiah Washington:Lolita Davidovich'), ('genre', 'Actie:Komedie:Misdaad:Thriller'), ('land', 'Verenigde Staten'), ('cover', 'http://www.filmtotaal.nl/images/covers/h9vggl6xn5.jpg'), ('tagline', 'In Hollywood, no one is who they really want to be.'), ('duur', '116'), ('synopsis', 'Twee detectives onderzoeken de moord op een rap-groep tijdens een optreden. Ze denken dat de beruchte platenbaas Sartain achter de moord zit. De geruchten gaan dat hij in het verleden wel vaker rappers heeft omgebracht die onder hun contract uit wilden komen...'), ('ft_rating', '5.3'), ('ft_votes', '25'), ('imdb_id', '0329717'), ('imdb_rating', '5.3'), ('imdb_votes', '30042'), ('starttijd', '1446249000'), ('eindtijd', '1446255600'), ('zender', 'BBC1'), ('filmtip', '1')]), OrderedDict([('ft_link', 'http://www.filmtotaal.nl/film.php?id=3685'), ('titel', 'Witchfinder General'), ('jaar', '1968'), ('regisseur', 'Michael Reeves'), ('cast', 'Vincent Price:Ian Ogilvy:Rupert Davies:Hilary Heath:Robert Russell:Nicky Henson'), ('genre', 'Biografie:Historisch:Horror'), ('land', 'Verenigd Koninkrijk'), ('cover', 'http://www.filmtotaal.nl/images/covers/bdc9fegcxi.jpg'), ('tagline', "The Year's Most Violent Film! [UK Theatrical]"), ('duur', '86'), ('synopsis', 'Tijdens de Engelse burgeroorlog wordt Matthew Hopkins door Cromwell tot opper-heksenjager benoemd. Hij krijgt een premie voor elke bekentenis die hij aan een heks weet te ontlokken. En daarbij gaat hij niet al te zachtzinnig te werk.'), ('ft_rating', '7'), ('ft_votes', '4'), ('imdb_id', '0063285'), ('imdb_rating', '6.9'), ('imdb_votes', '5994'), ('starttijd', '1446251700'), ('eindtijd', '1446256800'), ('zender', 'BBC2'), ('filmtip', '1')])])])

    """
    api_key = 'cg7j7qfbl4p3m5bb60xfxklxlph1uodi'
    xmldata = urlopen(str.format("http://www.filmtotaal.nl/api/filmsoptv.xml?apikey={0}&dag={1}&sorteer=0", api_key, time.strftime("%d-%m-%Y")))
    data = xmltodict.parse(xmldata.read())
    return data["filmsoptv"]


movies_Window = None
movies_Container = None


def show_all_films_page():
    """ Hierbij wordt de popup weergeven met de films die gekozen kunnen worden.
    """
    global movies_Window
    movies_Window = Tk()
    movies_Window.wm_title("Films")
    movies_Window.config(bg="darkred")
    movies_Window.geometry("1200x600")
    title_label = Label(movies_Window, text="De films van "+time.strftime("%d-%m-%Y")+":", bg="lightgreen")
    title_label.place(x=10,y=10)

    if len(todaysMovies) > 1:
        Button(movies_Window, text="Vorige pagina", command= lambda : Next_Page(-1), bg="darkgreen", fg="lightgreen").place(x=10, y=565)
        Button(movies_Window, text="Volgende pagina", command= lambda : Next_Page(1), bg="darkgreen", fg="lightgreen").place(x=1093, y=565)

    create_films()
    movies_Window.mainloop()


def create_films():
    """ Het is niet mogelijk om hiervan een doctest uit te voeren.
    """
    global movies_Container
    if movies_Container is not None:
        movies_Container.destroy()

    movies_Container = Canvas(movies_Window, width=1180, height=500, bg="green")
    movies_Container.place(x=10, y=50)

    i = 0
    global Page_Index
    for film in todaysMovies[Page_Index]:
        c = Canvas(movies_Container, width=224, height=480, bg="lightgreen")
        c.place(x=(i * 234) + 10, y=10)
        image = get_image(film["cover"], 204, 288)
        img = Label(c, image=image)
        img.place(x=10, y=10)
        img.image = image

        title = film["titel"] if film["titel"] is not None else "-1"
        jaar = film["jaar"] if film["jaar"] is not None else "-1"
        genre = film["genre"] if film["genre"] is not None else "Geen genre gevonden"
        duur = film["duur"] if film["duur"] is not None else "-1"
        starttijd = film["starttijd"] if film["starttijd"] is not None else "-1"
        eindtijd = film["eindtijd"] if film["eindtijd"] is not None else "-1"

        Label(c, text="Titel: "+title, bg="lightgreen").place(x=10, y=310)
        Label(c, text="Jaartal: "+jaar, bg="lightgreen").place(x=10, y=330)
        Label(c, text="Genre: "+genre.replace(":","/"), bg="lightgreen").place(x=10, y=350)
        Label(c, text="Duur: "+duur+ " Minuten", bg="lightgreen").place(x=10, y=370)
        Label(c, text="Begintijd: "+time.ctime(int(starttijd)).split(" ")[3][:-3], bg="lightgreen").place(x=10, y=390)
        Label(c, text="Eindtijd: "+time.ctime(int(eindtijd)).split(" ")[3][:-3], bg="lightgreen").place(x=10, y=410)
        Label(c, text="Prijs: €5.-", bg="lightgreen").place(x=10, y=430)

        Button(c, text="Compleet overzicht", command= lambda f=film: show_film_details(f), bg="darkgreen", fg="lightgreen").place(x=10, y=450)

        i += 1


todaysMovies = [[]]


def Parse_Films():
    index = 0
    i = 0
    global todaysMovies
    data = get_movies()
    for f in data["film"]:
        i += 1
        if(i > 5):
            todaysMovies.append([])
            index += 1
            i = 0
        todaysMovies[index].append(f)

Page_Index = 0


def Next_Page(index):
    """Deze functie zorgt ervoor dat de knoppen naar de vorige en volgende pagina werken.
    >>> Next_Page()
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
    TypeError: Next_Page() missing 1 required positional argument: 'index'
    """
    global Page_Index
    Page_Index += index
    if Page_Index < 0:
        Page_Index = len(todaysMovies)-1
    elif Page_Index >= len(todaysMovies):
        Page_Index = 0
    create_films()


def specialcode(title):
    """ De functie genereert de unieke code voor de ticket/reservering.
    >>> specialcode()
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
    TypeError: specialcode() missing 1 required positional argument: 'title'
    """

    datum = str(time.strftime("%H-%M-%S-%Y"))[::-1].replace("-", "").replace(".", "").replace(":", "").replace(" ", "")
    return (title.lower() + datum[0:10]).replace(" ","")

def Buy_Ticket(film):
    """ Deze functie zorgt ervoor dat bij de gekozen film een ticket weergegeven wordt.
    >>> Buy_Ticket(Lice)
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
    NameError: name 'Lice' is not defined
    >>> Buy_Ticket("Lice")
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
    TypeError: string indices must be integers
    >>> Buy_Ticket()
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
    TypeError: Buy_Ticket() missing 1 required positional argument: 'film'
    """

    file = csv.DictReader(open(klantdatafile, 'r'), delimiter=',')
    ticketsSold = 0
    for row in file:
        if row["zender"] == film["zender"] and row["tijd"] == time.ctime(int(film["starttijd"])).split(" ")[3][:-3]:
            ticketsSold += 1
        if ticketsSold > 9:
            showinfo(title='Geen kaartjes beschikbaar.', message='Er kunnen geen kaartjes meer gereserveerd worden.')
            return


    ticket = Toplevel()
    ticket.wm_title("Uw bestelling")
    ticket.config(bg="darkred")
    ticket.geometry("800x400")

    infoC = Canvas(ticket, width=780, height=380, bg="white")
    infoC.place(x=10, y=10)

    title = film["titel"] if film["titel"] is not None else "Geen titel gevonden"
    jaar = film["jaar"] if film["jaar"] is not None else "-1"
    genre = film["genre"] if film["genre"] is not None else "Geen genre gevonden"
    regisseur = film["regisseur"] if film["regisseur"] is not None else "-1"
    duur = film["duur"] if film["duur"] is not None else "-"
    starttijd = film["starttijd"] if film["starttijd"] is not None else "-1"
    eindtijd = film["eindtijd"] if film["eindtijd"] is not None else "-1"
    imdb_rating = film["imdb_rating"] if film["imdb_rating"] is not None else "-1"
    imdb_votes = film["imdb_votes"] if film["imdb_votes"] is not None else "-1"

    uniqueCode = specialcode(title)
    number = pyqrcode.create(uniqueCode)
    number.png('sketch.png', scale=6)

    load = Image.open('sketch.png')
    render = ImageTk.PhotoImage(load)
    img = Label(ticket, image=render)
    img.image = render
    img.place(x=400, y=100)

    Label(infoC, text="Titel: "+title, bg="white", font=("Helvetica", 15)).place(x=10, y=5)
    Label(infoC, text="Jaartal: "+jaar, bg="white", font=("Helvetica", 13)).place(x=10, y=35)
    Label(infoC, text="Genre: "+genre.replace(":","/"), bg="white", font=("Helvetica", 13)).place(x=10, y=60)
    Label(infoC, text="Regisseur: "+regisseur, bg="white", font=("Helvetica", 13)).place(x=10, y=85)
    Label(infoC, text="Duur: "+duur+ " Minuten", bg="white", font=("Helvetica", 13)).place(x=10, y=125)
    Label(infoC, text="Begintijd: "+time.ctime(int(starttijd)).split(" ")[3][:-3], bg="white", font=("Helvetica", 13)).place(x=10, y=150)
    Label(infoC, text="Eindtijd: "+time.ctime(int(eindtijd)).split(" ")[3][:-3], bg="white", font=("Helvetica", 13)).place(x=10, y=175)
    Label(infoC, text="IMDB Rating: "+imdb_rating, bg="white", font=("Helvetica", 13)).place(x=10, y=215)
    Label(infoC, text="IMDB Votes: "+imdb_votes, bg="white", font=("Helvetica", 13)).place(x=10, y=240)
    Label(infoC, text="Prijs: €5.-", bg="white", font=("Helvetica", 13)).place(x=10, y=275)
    Label(infoC, text="Uw unieke code: "+ uniqueCode, bg="white", font=("Helvetica", 13)).place(x=10, y=295)
    songs = get_songlinks(title)
    if songs != None:
        i = 0
        for song in songs:
            Button(infoC, text=str.format("Titlesong suggestie {0}", i+1), command=lambda s=song: webbrowser.open(s)).place(x=(i*130)+10, y=350)
            i += 1

    Label(infoC, text="Uw unieke code: ", bg="white", font=("Helvetica", 13)).place(x=400, y=60)

    file = csv.writer(open(klantdatafile, "a", newline=''))
    file.writerow([film["zender"], loginName, uniqueCode, time.ctime(int(starttijd)).split(" ")[3][:-3]])

Parse_Films()

window = Tk()
label = Label(window, text='Voer uw inlognaam in:')
label2 = Label(window, text='Voer uw emailadres in: ')
window.wm_title('Login')

naam = Entry(window)
email = Entry(window)

button1 = Button(window, text='Nieuw Acount', command=lambda: showinfo(title='Nieuw account', message='Als u nog geen acount hebt, vul dan bij het inlogscherm de gewenste gegevens in.'))
button1.grid(row=4, column=0)

label.grid(row=0, sticky=E)
label2.grid(row=1, sticky=E)

naam.grid(row=0, column=1)
email.grid(row=1, column=1)

button = Button(window, text='Voer in', command=lambda: antwoord(naam.get(),email.get()))
button.grid(row=4, column=1)

doctest.testmod()

window.mainloop()