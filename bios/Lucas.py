__author__ = 'Lucas'
import time
import untangle

filmtotaal_api = '6i1yqv1xyhumkosv7nk8s9au34e20iuq'
datum = time.strftime("%d-%m-%Y")

url = 'http://www.filmtotaal.nl/api/filmsoptv.xml?apikey='+filmtotaal_api+'&dag='+datum+'&sorteer=0'

obj = untangle.parse(url)

jaar_film = obj.filmsoptv.film['jaar']

print(jaar_film)