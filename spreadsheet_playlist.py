"""
Provide functionality to handle specifically my music spreadsheet.
"""
from typing import Union
from itertools import zip_longest, starmap
from spreadsheet import Spreadsheet
from colored_str import cyan, green, ColoredStr
from spotify_playlist import Track

class SpreadsheetTrack():
    """
    Class to encapsulate a row of my music spreadsheet.
    """

    _name: ColoredStr
    _track_title: ColoredStr
    matchups : int
    matchups_won : int
    track : Track = None


    def __init__(self, name, difference, score):
        self._name = ColoredStr(name, cyan)
        self._track_title = ColoredStr(difference, green)

        if not score:
            self.matchups = 0
            self.matchups_won = 0
        else:
            self.matchups, self.matchups_won = list(map(int, score.split('/')))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self._name.string = value
        elif isinstance(value, ColoredStr):
            self._name = value
        else:
            raise TypeError


    @property
    def track_title(self):
        return self._track_title

    @track_title.setter
    def track_title(self, value):
        if isinstance(value, str):
            self._track_title.string = value
        elif isinstance(value, ColoredStr):
            self._track_title = value
        else:
            raise TypeError

    def __str__(self):
        output = f"Spreadsheet track with name {self._name} "
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
    tab_name: str
    values_col: str
    deviations_col: str
    score_col: str
    first_row: int

    def __init__(self, spreadsheet_id: str,
                       tab_name: str,
                       values_col: str,
                       deviations_col: Union[str, None],
                       score_col: Union[str, None],
                       first_row: int):

        self.sheet = Spreadsheet(spreadsheet_id)
        self.tab_name = tab_name
        self.values_col = values_col
        self.deviations_col = deviations_col
        self.score_col = score_col
        self.first_row = first_row

        names = self.sheet.get_column(tab_name, values_col, first_row)
        deviations = self.sheet.get_column(tab_name, deviations_col, first_row)
        if score_col:
            scores = self.sheet.get_column(tab_name, score_col, first_row)
        else:
            # Necessary so that the starmap has the right types
            scores = []

        self.items = list(starmap(SpreadsheetTrack,
                         zip_longest(names, deviations, scores)))


    def __len__(self):
        return len(self.items)

    def __iter__(self):
        for item in self.items:
            yield item

    def __getitem__(self, key):
        return self.items[key]

    def __setitem__(self, key, value):
        if not isinstance(value, SpreadsheetTrack):
            raise TypeError("Spreadsheet Playlists items must be "
                            "Spreadsheet Tracks!")
        self.items[key] = value


    def __str__(self):
        return '\n'.join(map(str, self.items))

    def extend(self, new_len):
        self.items.extend([None for _ in range(len(self.items), new_len)])

    def write_to_sheet(self):
        def get_name(x):
            return x.name.string if x else ""
        def get_deviation(x):
            return x.track_title.string if x else ""
        def get_score(x):
            return f"{x.matchups_won}/{x.matchups}" if x else ""

        names = list(map(get_name, self.items))
        deviations = list(map(get_deviation, self.items))
        scores = list(map(get_score, self.items))

        self.set_sheet_column(self.values_col, names)
        self.set_sheet_column(self.deviations_col, deviations)
        if self.score_col:
            self.set_sheet_column(self.score_col, scores)

    def set_sheet_column(self, col_letter, values):
        self.sheet.set_column(self.tab_name,
                              col_letter,
                              self.first_row,
                              values=values)
