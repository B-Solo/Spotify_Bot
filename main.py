from spotify_playlist import *
from spreadsheet import *
from colorama import Fore, Style
from colorama import init as colorama_init


def green(s):
    return f"{Fore.GREEN}{s}{Style.RESET_ALL}"

def cyan(s):
    return f"{Fore.CYAN}{s}{Style.RESET_ALL}"

# Given a playlist, and a location of a (vertical) range on a spreadsheet, and possibly a file of rows to ignore,
# compare the track names of the playlist to the rows of the range, adjusting the spreadsheet (or recording
# further rows to ignore) as desired via the command line.
def consolidate_playlist_with_spreadsheet_col(playlist_id: str, 
                                              spreadsheet_id: str, 
                                              tab_name: str, 
                                              values_col: str,
                                              validation_col: str,
                                              first_row: int):
    

    print("Reading playlist...")
    playlist = Playlist(playlist_id)
    print("Loading spreadsheet...")
    sheet = Spreadsheet(spreadsheet_id)

    # because these are a column, this comes out as [[val1], [val2], ...]
    print("Reading spreadsheet...")
    sheet_vals = sheet.get_value_range(tab_name,
                                       f"{values_col}{first_row}",
                                       f"{values_col}")
    sheet_vals = [x for [x] in sheet_vals]

    validity_vals = sheet.get_value_range(tab_name,
                                          f"{validation_col}{first_row}",
                                          f"{validation_col}")
    if not validity_vals:
        validity_vals = []

    print(f"""The playlist of {len(playlist)} items has {len(sheet_vals)} """
          f"""titles in the spreadsheet.""")

    # Make sure there are at least as items in the spreadsheet values list as
    # there are in the playlist, so we have space for each title to be written
    sheet_vals.extend(
        ["" for _ in range(len(sheet_vals), len(playlist))]
        )
    validity_vals.extend(
        [[] for _ in range(len(validity_vals), len(playlist))]
    )


    data = zip(range(len(playlist)),
                            map(lambda x : x.name, playlist),
                            sheet_vals,
                            validity_vals)
    
    def needs_consolidating(tuple):
        _, track_name, sheet_track_name, difference_accepted = tuple
        # bool of the empty list is false
        return (not bool(difference_accepted) and
            track_name.lower() != sheet_track_name.lower())

    colorama_init()

    
    # Disparities are either something not being in the sheet, or the name
    # being different in the sheet and the track.
    exit_early = False
    for entry_num, track_name, sheet_track_name, _ in filter(needs_consolidating, data):
        if (sheet_track_name == ""):
            print(f"--------------------------------------------------------\n"
                  f"Missing entry {entry_num+1} in the sheet.\n"
                  f"Spotify track name is {green(track_name)}.\n"
                  f"Press r to write this name into the sheet, "
                  f"t to type a different entry for this row, or b to break.")
        else: 
            print(f"--------------------------------------------------------\n"
                  f"Conflict on entry {entry_num+1}.\n"
                  f"(SHEET) {cyan(sheet_track_name)} VS "
                  f"{green(track_name)} (SPOTIFY).\n"
                  f"Press r to overwrite sheet, a to accept the difference, "
                  f"t to type a different entry for this row, or b to break.")
        response = input()
        if response == 'r':
            sheet_vals[entry_num] = track_name
        elif response == 'a':
            validity_vals[entry_num] = ["accepted"]
        elif response == 't':
            sheet_vals[entry_num] = input("Enter the text for this row: ")
            validity_vals[entry_num] = ["accepted"]
        else:
            exit_early = True
            break
    
    if not exit_early:
        print("Spreadsheet and playlist are in agreement!")
    print("Updating spreadsheet....")
    sheet.set_value_range(tab_name, 
                          f"{values_col}{first_row}", 
                          f"{values_col}",
                          [[x] for x in sheet_vals])
    
    sheet.set_value_range(tab_name,
                          f"{validation_col}{first_row}",
                          f"{validation_col}",
                          validity_vals)
    




def main():
    EVERYTHING_ID = 'https://open.spotify.com/playlist/36d5XdCBocMKCXpFS1JoQ8?si=f0a4d20ecb764313'
    SONGS_2023_ID = 'https://open.spotify.com/playlist/37i9dQZF1Fa1IIVtEpGUcU?si=b409fff09912444d'
    SONGS_2022_ID = 'https://open.spotify.com/playlist/37i9dQZF1F0sijgNaJdgit?si=481888f3f4404b6a'
    SONGS_2021_ID = 'https://open.spotify.com/playlist/37i9dQZF1EUMDoJuT8yJsl?si=83094f9117684fbc'
    SONGS_2020_ID = 'https://open.spotify.com/playlist/37i9dQZF1EMg6nWsb4kEDa?si=1602964d65994708'
    SONGS_2019_ID = 'https://open.spotify.com/playlist/37i9dQZF1EthgUig02pBIz?si=943706dee97d4b82'

    YOUR_TOP_SONGS = [SONGS_2019_ID, SONGS_2020_ID, SONGS_2021_ID, SONGS_2022_ID, SONGS_2023_ID]
    MUSIC_SHEET_ID = '1apQT3YSnxTkZEw0N3PaSpFja7uzbvWJyZ6nHj4bzpN4'
    consolidate_playlist_with_spreadsheet_col(EVERYTHING_ID, MUSIC_SHEET_ID, 'Ben V3', 'A', 'B', 2)

    """dict = {}
    for year in YOUR_TOP_SONGS:
        for track in get_track_names_from_playlist(year):
            dict[track] = dict[track] + 1 if track in dict else 1

    print(sorted( ((v,k) for k,v in dict.items()), reverse=True)[:20])"""



    




   
    
    


if __name__ == '__main__':
    main()