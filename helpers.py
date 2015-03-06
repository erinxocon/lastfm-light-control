import ConfigParser
import logging


def getConfig(section):
    config = ConfigParser.ConfigParser()
    config.read('Config.ini')
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                logging.debug('skip: %s' % option)
        except:
            logging.error("exception on %s!" % option)
            dict1[option] = None
    return dict1
