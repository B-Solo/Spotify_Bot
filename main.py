from spotify_playlist import *
from spreadsheet_playlist import *
from colored_str import *




# Given a playlist, and a location of a (vertical) range on a spreadsheet, and possibly a file of rows to ignore,
# compare the track names of the playlist to the rows of the range, adjusting the spreadsheet (or recording
# further rows to ignore) as desired via the command line.
def consolidate_playlist_with_spreadsheet_col(playlist_id: str, 
                                              spreadsheet_id: str, 
                                              tab_name: str, 
                                              values_col: str,
                                              validation_col: str,
                                              score_col: str,
                                              first_row: int):
    

    print("Reading playlist...")
    playlist = Playlist(playlist_id)
    print("Reading spreadsheet...")
    sheet_playlist = SpreadsheetPlaylist(spreadsheet_id,
                                         tab_name,
                                         values_col,
                                         validation_col,
                                         score_col,
                                         first_row)


    print(f"""The playlist of {len(playlist)} items has {len(sheet_playlist)} """
          f"""titles in the spreadsheet.""")

    # Make sure there are at least as items in the spreadsheet values list as
    # there are in the playlist, so we have space for each title to be written
    sheet_playlist.extend(len(playlist))



    # TODO this function needs to change: it should now take a Track()
    # and a SpreadsheetTrack() and determine if they're equivalent    
    def needs_consolidating(tuple):
        _, track_name, sheet_track_name, difference_accepted = tuple
        # bool of the empty list is false
        return (not bool(difference_accepted) and
            track_name.lower() != sheet_track_name.lower())


    # TODO This will need a rewrite based on the above. We can also remove
    # all the colors as they're now encoded into the objects.
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
            validity_vals[entry_num] = "accepted"
        elif response == 't':
            sheet_vals[entry_num] = input("Enter the text for this row: ")
            validity_vals[entry_num] = "accepted"
        else:
            exit_early = True
            break
    
    if not exit_early:
        print("Spreadsheet and playlist are in agreement!")
    print("Updating spreadsheet....")
    sheet_playlist.write_to_sheet()
    

def test_func(spreadsheet_id: str, 
                tab_name: str, 
                values_col: str,
                validation_col: str,
                score_col: str,
                first_row: int):
    sheet_playlist = SpreadsheetPlaylist(spreadsheet_id, 
                                         tab_name, 
                                         values_col, 
                                         validation_col, 
                                         score_col, 
                                         first_row)
    print(sheet_playlist[0])
    print(sheet_playlist[2])



def main():
    colored_str_init()
    EVERYTHING_ID = 'https://open.spotify.com/playlist/36d5XdCBocMKCXpFS1JoQ8?si=f0a4d20ecb764313'
    SONGS_2023_ID = 'https://open.spotify.com/playlist/37i9dQZF1Fa1IIVtEpGUcU?si=b409fff09912444d'
    SONGS_2022_ID = 'https://open.spotify.com/playlist/37i9dQZF1F0sijgNaJdgit?si=481888f3f4404b6a'
    SONGS_2021_ID = 'https://open.spotify.com/playlist/37i9dQZF1EUMDoJuT8yJsl?si=83094f9117684fbc'
    SONGS_2020_ID = 'https://open.spotify.com/playlist/37i9dQZF1EMg6nWsb4kEDa?si=1602964d65994708'
    SONGS_2019_ID = 'https://open.spotify.com/playlist/37i9dQZF1EthgUig02pBIz?si=943706dee97d4b82'

    YOUR_TOP_SONGS = [SONGS_2019_ID, SONGS_2020_ID, SONGS_2021_ID, SONGS_2022_ID, SONGS_2023_ID]
    MUSIC_SHEET_ID = '1apQT3YSnxTkZEw0N3PaSpFja7uzbvWJyZ6nHj4bzpN4'
    #consolidate_playlist_with_spreadsheet_col(EVERYTHING_ID, MUSIC_SHEET_ID, 'Ben V3', 'A', 'B', 2)
    test_func(MUSIC_SHEET_ID, 'Ben V3', 'A', 'B', 'C', 2)


    




   
    
    


if __name__ == '__main__':
    main()