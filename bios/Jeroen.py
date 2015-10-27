__author__ = 'jeroendevries'
#python module voor contact met spotify
import spotipy
import pprint

def spotify(titel):
    """
    :param titel:
    :return:Een URL met een link naar een muziek suggestie op basis van de titel
    """
    spotify = spotipy.Spotify()
    suggestie = spotify.search(q=titel, limit=1)

    return suggestie


pprint.pprint(spotify("Conquest of Paradise"))