"""
Provide a variety of helpers to manage my Spotify playlist spreadsheet.
"""
from random import choice

from ascii_magic import AsciiArt

from spotify_playlist import Playlist, Track
from spreadsheet_playlist import SpreadsheetPlaylist, SpreadsheetTrack
from colored_str import color_user_input, Fore, colored_str_init
import ids




def consolidate_playlist_with_spreadsheet(playlist: Playlist,
                                          sheet_playlist: SpreadsheetPlaylist):
    """
    Makes a spreadsheet consistent with a playlist.

    In particular, compares the names of songs given in the values_col against
    the track names in the playlist (allowing for any discrepancies listed)
    in the deviations_col, and resolves conflicts via user input on the CLI
    and writing any updates into the spreadsheet.
    """


    print(f"""The playlist of {len(playlist)} items has {len(sheet_playlist)} """
          f"""titles in the spreadsheet.""")

    # Make sure there are at least as items in the spreadsheet values list as
    # there are in the playlist, so we have space for each title to be written
    sheet_playlist.extend(len(playlist))



    # Tracks in the sheet is right if either its name matches, or the title
    # we've stored for it matches.
    def agree(track: Track, sheet_track: SpreadsheetTrack):
        if not sheet_track or not track:
            return False
        return (track.name.lower() == sheet_track.name.lower()
                or track.name.lower() == sheet_track.track_title.lower())



    entry_nums = range(len(playlist))
    made_change = False
    for entry_num, track, sheet_track in filter(
                                lambda x: not agree(x[1],x[2]),
                                zip(entry_nums, playlist, sheet_playlist)):
        if not sheet_track:
            print(f"--------------------------------------------------------\n"
                  f"Missing entry {entry_num+1} in the sheet.\n"
                  f"Spotify track name is {track.name}.\n"
                  f"Press r to write this name into the sheet, "
                  f"t to type a different entry for this row, or b to break.")
        else:
            print(f"--------------------------------------------------------\n"
                  f"Conflict on entry {entry_num+1}.\n"
                  f"(SHEET) {sheet_track.name} VS {track.name} (SPOTIFY).\n"
                  f"Press r to overwrite sheet, a to accept the difference, "
                  f"t to type a different entry for this row, or b to break.")
        response = input()
        if response != 'b' and not sheet_track:
            # Make a new object if we'll need one
            sheet_track = SpreadsheetTrack("", "", "")
            sheet_playlist[entry_num] = sheet_track
        if response == 'r':
            sheet_track.name = track.name
        elif response == 'a':
            sheet_track.track_title = track.name
        elif response == 't':
            sheet_track.name = color_user_input("Enter the text for this row: ", Fore.CYAN)
            sheet_track.track_title = track.name
        else:
            print("Breaking early...")
            if made_change:
                print("Updating spreadsheet....")
                sheet_playlist.write_to_sheet()
            exit()
        made_change = True


    print("Spreadsheet and playlist are in agreement!")
    for spotify_track, sheet_track in zip(playlist, sheet_playlist):
        sheet_track.track = spotify_track


    if made_change:
        print("Updating spreadsheet....")
        sheet_playlist.write_to_sheet()



def make_comparisons(sheet_playlist: SpreadsheetPlaylist):
    for _ in range(0,5):
        print_two_tracks(choice(sheet_playlist), choice(sheet_playlist))

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



def main():
    """
    main
    """
    colored_str_init()
    print("Reading playlist...")
    playlist = Playlist(ids.EVERYTHING)
    print("Reading spreadsheet...")
    sheet_playlist = SpreadsheetPlaylist(ids.MUSIC_SHEET,
                                         'Ben V3', 'A', 'B', 'C', 2)

    consolidate_playlist_with_spreadsheet(playlist, sheet_playlist)
    make_comparisons(sheet_playlist)




if __name__ == '__main__':
    main()
