import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import httplib2

def get_values_from_spreadsheet(spreadsheet_id, range_name, concatenate=False):
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = get_credentials(scopes)

    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        if concatenate:
            result = []
            [result.extend(x) for x in values]
            values = result
        
        return values
    
    except HttpError as err:
        print(err)


def alter_spreadsheet(spreadsheet_id, location_name, new_value):
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = get_credentials(scopes)

    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().update(spreadsheetId=spreadsheet_id, range=location_name, valueInputOption='RAW', body = new_value).execute()
        
        return True
    
    except HttpError as err:
        print(err)


    # See the markdown for an explanation of what this is doing but in short
    # we already have the secret base credentials, and these + user login
    # generate per-user access 'tokens'.
def get_credentials(scopes):
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

