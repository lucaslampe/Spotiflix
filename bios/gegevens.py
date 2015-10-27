from tkinter import *
from tkinter.messagebox import showinfo
from bios.validatie import *


def antwoord(naam, wachtwoord):
    if valideren(naam,wachtwoord) == TRUE:
        showinfo(title='popup', message='U bent nu ingelogd als'+naam)
    elif naam == "":
        showinfo(title='popup', message='U heeft geen naam ingevuld')
    elif wachtwoord == ""
        showinfo(title='popup', message='U heeft geen wachtwoord ingevuld')
    else:
        showinfo(title='popup', message='Combinatie van naam en wachtwoord onjuist')



window = Tk()
label = Label(window, text='Voer uw inlognaam in:', )
label2 = Label(window, text='Voer uw wachtwoord in: ',)
naam = Entry(window)
wachtwoord = Entry(window)

label.grid(row=0, sticky=E)
label2.grid(row=1, sticky=E)

naam.grid(row=0, column=1)
wachtwoord.grid(row=1, column=1)

button = Button(window, text='Voer in',
command=(lambda: antwoord(naam.get(),wachtwoord.get())))
button.grid(row=2)
window.mainloop()



aanbieders = {
    'Harderwijk': {'Man on fire': '10.10', 'Man on water': '10.20'},
    'Amersfoort': {'Man on the moon': '10,50', 'Man on ground': '10.15'},
    'Utrecht': {'Scarface': '09,10', 'Scarfuck': '12.10'}
}

def films():

    showinfo(title='popup', message='Deze film kunt u kijken bij bioscoop ')


window = Tk()
label = Label(window, text='Films die vandaag beschikbaar zijn:')
label.grid(row=0)

knop = Checkbutton(window, text='Man on fire',command=antwoord)
knop2= Checkbutton(window, text='Saving Private Ryan',command=antwoord)
knop3= Checkbutton(window, text='Scarface', command=antwoord)

knop.grid(row=1, sticky=W)
knop2.grid(row=2, sticky=W)
knop3.grid(row=3, sticky=W)


window.mainloop()




