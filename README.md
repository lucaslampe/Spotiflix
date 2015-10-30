# Spotiflix
<img src="http://www.hu.nl/includes/img/HU-Platform/hu-logo-nl.svg" width="200">

<img src="https://camo.githubusercontent.com/890acbdcb87868b382af9a4b1fac507b9659d9bf/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c6963656e73652d4d49542d626c75652e737667">
[![Build Status](https://travis-ci.org/lucaslampe/Spotiflix.svg?branch=master)](https://travis-ci.org/lucaslampe/Spotiflix)

<img src="http://i.imgur.com/1vrXua6.png">

## Documentatie

Om **Spotiflix** te kunnen gebruiken moeten er een aantal packages worden geïnstalleerd, namelijk:

* [PyPNG](https://github.com/drj11/pypng)
* [Spotipy](https://github.com/plamere/spotipy)
* [Pillow PIL](https://github.com/python-pillow/Pillow)
* [xmltodict](https://github.com/martinblech/xmltodict)
* [PyQRCode](https://github.com/mnooner256/pyqrcode)

Na deze packages te hebben geïnstalleerd zijn we gereed om het programma uit te voeren.
Dit kunt u doen door dit project te openen in [PyCharm](https://www.jetbrains.com/pycharm/) en `ThuisBioscoop.py` te runnen.

Voor zowel gebruikers als aanbieders is **Spotiflix** een zeer gemakkelijk programma in gebruik.
Een account aan maken is zo gedaan. Voer uw gebruikersnaam en e-mailadres in en u bent klaar om te beginnen.

<p align="center"><img src="http://i.imgur.com/S0e8moW.png"></p>

#### Gebruikers

Als gebruiker krijgt na het inloggen een pop-up met een bevestiging te zien en wordt u door verwezen naar het beginscherm.
Hier vindt u alle films die deze dag te bekijken zijn en waar u zich voor kunt aanmelden.

Kies een film uit en klik op `Compleet overzicht`, waaruit een nieuw scherm volgt met meer informatie over de geselecteerde film. Beslist u deze film te gaan kijken, drukt u simpelweg op `Reserveer kaartje`. Weer springt er een nieuw scherm op waar u uw persoonlijke code / QR-code en nadere gegevens kunt terugvinden.

<p align="center"><img src="http://i.imgur.com/Wm7WqP8.png" width="600"></p>

De unieke functie van **Spotiflix** komt nu aan het licht. Linksonder in het scherm staan (als de film in de *Spotify* database wordt herkent) twee knoppen die u doorverwijzen naar *Spotify*, waar u de soundtrack van de film kunt beluisteren.

#### Aanbieders

Als aanbieder verschijnt na het inloggen een venster met een overzicht van alle bezoekers die bij u uw film komen bekijken. Hier kunt u de persoonlijke code van de bezoeker invoeren. Na het invoeren klikt u op `Voer in`, en heeft u succesvol een bezoeker geregistreerd. De code van deze bezoeker wordt automatisch uit de database verwijderdt.

<p align="center"><img src="http://i.imgur.com/3xreAj8.png" width="600"></p>

## License
```
The MIT License (MIT)

Copyright (c) 2015 Carlo Riedstra, Ferhat Ucar, Jeroen de Vries, Lucas Lampe, Tjeerd Slokker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
