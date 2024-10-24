from spotify_handler import *
from sheets_handler import *
import pickle
import re




# To activate virtual environment, do .venv\Scripts\activate


# Given a playlist, and a location of a (vertical) range on a spreadsheet, and possibly a file of rows to ignore,
# compare the track names of the playlist to the rows of the range, adjusting the spreadsheet (or recording
# further rows to ignore) as desired via the command line.
def consolidate_playlist_with_spreadsheet_col(playlist_id, spreadsheet_id, tab_name, first_cell):
    
    col, first_row = find_row_col(first_cell)
    sheet = Spreadsheet(spreadsheet_id)
    playlist = Playlist(playlist_id)

    # because these are a column, this comes out as [[val1], [val2], ...]
    spreadsheet_values = sheet.get_value_range(tab_name,
                                               first_cell,
                                               f"{col}{first_row + 10000}")
    spreadsheet_values = [x for [x] in spreadsheet_values]

    print(f"Have detected {len(spreadsheet_values)} rows of the spreadsheet, for {len(playlist)} tracks in the playlist")

    # Make sure there are at least as items in the spreadsheet values list as
    # there are in the playlist, so we have space for each title to be written
    spreadsheet_values.extend(
        ["" for _ in range(len(spreadsheet_values), len(playlist))]
        )
    
    return spreadsheet_values

    ### TODO: this is HORRIBLE flow. The correct method is to store the
    # altered or agreed upon titles in the spreadsheet_values list, and then
    # once we're done (for whatever reason), write that entire range to the
    # playlist all at once.

    """
    try:
        approved_rows = pickle.load(open(approved_rows_file, 'rb'))
    except:
        approved_rows = set()
    
    for i, (name_in_sheet, track_name) in enumerate(zip(spreadsheet_values, track_names)):
        if re.sub(r'’', r'\'', name_in_sheet.lower()) != track_name.lower() and (i not in approved_rows):
            print("Conflict on entry " + str(i+1) + ":\nIn spreadsheet as:     " + name_in_sheet + ".\nSpotify track name is: " + track_name + 
                  ".\nPress r to overwrite sheet, a to accept the difference, t to type a different entry for this row, or b to break")
            response = input()
            if response == 'r':
                alter_spreadsheet(spreadsheet_id, sheet_name + "!" + col + str(i+2), {'values': [[track_name]]})
            elif response == 'a':
                approved_rows.add(i)
            elif response == 't':
                new_row_text = input("Enter the text for this row:")
                alter_spreadsheet(spreadsheet_id, sheet_name + "!" + col + str(i+2), {'values': [[new_row_text]]})
                approved_rows.add(i)
            else:
                break

    print("No further conflicts.")

    with open(approved_rows_file, 'wb') as outfile:
        pickle.dump(approved_rows, outfile)"""



def main():
    EVERYTHING_ID = 'https://open.spotify.com/playlist/36d5XdCBocMKCXpFS1JoQ8?si=f0a4d20ecb764313'
    SONGS_2023_ID = 'https://open.spotify.com/playlist/37i9dQZF1Fa1IIVtEpGUcU?si=b409fff09912444d'
    SONGS_2022_ID = 'https://open.spotify.com/playlist/37i9dQZF1F0sijgNaJdgit?si=481888f3f4404b6a'
    SONGS_2021_ID = 'https://open.spotify.com/playlist/37i9dQZF1EUMDoJuT8yJsl?si=83094f9117684fbc'
    SONGS_2020_ID = 'https://open.spotify.com/playlist/37i9dQZF1EMg6nWsb4kEDa?si=1602964d65994708'
    SONGS_2019_ID = 'https://open.spotify.com/playlist/37i9dQZF1EthgUig02pBIz?si=943706dee97d4b82'

    YOUR_TOP_SONGS = [SONGS_2019_ID, SONGS_2020_ID, SONGS_2021_ID, SONGS_2022_ID, SONGS_2023_ID]
    MUSIC_SHEET_ID = '1apQT3YSnxTkZEw0N3PaSpFja7uzbvWJyZ6nHj4bzpN4'
    print(consolidate_playlist_with_spreadsheet_col(EVERYTHING_ID, MUSIC_SHEET_ID, 'Ben V3', 'A2'))

    """dict = {}
    for year in YOUR_TOP_SONGS:
        for track in get_track_names_from_playlist(year):
            dict[track] = dict[track] + 1 if track in dict else 1

    print(sorted( ((v,k) for k,v in dict.items()), reverse=True)[:20])"""



    




   
    
    


if __name__ == '__main__':
    main()