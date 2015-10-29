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
import doctest


klantdatafile = 'KlantData.csv'


def clear_database():
    pass


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
    """
    :param uniekecode:
    :return:
    >>> 
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
    w = Tk()
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
    genre = film["genre"] if film["genre"] is not None else "-1"
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
    image_bytes = urlopen(url).read()
    data_stream = io.BytesIO(image_bytes)
    pil_image = Image.open(data_stream)
    resized_img = pil_image.resize((w, h), Image.ANTIALIAS)
    return ImageTk.PhotoImage(resized_img)


def get_movies():
    api_key = 'cg7j7qfbl4p3m5bb60xfxklxlph1uodi'
    xmldata = urlopen(str.format("http://www.filmtotaal.nl/api/filmsoptv.xml?apikey={0}&dag={1}&sorteer=0", api_key, time.strftime("%d-%m-%Y")))
    data = xmltodict.parse(xmldata.read())
    return data["filmsoptv"]


movies_Window = None
movies_Container = None


def show_all_films_page():
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
        genre = film["genre"] if film["genre"] is not None else "-1"
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
    global Page_Index
    Page_Index += index
    if Page_Index < 0:
        Page_Index = len(todaysMovies)-1
    elif Page_Index >= len(todaysMovies):
        Page_Index = 0
    create_films()


def specialcode(title):
    datum = str(time.strftime("%H-%M-%S-%Y"))[::-1].replace("-", "").replace(".", "").replace(":", "").replace(" ", "")
    return (title.lower() + datum[0:10]).replace(" ","")


def Play_Titlesong(song):
    print(song)


def Buy_Ticket(film):

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
    genre = film["genre"] if film["genre"] is not None else "-1"
    regisseur = film["regisseur"] if film["regisseur"] is not None else "-1"
    duur = film["duur"] if film["duur"] is not None else "-"
    starttijd = film["starttijd"] if film["starttijd"] is not None else "-1"
    eindtijd = film["eindtijd"] if film["eindtijd"] is not None else "-1"
    imdb_rating = film["imdb_rating"] if film["imdb_rating"] is not None else "-1"
    imdb_votes = film["imdb_votes"] if film["imdb_votes"] is not None else "-1"

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
    Label(infoC, text="Uw unieke code: "+ specialcode(title).replace(" ",""), bg="white", font=("Helvetica", 13)).place(x=10, y=295)
    songs = get_songlinks(title)
    if songs != None:
        i = 0
        for song in songs:
            Button(infoC, text=str.format("Titlesong suggestie {0}", i+1), command=lambda s=song: webbrowser.open(s)).place(x=(i*130)+10, y=350)
            i += 1

    Label(infoC, text="Uw unieke code: ", bg="white", font=("Helvetica", 13)).place(x=400, y=60)

    uniqueCode = specialcode(title)
    number = pyqrcode.create(uniqueCode)
    #number.png('sketch.png', scale=6) TODO fix this

    load = Image.open('sketch.png')
    render = ImageTk.PhotoImage(load)
    img = Label(ticket, image=render)
    img.image = render
    img.place(x=400, y=100)

    file = csv.writer(open(klantdatafile, "a", newline=''))
    file.writerow([film["zender"], loginName, uniqueCode, time.ctime(int(starttijd)).split(" ")[3][:-3]])

Parse_Films()

window = Tk()
label = Label(window, text='Voer uw inlognaam in:')
label2 = Label(window, text='Voer uw emailadres in: ')

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
window.mainloop()