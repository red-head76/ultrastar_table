# Copyright

import os
import pathlib
import re
import warnings
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd


class UltrastarTable():
    def __init__(self) -> None:
        self._columns = ['Artist', 'Title', 'Directory', 'Cover', 'Video', 'Commentary']
        self._dtypes = {'Artist': str, 'Title': str, 'Directory': str,
                        'Cover': bool, 'Video': bool, 'Commentary': str}
        # If modifying these scopes, delete the file token.json.
        self._scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.dfs = {"LOCAL": None,
                    "RANGE_SONGLIST": None,
                    "JOINED": None,
                    "RANGE_CHECKLIST": None}
        with open("config.json") as f:
            self.config = json.load(f)

    @staticmethod
    def _set_dtypes(df, dtypes):
        for column in df.columns:
            df[column] = df[column].astype(dtypes[column])

    def read_from_folder(self, path):
        """Reads all song names from a given folder

        Parameters
        ----------
        path : str, pathlib.Path
            path to the folder

        Returns
        -------
        pd.DataFrame
            DataFrame containing all information
        """
        path = pathlib.Path(path)
        candidates = os.listdir(path)
        dfs = []
        for candidate in candidates:
            try:
                files = os.listdir(path / candidate)
                # Extract Artist and Title information from .txt file
                r = re.compile(r".*\.txt$")
                newlist = list(filter(r.match, files))
                if len(newlist) > 1:
                    raise FileNotFoundError("There are multiple .txt files in the" +
                                            f"subfolder {candidate}")
                txtfile = newlist[0]
                with open(path / candidate / txtfile, "r") as f:
                    data = "".join(f.readlines())
                artist = re.search(r"(?<=#ARTIST:).*?(?=\n)", data).group(0)
                title = re.search(r"(?<=#TITLE:).*?(?=\n)", data).group(0)
                # Check if video is available
                cover = any([re.search(r"(.*\.jpg)|(.*\.png)", file) for file in files])
                video = any([re.search(r"(.*\.mp4)|(.*\.avi)", file) for file in files])
                commentary = None

                dfs.append(pd.DataFrame([dict(zip(self._columns, [artist, title, candidate, cover,
                                                                  video, commentary]))]))
            except Exception as e:
                warnings.warn(f"{candidate} had wrong format and was skipped.")
                print(e)
        df = pd.concat(dfs, ignore_index=True)
        self._set_dtypes(df, self._dtypes)
        return df

    def _handle_login(self):
        # This follows the tutorial at https://developers.google.com/sheets/api/quickstart/python
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self._scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self._scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def read_from_spreadsheet(self):
        spreadsheet_id = self.config['SPREADSHEET_ID']
        creds = self._handle_login()
        dfs = {}
        for name in ['RANGE_SONGLIST', 'RANGE_CHECKLIST']:
            range_name = self.config[name]
            try:
                service = build('sheets', 'v4', credentials=creds)
                # Call the Sheets API
                sheet = service.spreadsheets()
                result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                            range=range_name).execute()
                values = result.get('values', [])
                if not values:
                    raise ValueError(f"No data could be retrieved for range {range_name}")
                print("Sucessfully retrieved data for range {range_name}")
                df = pd.DataFrame(values)
                df.columns = df.iloc[0]
                df = df[1:]
                self._set_dtypes(df, self._dtypes)
                df = df.reset_index(drop=True)
                dfs[name] = df
            except HttpError as err:
                print("Request failed")
                print(err)
            except Exception as err:
                print(err)
        return dfs

    def update_dfs(self):
        self.dfs["LOCAL"] = self.read_from_folder(self.config["LOCAL_PATH"])
        self.dfs.update(self.read_from_spreadsheet())

    def write_to_spreadsheet(self):
        creds = self._handle_login()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        body = {"range": self.config["RANGE_SONGLIST"],
                "majorDimension": 'ROWS',
                "values": self.dfs["JOINED"].T.reset_index().T.values.tolist()}
        sheet.values().update(spreadsheetId=self.config["SPREADSHEET_ID"],
                              valueInputOption='RAW',
                              range=self.config["RANGE_SONGLIST"],
                              body=body).execute()

    def merge_dfs(self):
        username = os.getlogin()
        self.dfs["LOCAL"][username] = True
        self.dfs["JOINED"] = self.dfs["RANGE_SONGLIST"].merge(self.dfs["LOCAL"], how='outer')
