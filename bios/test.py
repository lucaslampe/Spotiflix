__author__ = 'Carlo'
from urllib.request import urlopen
import xml.etree.ElementTree as ET
page = urlopen("http://www.filmtotaal.nl/api/filmsoptv.xml?apikey=6i1yqv1xyhumkosv7nk8s9au34e20iuq&dag=27-10-2015&sorteer=0")
#contents = page.read()
tree = ET.parse(page)
root = tree.getroot()
for titel in root.iter('titel'):
    print(titel.text)
    for synopsis in root.iter('synopsis'):
        print(synopsis.text)