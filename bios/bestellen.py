__author__ = 'Carlo'
import datetime


def specialcode(aanbieder):
    '''
    Maakt een speciale code op bais van de datum
    :param aanbieder:
    :return:
    '''
    code = str(datetime.datetime.today())[::-1].replace("-", "").replace(".", "").replace(":", "").replace(" ", "")
    return str(aanbieder.lower() + code[0:10])
