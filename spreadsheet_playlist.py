from itertools import zip_longest, starmap
from typing import Any
from spreadsheet import Spreadsheet
from colored_str import *

class SpreadsheetTrack():
    # Track title is what Spotify calls this track. If this is not set
    # then the name field must match the track title exactly

    name: str
    track_title: str
    matchups : int
    matchups_won : int
    
    def __init__(self, name, difference, score):
        self.name = ColoredStr(name, cyan)
        self.track_title = ColoredStr(difference, green)
        
        if not score:
            self.matchups = 0
            self.matchups_won = 0
        else:
            self.matchups, self.matchups_won = list(map(int, score.split('/')))

    def __str__(self):
        output = f"Spreadsheet track with name {self.name} " 
        if self.track_title:
                output += f"which corresponds to Spotify track {self.track_title} " 
        output += f"which has won {self.matchups_won}/{self.matchups} matchups."
        return output

class SpreadsheetPlaylist():
    """
    Class for storing a playlist written in a spreadsheet.

    Really just a list of SpreadsheetTrack with a nice wrapper to extract these
    from a google sheet
    """

    items : list[SpreadsheetTrack]
    sheet : Spreadsheet

    def __init__(self, spreadsheet_id: str, 
                       tab_name: str, 
                       values_col: str,
                       deviations_col: str,
                       score_col: str,
                       first_row: int):
        
        self.sheet = Spreadsheet(spreadsheet_id)

        names = self.sheet.get_column(tab_name, values_col, first_row)
        deviations = self.sheet.get_column(tab_name, deviations_col, first_row)
        scores = self.sheet.get_column(tab_name, score_col, first_row)
        
        self.items = list(starmap(SpreadsheetTrack, 
                         zip_longest(names, deviations, scores)))
        
                        
    def __len__(self):
        return len(self.items)

    def __iter__(self):
        for item in self.items:
            yield item

    def __getitem__(self, key):
        return self.items[key]
    
    def __str__(self):
        return '\n'.join(map(str, self.items))
    
    def extend(self, new_len):
        self.items.extend([None for _ in range(len(self.items), new_len)])

    # TODO: implement this
    def write_to_sheet(self):
        raise NotImplementedError