from __future__ import print_function
import spotify_handler
import sheets_handler




# To activate virtual environment, do .venv\Scripts\activate


# Given a playlist, and a location of a (vertical) range on a spreadsheet, and possibly a file of rows to ignore,
# compare the track names of the playlist to the rows of the range, adjusting the spreadsheet (or recording
# further rows to ignore) as desired via the command line.
def consolidate_playlist_with_spreadsheet_col(playlist_id, spreadsheet_id, sheet_name, first_cell, approved_rows_file=""):
    
    col, first_row = find_row_col(first_cell)

    spreadsheet_values = get_values_from_spreadsheet(spreadsheet_id, sheet_name + "!" + first_cell + ":" + col + str(first_row + 10000), concatenate=True)
    track_names = get_track_names_from_playlist(playlist_id)

    print(f"Have detected {len(spreadsheet_values)} rows of the spreadsheet, for {len(track_names)} tracks in the playlist")

    # This will ensure we have at least as many spreadsheet spaces as tracks, so that if we add
    # new tracks, the program will let us add them to the spreadsheet
    while(len(spreadsheet_values) < len(track_names)): 
        spreadsheet_values.append("")



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
        pickle.dump(approved_rows, outfile)



def main():
    EVERYTHING_ID = 'https://open.spotify.com/playlist/36d5XdCBocMKCXpFS1JoQ8?si=f0a4d20ecb764313'
    SONGS_2023_ID = 'https://open.spotify.com/playlist/37i9dQZF1Fa1IIVtEpGUcU?si=b409fff09912444d'
    SONGS_2022_ID = 'https://open.spotify.com/playlist/37i9dQZF1F0sijgNaJdgit?si=481888f3f4404b6a'
    SONGS_2021_ID = 'https://open.spotify.com/playlist/37i9dQZF1EUMDoJuT8yJsl?si=83094f9117684fbc'
    SONGS_2020_ID = 'https://open.spotify.com/playlist/37i9dQZF1EMg6nWsb4kEDa?si=1602964d65994708'
    SONGS_2019_ID = 'https://open.spotify.com/playlist/37i9dQZF1EthgUig02pBIz?si=943706dee97d4b82'

    YOUR_TOP_SONGS = [SONGS_2019_ID, SONGS_2020_ID, SONGS_2021_ID, SONGS_2022_ID, SONGS_2023_ID]
    MUSIC_SHEET_ID = '1apQT3YSnxTkZEw0N3PaSpFja7uzbvWJyZ6nHj4bzpN4'
    #consolidate_playlist_with_spreadsheet_col(EVERYTHING_ID, MUSIC_SHEET_ID, 'Ben V3', 'A2', "EverythingSheetDiffs.txt")

    dict = {}
    for year in YOUR_TOP_SONGS:
        for track in get_track_names_from_playlist(year):
            dict[track] = dict[track] + 1 if track in dict else 1

    print(sorted( ((v,k) for k,v in dict.items()), reverse=True)[:20])



    




   
    
    


if __name__ == '__main__':
    main()