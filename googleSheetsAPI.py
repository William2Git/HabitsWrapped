# os is built-in python module that lets you interact with things related to your operating system
import os.path

# request class allows us to refresh an expired access token
from google.auth.transport.requests import Request
# Credentials object has authentication information that gives us access to authentication info 
from google.oauth2.credentials import Credentials
# InstalledAppFlow is the OAuth part allows users to let Google give Python credentials
from google_auth_oauthlib.flow import InstalledAppFlow
# build() builds a connection/interface to Google API
from googleapiclient.discovery import build
# Httperror allows us to catch errors from Google Sheets API
from googleapiclient.errors import HttpError

# scopes defines the permission that the user needs to give to use this app
# for me, i put read and write
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_values(spreadsheet_id, range_name):
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
    
  # checks if the file exists (credentials already exist)
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    # checks if expired credentials can be refreshed
    if creds and creds.expired and creds.refresh_token:
      # uses refresh token to get a new one
      creds.refresh(Request())
    else:
      # if no refresh token, we will get a new token through OAuth login
      # this loads credentials.json, which has information about my specific Google project
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      # perform OAuth login
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
        
  # pylint: disable=maybe-no-member
  try:
    service = build("sheets", "v4", credentials=creds)

    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=range_name)
        .execute()
    )
    rows = result.get("values", [])
    print(f"{len(rows)} rows retrieved")
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error

# main function
if __name__ == "__main__":
  # Pass: spreadsheet_id, and range_name
  get_values("19SLHheAlCR8XxFji3jmO87LHzbh-ykUEbJzTgji9jEA", "B2:B6")