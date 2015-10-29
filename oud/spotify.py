__author__ = 'jeroendevries'

# python module voor contact met spotify

import spotipy


def spotify(titel):
    """
    :param titel:
    :return:(URL,Titel nummer, Artiest)
    """
    spot = spotipy.Spotify()

    suggestie1 = spot.search(q=titel + " ", limit=1)
    suggestie2 = spot.search(q=titel + " " + 'From', limit=1)

    try:
        sug1 = (suggestie1['tracks']['items'][0]['external_urls']['spotify'], suggestie1['tracks']['items'][0]['name'], suggestie1['tracks']['items'][0]["artists"][0]['name'])
        sug2 = (suggestie2['tracks']['items'][0]['external_urls']['spotify'], suggestie2['tracks']['items'][0]['name'], suggestie2['tracks']['items'][0]["artists"][0]['name'])
        return (sug1, sug2)
    except:
        print("Helaas geen nummer gevonden")
    return None

# Test code
# song = spotify("Conquest of paradise")
if song is not None:
    for i in range(0,2):
        print(song[i])
