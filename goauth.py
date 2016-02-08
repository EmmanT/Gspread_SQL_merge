import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import os


def auth():
    json_key = json.load(open('Drive - GSpread-4d52fe59b4cb.json'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
    return gspread.authorize(credentials), json_key['leak_tracker']



