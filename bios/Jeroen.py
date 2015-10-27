__author__ = 'jeroendevries'

# python module voor contact met spotify

import spotipy


def spotify(titel, jaar):
    """
    :param titel:
    :return:Een URL met een link naar een muziek suggestie op basis van de titel
    """
    jaar = str(jaar)
    spot = spotipy.Spotify()

    suggestie1 = spot.search(q=titel + " " + jaar, limit=1)
    suggestie2 = spot.search(q=titel + " " + 'soundtrack', limit=1)
    suggestie3 = spot.search(q=titel + " " + 'soundtrack' + " " + jaar, limit=1)
    try:
      for x in range(0,3):
          y = x
          sug + str(y) = suggestie + y['tracks']['items'][0]['album']['external_urls']['spotify']
    except:
        print("Helaas geen nummer gevonden")

    return (sug1, sug2, sug3)
for i in range(0,3):
    print(spotify("Paradise", 2010)[i])