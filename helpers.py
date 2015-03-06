import ConfigParser
import logging
import sys


def get_config(section):
    """reutns a dictionary for a section in the config"""
    config = ConfigParser.ConfigParser()
    config.read('settings.config')
    dict1 = {}
    try:
        options = config.options(section)
    except ConfigParser.NoSectionError as e:
        logging.error('Config: {0}'.format(e))
        sys.exit('Invalid Config file: {0}'.format(e))
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                logging.debug('skip: {0}'.format(option))
        except:
            logging.error("exception on {0}".format(option))
            dict1[option] = None
    return dict1
