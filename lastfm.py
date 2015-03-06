import logging
import requests
import helpers


class Track(object):
    """Converts last.fm json response into a nice little object for easy
       querying.  Returns all information about tags, color, artist, and title.
    """
    def __init__(self, lastfm_track, api_key, genre_colors):
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
        self._genre_colors = genre_colors

    def _list_color_genres(self):
        """Return a list of genres from the configuration file for matching."""
        return map(str.lower, self._genre_colors.keys())

    def _get_tags(self, pay_load):
        """Actually gets the tags"""
        l=[]
        # request url and format into dictionary
        r = requests.get('http://ws.audioscrobbler.com/2.0/', params=pay_load)
        json = r.json()

        # check to see if the response was an error else no none and log error
        if 'error' not in json.keys():
            try:
                tag_list = json['toptags']['tag']
            except KeyError:
                logging.error('Empty tag list')
                return None

            for tag in tag_list:
                l.append(tag.get('name'))

            return l

        else:
            logging.info('No Tags Found')
            logging.error('Error_Code: {0}. Message: {1}.'.format(
                            json.get('error'), json.get('message')))
            return None

    def get_track_tags(self):
        """Returns a sorted list of track tags.  Will try and use the tracks
           mbid (music brainz id), otherwise it will use title and artist"""
        # check to see if there is a music braiz id
        if self.track_mbid:
            pay_load = {'method': 'track.gettoptags',
                        'mbid': self.track_mbid,
                        'api_key': self._api_key,
                        'format': 'json'}
        # if no mbid, use artist and title for api call
        else:
            pay_load = {'method': 'track.gettoptags',
                        'artist=': self.artist,
                        'track': self.title,
                        'api_key': self._api_key,
                        'format': 'json'}

        return self._get_tags(pay_load)

    def get_album_tags(self):
        """Returns a sorted list of album tags.  Will try and use the album
           mbid (music braiz id), otherwuse it will use album, and artist"""
        # check to see if there is a music braiz id
        if self.album_mbid:
            pay_load = {'method': 'album.gettoptags',
                        'mbid': self.album_mbid,
                        'api_key': self._api_key,
                        'format': 'json'}
        # if no mbid, use artist and title for api call
        else:
            pay_load = {'method': 'album.gettoptags',
                        'artist=': self.artist,
                        'album': self.album,
                        'api_key': self._api_key,
                        'format': 'json'}

        return self._get_tags(pay_load)

    def get_artist_tags(self):
        """Returns a sorted list of artist tags.  Will try and use the album
           mbid (music braiz id), otherwuse it will use artist"""
        # check to see if there is a music braiz id
        if self.artist_mbid:
            pay_load = {'method': 'artist.gettoptags',
                        'mbid': self.artist_mbid,
                        'api_key': self._api_key,
                        'format': 'json'}
        # if no mbid, use artist and title for api call
        else:
            pay_load = {'method': 'artist.gettoptags',
                        'artist=': self.artist,
                        'api_key': self._api_key,
                        'format': 'json'}

        return self._get_tags(pay_load)

    def color(self):
        """Returns a color from the defined color genre configurations."""
        l = []
        if self.get_artist_tags() != None:
            for tag in self.get_track_tags():
                if tag.lower() in self._list_color_genres():
                    l.append(tag.lower())
        
        return self._genre_colors[l[0]]


class LastFM(object):
    """Create a LastFM connection"""
    def __init__(self, user, api_key, genre_colors):
        """Accepts user name, api key, and a dictionary of genre color key 
           value pairs."""
        self._user = user
        self._api_key = api_key
        self._genre_colors = genre_colors


    def get_now_playing(self):
        """Returns a lastfm.Track object of the most recently played track.
           use LastFM.is_playing to see if it's currently playing or not"""
        # create requests url params payload
        pay_load = {'method': 'user.getrecenttracks',
                    'user': self._user,
                    'api_key': self._api_key,
                    'format': 'json'}

        # request the recent tracks
        r = requests.get('http://ws.audioscrobbler.com/2.0/', params=pay_load)

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
        if most_recent:
            most_recent = Track(most_recent, self._api_key, self._genre_colors)
            logging.info('Now Playing: {0} - {1}'.format(most_recent.title,
                          most_recent.artist))
            return most_recent
        else:
            logging.info('Music not currently playing.')
            return Nones
