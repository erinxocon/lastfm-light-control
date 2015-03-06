import ConfigParser
import logging
import sys
import requests

from colour import Color


def getConfig():
    config = ConfigParser.ConfigParser()
    config.read('Config.ini')
    dict1 = {}
    options = config.options('Colors')
    for option in options:
        try:
            dict1[option] = config.get('Colors', option)
            if dict1[option] == -1:
                logging.debug('skip: %s' % option)
        except:
            logging.error("exception on %s!" % option)
            dict1[option] = None
    return dict1


def get_current_playing():
    r = requests.get('http://ws.audioscrobbler.com/2.0/'
                     '?method=user.getrecenttracks'
                     '&user=erinxocon'
                     '&api_key=afaa22c97ad79f6b8241daf07c751fbb'
                     '&format=json')

    json_response = r.json()

    try:
        most_recent = json_response['recenttracks']['track'][0]
    except KeyError:
        logging.error('Error, recent track can not be found.')
        most_recent = None

    if most_recent['@attr']['nowplaying'] == 'true':
        logging.info('Now Playing: '+most_recent['name'] + ' - ' +
                     most_recent['artist']['#text'])
        return most_recent
    else:
        logging.info('Music not currently playing.')
        return None


def run():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    logging.debug('App Starting up')
    genre_colors = getConfig()
    logging.info('Genre Colors are: '+str(genre_colors))
    get_current_playing()

if __name__ == '__main__':
    run()
