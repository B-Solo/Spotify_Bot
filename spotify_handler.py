from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
# Your spotify tokens can be found at 
# https://developer.spotify.com/dashboard/e287922924f04651a63a8476fdfa59eb/settings
from spotify_tokens import *
from datetime import datetime


# There's just inherently a lot of confusion over the word track.
# It means both:
# 1) an item on a playlist (we sometimes call these Playlist Items)
# 2) a song, as opposed to episode of a podcast.
# We disambiguate in the code using these numbers

class Track():

    name: str
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
            self.name = item_dict["track"]["name"]
            self.id = item_dict["track"]["id"]
            self.date_added = datetime.fromisoformat(item_dict["added_at"])
            self.length = item_dict["track"]["duration_ms"] // 1000
            self.is_podcast = item_dict["track"]["type"] == "episode"

            # from what I can see, type seems to be what you call a podcast artist
            extract_artist = lambda x : x["name"] if x["name"] else x["type"]
            self.artists = list(map(extract_artist, item_dict["track"]["artists"]))

            self.album_name = item_dict["track"]["album"]["name"]
            self.album_cover_url = item_dict["track"]["album"]["images"][0]["url"]

            self.popularity = item_dict["track"]["popularity"]
            self.preview_audio_link = item_dict["track"]["preview_url"]
        except KeyError:
            print(f"Failed to process track: {item_dict}.")
            raise

    
    def __repr__(self):
        dict = {}
        dict["track"] = {}
        dict["track"]["album"] = {}

        dict["track"]["name"] = self.name
        dict["track"]["id"] = self.id
        dict["added_at"] = datetime.isoformat(self.date_added)
        dict["track"]["duration_ms"] = self.length * 1000
        dict["track"]["type"] = "episode" if self.is_podcast else "track"

        wrap_artist = lambda x : {"name" : x}
        dict["track"]["artists"] = list(map(wrap_artist, self.artists))

        dict["track"]["album"]["name"] = self.album_name
        dict["track"]["album"]["images"] = [{"url" : self.album_cover_url}]

        dict["track"]["popularity"] = self.popularity
        dict["track"]["preview_url"] = self.preview_audio_link

        return f"Track({dict})"
    
    def __str__(self):
        return (f"""{"Podcast:" if self.is_podcast else "Track:  "}\
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
                        

    def __iter__(self):
        return self
    
    def __next__(self):
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
                                                 redirect_uri=REDIRECT_URL, 
                                                 scope=scope))










if __name__ == "__main__":
    EVERYTHING_ID = 'https://open.spotify.com/playlist/36d5XdCBocMKCXpFS1JoQ8?si=f0a4d20ecb764313'
    pl = Playlist(EVERYTHING_ID)
    top_10 = sorted(pl.items, key=lambda x: x.popularity, reverse=True)[:10]
    print(list(map(lambda x: f"Rating {x.popularity}: {str(x)}", top_10)))
    
