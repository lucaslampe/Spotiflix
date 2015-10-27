__author__ = 'Carlo'
from urllib.request import urlopen
import xml.etree.ElementTree as ET
import time

filmtotaal_api = '6i1yqv1xyhumkosv7nk8s9au34e20iuq'
datum = time.strftime("%d-%m-%Y")

page = urlopen("http://www.filmtotaal.nl/api/filmsoptv.xml?apikey="+filmtotaal_api+"&dag="+datum+"&sorteer=0")
#contents = page.read()

tree = ET.parse(page)
root = tree.getroot()
for titel in root.iter('titel'):
    print(titel.text)
    for synopsis in root.iter('synopsis'):
        print(synopsis.text)
