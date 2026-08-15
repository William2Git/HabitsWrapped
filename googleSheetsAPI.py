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

# read function
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
    # makes a Google Sheets API v4 client using the OAuth credentials
    # service gives us an interface for interacting w google sheets
    service = build("sheets", "v4", credentials=creds)

    # results is a dictionary with many values, we can access specific info thru specific keys
    # the (parenthesis) just allows us to continue the express onto new lines; it does not affect code
    result = (
      # .values() says i want to work with spreadsheet cell values
      # .execute() sends the api request to google
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=range_name)
        .execute()
    )
    # .get() function for dictionaries, gets the values
    # default value is empty array if no values key
    rows = result.get("values", [])
    print(f"{len(rows)} rows retrieved")
    print(rows)
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error

# write function
def update_values(spreadsheet_id, range_name, value_input_option, _values):
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
      
  try:
    # builds sheets api v4 client using credentials
    service = build("sheets", "v4", credentials=creds)
    
    # values is a 2D list, where each list is the cell values for that row 
    # if one list has 3 cell values, that means i filled out 3 columns in the first rows in the sheet
    # every subsequent list is the next row of cell values
    body = {"values": _values}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )
    print(f"{result.get('updatedCells')} cells updated.")
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error

# main function
if __name__ == "__main__":
  # for reading: Pass: spreadsheet_id, and range_name
  data = get_values("19SLHheAlCR8XxFji3jmO87LHzbh-ykUEbJzTgji9jEA", "B2:B6")
  print(data)
  
  # for writing: Pass: spreadsheet_id,  range_name, value_input_option and  _values
  # range_name can be bigger than _values
  # _values must have a shape/size that fits into range_name, otherwise it errors
  # if range_name is bigger, then the remaining cells are untouched
  
  # value_input_option can be USER_ENTERED or RAW
  # RAW means it gets put in as a string as entered
  # USER_ENTERED means the input will be however it looks like in SHEETS UI
  # so formulas =1+2 become 3, any dates become the date
  
  # _values is a 2D list, where each list is the cell values for that row 
  # if one list has 3 cell values, that means i filled out 3 columns in the first rows in the sheet
  # every subsequent list is the next row of cell values
  update_values(
      "19SLHheAlCR8XxFji3jmO87LHzbh-ykUEbJzTgji9jEA",
      "A2:B3",
      "USER_ENTERED",
      [["1", "2"], ["5", "1"]],
  )
  
  data = get_values("19SLHheAlCR8XxFji3jmO87LHzbh-ykUEbJzTgji9jEA", "A2:A8")
  print(data)
  