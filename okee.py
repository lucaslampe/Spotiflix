import spotipy
import doctest


def get_songlinks(titel):
    """ Vraagd de links op van de soundtracks die beschikbaar zijn.
    >>> get_songlinks("Man on fire")
    ('https://open.spotify.com/track/5GFfRpAb26A57ao6nxjIIS', 'https://open.spotify.com/track/5IxaywIlITiuADtbdZBiYh')
    >>> get_songlinks("License to Bill")
    Helaas geen nummer gevonden
    >>> get_songlinks("License to Kill")
    ('https://open.spotify.com/track/6GjmlZzBt2FHgLL1x3VMc5', 'https://open.spotify.com/track/1MSqN0iVTQh8115I0Ps7CF')
    """
    spot = spotipy.Spotify()

    suggestie1 = spot.search(q=titel + " ", limit=1)
    suggestie2 = spot.search(q=titel + " " + 'From', limit=1)

    try:
        return suggestie1['tracks']['items'][0]['external_urls']['spotify'], suggestie2['tracks']['items'][0]['external_urls']['spotify']
    except:
        print("Helaas geen nummer gevonden")
    return None

doctest.testmod()
