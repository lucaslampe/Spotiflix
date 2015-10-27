__author__ = 'Carlo'
import datetime
from index import *
film = "Pirates of the Caribbean"
aanbieder = "Henk"
def specialcode():
    #output = []
    #for i in range(len(username)):
        #output.append(str(ord(username.lower()[i])))
    datum = str(datetime.datetime.today())[::-1].replace("-", "").replace(".", "").replace(":", "").replace(" ", "")
    #namestr = ''.join(output)
    return str(aanbieder.lower() + datum[0:10])
print(specialcode())