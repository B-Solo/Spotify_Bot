from spotify_playlist import *
from spreadsheet_playlist import *
from colored_str import color_user_input, Fore




def consolidate_playlist_with_spreadsheet_col(playlist_id: str, 
                                              spreadsheet_id: str, 
                                              tab_name: str, 
                                              values_col: str,
                                              deviation_col: str,
                                              first_row: int):
    """
    Makes a spreadsheet consistent with a playlist.

    In particular, compares the names of songs given in the values_col against
    the track names in the playlist (allowing for any discrepancies listed)
    in the deviations_col, and resolves conflicts via user input on the CLI
    and writing any updates into the spreadsheet.
    """
    

    print("Reading playlist...")
    playlist = Playlist(playlist_id)
    print("Reading spreadsheet...")
    sheet_playlist = SpreadsheetPlaylist(spreadsheet_id,
                                         tab_name,
                                         values_col,
                                         deviation_col,
                                         None,
                                         first_row)


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
    exit_early = False
    for entry_num, track, sheet_track in filter(
                                lambda x: not agree(x[1],x[2]), 
                                zip(entry_nums, playlist, sheet_playlist)):
        if (not sheet_track):
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
            exit_early = True
            break
    
    if not exit_early:
        print("Spreadsheet and playlist are in agreement!")
    print("Updating spreadsheet....")
    sheet_playlist.write_to_sheet()
    





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
    consolidate_playlist_with_spreadsheet_col(EVERYTHING_ID, MUSIC_SHEET_ID, 'Ben V3', 'A', 'B', 2)


    




   
    
    


if __name__ == '__main__':
    main()