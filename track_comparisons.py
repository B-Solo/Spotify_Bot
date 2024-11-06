from ascii_magic import AsciiArt
from random import choice
from spreadsheet_playlist import SpreadsheetPlaylist, SpreadsheetTrack



def which_is_better(track1: SpreadsheetTrack, track2: SpreadsheetTrack):
    """
    Returns None if the user breaks out of the loop. Else returns the 'winner'
    which is the first track by default if they're even.
    """
    print_two_tracks(track1, track2)
    x = input(f"Which is better: {track1.name} (1), {track2.name} (2), or are they tied (3)? ")
    if (x != '1' and x != '2' and x != '3'):
        return None
    track1.matchups += 1
    track2.matchups += 1
    if (x == '3'):
        track1.matchups_won += 1
        track2.matchups_won += 1
        return choice([track1, track2])
    if (x == '2'):
        track2.matchups_won += 1
        return track2
    track1.matchups_won += 1
    return track1
    

    


def which_is_worse():
    raise NotImplementedError

def is_this_happy():
    raise NotImplementedError

def is_this_sad():
    raise NotImplementedError


def print_two_tracks(track1: SpreadsheetTrack, track2: SpreadsheetTrack):
    try:
        album_cover1 = AsciiArt.from_url(track1.track.album_cover_url)
        album_cover2 = AsciiArt.from_url(track2.track.album_cover_url)
    except OSError:
        print("Was unable to obtain an album cover.")
    else:
        album_cover1_ascii = album_cover1.to_ascii(columns=64).split("\n")
        album_cover2_ascii = album_cover2.to_ascii(columns=64).split("\n")
        output = list(map(lambda x: f"{x[0]}   {x[1]}", zip(album_cover1_ascii, album_cover2_ascii)))
        print()
        for y in output:
            print(y)
        print("-"*(64+3+64))
        print(f"{track1.name.center(64)}   {track2.name.center(64)}")