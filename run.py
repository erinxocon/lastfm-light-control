import lastfm
import logging
import sys
import helpers
import open_pixel

from time import sleep


def run():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    logging.debug('App Starting up')
    genre_colors = helpers.get_config('Colors')
    last_creds = helpers.get_config('Last_fm')
    logging.info('Genre Colors are: '+str(genre_colors))
    network = lastfm.LastFM(last_creds['user'], last_creds['api_key'], genre_colors)
    old_color = 'White'
    while True:
        current = network.get_now_playing()
        if current.is_playing:
            #color = current.color()
            #logging.info(current.get_artist_tags())
            #logging.info(color)
            rgb = open_pixel.create_color(current.color())
            logging.info(rgb)
            #open_pixel.fade_neopixel(color, old_color, 10, 0.01)
            open_pixel.set_neopixel_color(rgb)
            #old_color = color
        sleep(5)



if __name__ == '__main__':
    run()
