

from tkinter import *
from validatie import *
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
from urllib.request import urlopen
import time
import io
import xmltodict

def antwoord(naam, wachtwoord):
    if valideren(naam,wachtwoord) == True:
        #showinfo(title='popup', message='U bent nu ingelogd als'+naam)
        global window
        window.destroy()
    elif naam == "":
        showinfo(title='popup', message='U heeft geen naam ingevuld')
    elif wachtwoord == "":
        showinfo(title='popup', message='U heeft geen wachtwoord ingevuld')
    else:
        showinfo(title='popup', message='Combinatie van naam en wachtwoord onjuist')

window = Tk()
label = Label(window, text='Voer uw inlognaam in:', )
label2 = Label(window, text='Voer uw wachtwoord in: ',)
naam = Entry(window)
wachtwoord = Entry(window, show="*")

label.grid(row=0, sticky=E)
label2.grid(row=1, sticky=E)

naam.grid(row=0, column=1)
wachtwoord.grid(row=1, column=1)

button = Button(window, text='Voer in', command=(lambda: antwoord(naam.get(),wachtwoord.get())))
button.grid(row=2)
window.mainloop()

def Show_Film_Details(film):
    w = Toplevel()
    w.config(bg="darkred")
    w.geometry("600x600")

    canvas = Canvas(w, width=580, height=580, bg="darkgreen")
    canvas.place(x=10, y=10)

    infoC = Canvas(canvas, width=290, height=300, bg="lightgreen")
    infoC.place(x=280, y=10)

    syncC = Canvas(canvas, width=560, height=180, bg="lightgreen")
    syncC.place(x=10, y=390)

    image = Get_Image(film["cover"], 260, 368)
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

    Label(infoC, text="Titel: "+title, bg="lightgreen", font=("Helvetica", 15)).place(x=10, y=5)
    Label(infoC, text="Jaartal: "+jaar, bg="lightgreen", font=("Helvetica", 13)).place(x=10, y=35)
    Label(infoC, text="Genre: "+genre.replace(":","/"), bg="lightgreen", font=("Helvetica", 13)).place(x=10, y=60)
    Label(infoC, text="Regisseur: "+regisseur, bg="lightgreen", font=("Helvetica", 13)).place(x=10, y=85)
    Label(infoC, text="Duur: "+duur+ " Minuten", bg="lightgreen", font=("Helvetica", 13)).place(x=10, y=125)
    Label(infoC, text="Begintijd: "+time.ctime(int(starttijd)).split(" ")[3][:-3], bg="lightgreen", font=("Helvetica", 13)).place(x=10, y=150)
    Label(infoC, text="Eindtijd: "+time.ctime(int(eindtijd)).split(" ")[3][:-3], bg="lightgreen", font=("Helvetica", 13)).place(x=10, y=175)
    Label(infoC, text="IMDB Rating: "+imdb_rating, bg="lightgreen", font=("Helvetica", 13)).place(x=10, y=215)
    Label(infoC, text="IMDB Votes: "+imdb_votes, bg="lightgreen", font=("Helvetica", 13)).place(x=10, y=240)
    Label(infoC, text="Prijs: €5.-", bg="lightgreen", font=("Helvetica", 13)).place(x=10, y=275)

    Label(syncC, text="Cast: "+cast.replace(":",", "), bg="lightgreen", wraplength=550, justify=LEFT).place(x=10, y=10)
    Label(syncC, text="Synopsis: "+sysnopsis, bg="lightgreen", wraplength=550, justify=LEFT).place(x=10, y=50)

    Button(canvas, text="       Koop kaartje       ", font=("Helvetica", 20), command= lambda f=film: Show_Film_Details(f), bg="darkred", fg="pink").place(x=282, y=325)

    w.mainloop()

def Get_Image(url, w, h):
    image_bytes = urlopen(url).read()
    data_stream = io.BytesIO(image_bytes)
    pil_image = Image.open(data_stream)
    resized_img = pil_image.resize((w, h), Image.ANTIALIAS)
    return ImageTk.PhotoImage(resized_img)

def Get_Movies():
    api_key = 'cg7j7qfbl4p3m5bb60xfxklxlph1uodi'
    xmldata = urlopen(str.format("http://www.filmtotaal.nl/api/filmsoptv.xml?apikey={0}&dag={1}&sorteer=0", api_key, time.strftime("%d-%m-%Y")))
    data = xmltodict.parse(xmldata.read())
    return data["filmsoptv"]


movies_Window = None
movies_Container = None
def Show_All_Films_Page():
    global movies_Window
    movies_Window = Tk()
    movies_Window.config(bg="darkred")
    movies_Window.geometry("1200x600")
    titleLabel = Label(movies_Window, text="De films van "+time.strftime("%d-%m-%Y")+":", bg="lightgreen")
    titleLabel.place(x=10,y=10)

    if(len(todaysMovies) > 1):
        Button(movies_Window, text="Vorige pagina", command= lambda : Next_Page(-1), bg="darkgreen", fg="lightgreen").place(x=10, y=565)
        Button(movies_Window, text="Volgende pagina", command= lambda : Next_Page(1), bg="darkgreen", fg="lightgreen").place(x=1093, y=565)

    Create_Films()
    movies_Window.mainloop()

def Create_Films():
    global movies_Container
    if(movies_Container is not None):
        movies_Container.destroy()

    movies_Container = Canvas(movies_Window, width=1180, height=500, bg="green")
    movies_Container.place(x=10, y=50)

    i = 0
    global Page_Index
    for film in todaysMovies[Page_Index]:
        c = Canvas(movies_Container, width=224, height=480, bg="lightgreen")
        c.place(x=(i * 234) + 10, y=10)
        image = Get_Image(film["cover"], 204, 288)
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

        Button(c, text="Compleet overzicht", command= lambda f=film: Show_Film_Details(f), bg="darkgreen", fg="lightgreen").place(x=10, y=450)

        i += 1


todaysMovies = [[]]
def Parse_Films():
    index = 0
    i = 0
    global todaysMovies
    data = Get_Movies()
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
    Create_Films()

Parse_Films()
Show_All_Films_Page()