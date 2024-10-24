import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from typing import Any

class Spreadsheet():

    _sheets_api_handle = None
    _sheet_id = None


    def __init__(self, spreadsheet_id):
        self._sheet_id = spreadsheet_id
        
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = self._get_credentials(scopes)
        service = build('sheets', 'v4', credentials=credentials)
        self._sheets_api_handle = service.spreadsheets().values()




    # See the markdown for an explanation of what this is doing but in short
    # we already have the secret base credentials, and these + user login
    # generate per-user access 'tokens'.
    def _get_credentials(self, scopes):
        creds = None

        if os.path.exists('google_auth_token.json'):
            creds = Credentials.from_authorized_user_file('google_auth_token.json', scopes)
        
        # If credentials are valid, return them
        if creds and not creds.expired:
            return creds
        
        # Else try and refresh them
        try:
            creds.refresh(Request())   
        # This can fail if:
        # 1) the credentials or the refresh token don't exist
        # 2) a refresh hasn't happened in 6 months (google kills the refresh token) 
        # In either case, just do a full regeneration
        except:
            flow = InstalledAppFlow.from_client_secrets_file('google_secret_base_credentials.json', scopes)
            creds = flow.run_local_server(port=0)

        # Save the new credentials for the next run
        with open('google_auth_token.json', 'w') as token:
            print("User token was regenerated")
            token.write(creds.to_json())

        return creds


    def get_value_range(self, tab_name: str, top_left_cell: str, bot_right_cell: str) -> list[list[Any]]:

        try:
            result = self._sheets_api_handle.get(
                        spreadsheetId=self._sheet_id, 
                        range=f"{tab_name}!{top_left_cell}:{bot_right_cell}",
                        ).execute()
        except HttpError as err:
            print(f"Bad request, got error string {err}")
            raise
            
        try:
            return result["values"]
        except KeyError:
            print("No data found.")


    def get_value(self, tab_name: str, location: str) -> Any:
        return self.get_value_range(tab_name, location, location)[0][0]
        



    def change_value(self, tab_name: str, location: str, new_value):
        try:
            self._sheets_api_handle.update(
                                           self._sheet_id,
                                           f"{tab_name}!{location}", 
                                           body = {'values': [[new_value]]}
                                           ).execute()
                
        except HttpError as err:
            print(err)





#given the name of a cell as a string, return the string for the letter code for its column,
#and the integer number for its row
def find_row_col(cell):
    i = 0
    while(cell[i].isalpha()):
        i += 1

    return cell[:i], int(cell[i:])


def main():
    MUSIC_SHEET_ID = '1apQT3YSnxTkZEw0N3PaSpFja7uzbvWJyZ6nHj4bzpN4'
    sheet_name = 'Ben V3'
    first_cell = 'A2'
    col, first_row = find_row_col(first_cell)
    spreadsheet_values = get_values_from_spreadsheet(MUSIC_SHEET_ID, sheet_name + "!" + first_cell + ":" + col + str(first_row + 10000), concatenate=True)
    print(spreadsheet_values)

if __name__ == "__main__":
    main()

