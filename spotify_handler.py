from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
# Your spotify tokens can be found at 
# https://developer.spotify.com/dashboard/e287922924f04651a63a8476fdfa59eb/settings
from spotify_tokens import *
from abc import ABC, abstractmethod
from datetime import datetime, fromisoformat


# There's just inherently a lot of confusion over the word track.
# It means both:
# 1) an item on a playlist (we sometimes call these Playlist Items)
# 2) a song, as opposed to episode of a podcast.
# We disambiguate in the code using these numbers

class Playlist_Item(ABC):

    name: str
    id: str
    date_added: datetime
    length: int


    @abstractmethod
    def __init__(item_dict: dict):
        """
        The Spotipy API handles Playlist items as dictionaries"""
        pass


class Track(Playlist_Item):

    album_name: str
    album_cover_link: str
    # note to ben - do NOT confuse album artists with the track artists
    artists: list[str]
    # this looks interesting!
    popularity: int
    preview_audio_link: str


    def __init__(item_dict: dict):
        # TODO: implement me!!!
        pass


class Episode(Playlist_Item):
    def __init__(item_dict: dict):
        raise NotImplementedError


class Playlist():
    """
    Class for storing a Spotify playlist.

    Really just a list of Playlist Items with a nice wrapper to extract from
    a Spotify playlist.
    """

    _items : list[Playlist_Item]

    def __init__(self, playlist_id: str):
        self._items = []
        sp = self._get_handle("playlist-read-private")

        # Iterate over the playlist until we have all of the (1) tracks.
        results = sp.playlist_tracks(playlist_id)
        playlist_items = results['items']
        while results['next']:
            results = sp.next(results)
            playlist_items.extend(results['items'])


        # Now populate our list, converting to Playlist Item type
        for item in playlist_items:
            if item["track"]:
                if item["track"]["track"]:
                    self._items.append(Track(item))
                elif item["track"]["episode"]:
                    self._items.append(Episode(item))
                else:
                    raise ValueError("""The playlist item received from Spotipy
                                         is neither a track nor an Episode.""")
                

    def __iter__(self):
        return self._items
    
    def __next__(self):
        for item in self._items:
            yield item

    def _get_handle(self,scope: str) -> Spotify:
        """
        Given a scope, create a handle to access Spotify
        """
        return Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, 
                                                 client_secret= CLIENT_SECRET, 
                                                 redirect_uri=REDIRECT_URL, 
                                                 scope=scope))










if __name__ == "__main__":
    EVERYTHING_ID = 'https://open.spotify.com/playlist/36d5XdCBocMKCXpFS1JoQ8?si=f0a4d20ecb764313'
    Playlist(EVERYTHING_ID)
