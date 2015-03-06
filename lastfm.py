import logging
import requests
import helpers


def get_current_playing():
    config = helpers.getConfig('Last_fm')

    try:
        user = config['user']
        api_key = config['api_key']
    except KeyError:
        logging.error('User name or api_key invalid.')

    r = requests.get('http://ws.audioscrobbler.com/2.0/'
                     '?method=user.getrecenttracks'
                     '&user='+user +
                     '&api_key='+api_key +
                     '&format=json')

    json_response = r.json()

    try:
        most_recent = json_response['recenttracks']['track'][0]
        logging.debug('Recent Track Found')
    except KeyError as e:
        logging.error('Error, recent track can not be found.', e)
        logging.debug('No recent track found.')
        most_recent = None

    if most_recent.get('@attr'):
        if most_recent.get('@attr').get('nowplaying') == 'true':
            logging.info('Now Playing: {0} - {1}'.format(most_recent['name'],
                         most_recent['artist']['#text']))
            return most_recent
    else:
        logging.info('Music not currently playing.')
        return None
