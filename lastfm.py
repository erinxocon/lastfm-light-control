import logging
import requests
import helpers


class Track(object):
    """Converts last.fm json response into a nice little object for easy
       querying.  Returns all information about tags, color, artist, and title.
    """
    def __init__(self, lastfm_track, api_key):
        """Set public and private variables"""
        # public vars
        try:
            self.is_playing = lastfm_track['@attr']['nowplaying']
        except:
            self.is_playing = False

        try:
            self.title = lastfm_track['name']
        except:
            self.title = None

        try:
            self.album = lastfm_track['album']['#text']
        except:
            self.album = None

        try:
            self.artist = lastfm_track['artist']['#text']
        except:
            self.artist = None

        try:
            self.track_mbid = lastfm_track['mbid']
        except:
            self.track_mbid = None

        try:
            self.album_mbid = lastfm_track['album']['mbid']
        except:
            self.album_mbid = None

        try:
            self.artist_mbid = lastfm_track['artist']['mbid']
        except:
            self.artist_mbid = None

        # private var
        self._api_key = api_key

    def get_track_tags(self):
        """Returns a sorted list of track tags.  Will try and use the tracks
           mbid (music brainz id), otherwise it will use title and artist"""
        # check to see if there is a music braiz id
        if self.track_mbid:
            url = ('http://ws.audioscrobbler.com/2.0/'
                   '?method=track.gettoptags'
                   '&mbid=' + self.track_mbid +
                   '&api_key='+self._api_key +
                   '&format=json')
        # if no mbid, use artist and title for api call
        else:
            url = ('http://ws.audioscrobbler.com/2.0/'
                   '?method=track.gettoptags'
                   '&artist=' + self.artist +
                   '&track=' + self.title +
                   '&api_key=' + self._api_key +
                   '&format=json')

        # request url and format into dictionary
        r = requests.get(url)
        json = r.json()

        # check to see if the response was an error else no none and log error
        if 'error' not in json.keys():
            return json['toptags']['tag']
        else:
            logging.info('No Tags Found')
            logging.error('Error_Code: {1}. Message: {2}.'.format(
                         json.get('error'), json.get('message')))
            return None


def get_now_playing():
    # get the config for the last fm section
    config = helpers.getConfig('Last_fm')

    # try and get the username and password and log error if it's not working
    try:
        user = config['user']
        api_key = config['api_key']
    except KeyError:
        logging.error('User name or api_key invalid.')

    # request the recent tracks
    r = requests.get('http://ws.audioscrobbler.com/2.0/'
                     '?method=user.getrecenttracks'
                     '&user=' + user +
                     '&api_key=' + api_key +
                     '&format=json')

    # format into dictionary
    json_response = r.json()

    # try and pick out the most recent track
    try:
        most_recent = json_response['recenttracks']['track'][0]
        logging.debug('Recent Track Found')
    except KeyError as e:
        logging.error('Error, recent track can not be found.', e)
        logging.debug('No recent track found.')
        most_recent = None

    # check to see if it's playing
    if most_recent.get('@attr'):
        if most_recent.get('@attr').get('nowplaying') == 'true':
            logging.info('Now Playing: {0} - {1}'.format(most_recent['name'],
                         most_recent['artist']['#text']))
            return most_recent
    else:
        logging.info('Music not currently playing.')
        return None
