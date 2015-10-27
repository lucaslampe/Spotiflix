__author__ = 'jeroendevries'

# python module voor contact met spotify

import spotipy


def spotify(titel):
    """
    :param titel:
    :return:Een URL met een link naar een muziek suggestie op basis van de titel
    """
    spot = spotipy.Spotify()
    suggestie = spot.search(q=titel, limit=1)

    return suggestie['tracks']['items'][0]['album']['external_urls']['spotify']

print(spotify("Conquest of Paradise"))