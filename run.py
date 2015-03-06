import lastfm
import logging
import sys
import helpers


def run():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    logging.debug('App Starting up')
    genre_colors = helpers.get_config('Colors')
    last_creds = helpers.get_config('Last_fm')
    logging.info('Genre Colors are: '+str(genre_colors))
    network = lastfm.LastFM(last_creds['user'], last_creds['api_key'], genre_colors)
    current = network.get_now_playing()
    print(current.get_track_tags())
    print(current.color())


if __name__ == '__main__':
    run()
