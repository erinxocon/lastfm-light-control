import lastfm
import logging
import sys
import helpers


def run():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    logging.debug('App Starting up')
    genre_colors = helpers.getConfig('Colors')
    logging.info('Genre Colors are: '+str(genre_colors))
    lastfm.get_current_playing()


if __name__ == '__main__':
    run()