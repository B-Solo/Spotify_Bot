"""
Provides functionality for reading a playlist from Spotify
"""

from datetime import datetime
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotify_tokens import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from colored_str import ColoredStr, green

class Track():
    """
    A class to encapsulate the concept of a Spotify Track.
    """

    name: ColoredStr
    id: str
    date_added: datetime
    length: int
    is_podcast: bool

    artists: list[str]

    album_name: str
    album_cover_url: str

    popularity: int
    preview_audio_link: str

    def __init__(self, item_dict: dict):
        """
        Initialise an item by populating its fields.


        The Spotipy API handles Playlist items as dictionaries.
        """
        try:
            self.name = ColoredStr(item_dict["track"]["name"], green)
            self.id = item_dict["track"]["id"]
            self.date_added = datetime.fromisoformat(item_dict["added_at"])
            self.length = item_dict["track"]["duration_ms"] // 1000
            self.is_podcast = item_dict["track"]["type"] == "episode"

            # from what I can see, type seems to be what you call a podcast artist
            def extract_artist(x):
                return x["name"] if x["name"] else x["type"]
            self.artists = list(map(extract_artist, item_dict["track"]["artists"]))

            self.album_name = item_dict["track"]["album"]["name"]
            self.album_cover_url = item_dict["track"]["album"]["images"][0]["url"]

            self.popularity = item_dict["track"]["popularity"]
            self.preview_audio_link = item_dict["track"]["preview_url"]
        except KeyError:
            print(f"Failed to process track: {item_dict}.")
            raise


    def __repr__(self):
        track_dict = {}
        track_dict["track"] = {}
        track_dict["track"]["album"] = {}

        track_dict["track"]["name"] = self.name
        track_dict["track"]["id"] = self.id
        track_dict["added_at"] = datetime.isoformat(self.date_added)
        track_dict["track"]["duration_ms"] = self.length * 1000
        track_dict["track"]["type"] = "episode" if self.is_podcast else "track"

        def wrap_artist(x):
            return {"name" : x}
        track_dict["track"]["artists"] = list(map(wrap_artist, self.artists))

        track_dict["track"]["album"]["name"] = self.album_name
        track_dict["track"]["album"]["images"] = [{"url" : self.album_cover_url}]

        track_dict["track"]["popularity"] = self.popularity
        track_dict["track"]["preview_url"] = self.preview_audio_link

        return f"Track({track_dict})"

    def __str__(self):
        return (f"""{"Podcast:" if self.is_podcast else "Track:"}
                    {self.name} by {', '.join(self.artists)}""")


class Playlist():
    """
    Class for storing a Spotify playlist.

    Really just a list of Playlist Items with a nice wrapper to extract from
    a Spotify playlist.
    """

    items : list[Track]

    def __init__(self, playlist_id: str):
        self.items = []
        sp = self._get_handle("playlist-read-private")

        # Iterate over the playlist until we have all of the (1) tracks.
        results = sp.playlist_tracks(playlist_id)
        playlist_items = results['items']
        while results['next']:
            results = sp.next(results)
            playlist_items.extend(results['items'])


        # Now populate our list, converting to Playlist Item type
        self.items = [Track(item) for item in playlist_items
                        if item["track"]]

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        for item in self.items:
            yield item

    def __getitem__(self, key):
        return self.items[key]

    def __str__(self):
        return '\n'.join(map(str, self.items))

    def _get_handle(self,scope: str) -> Spotify:
        """
        Given a scope, create a handle to access Spotify
        """
        return Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                 client_secret= CLIENT_SECRET,
                                                 redirect_uri=REDIRECT_URI,
                                                 scope=scope))
