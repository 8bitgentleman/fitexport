# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import time
from os import path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pprint


pp = pprint.PrettyPrinter(indent=4)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/fitness.activity.read']
# DATA SOURCE
DATA_SOURCE = "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"

START_TIME = "1051700038292387000-"
# test time
# START_TIME = "1577854800000000000-"


def saveJSON(name, data):
    dir_name = path.dirname(path.abspath(__file__))
    file_name = "exports/" + name + "-" + str(int(time.time())) + ".json"
    full_name = path.join(dir_name, file_name)
    with open(full_name, 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)


def main():
    """Shows basic usage of the FIT API.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=54547)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('fitness', 'v1', credentials=creds)

    # Call the Fitness API
    DATA_SET = START_TIME + str(time.time_ns())
    data_sources = service.users().dataSources(). \
        list(userId='me'). \
        execute()

    saveJSON("dataSources", data_sources)

    data_list = []
    for index, s in enumerate(data_sources['dataSource']):

        try:
            dataset = service.users().dataSources(). \
                datasets(). \
                get(userId='me', dataSourceId=s['dataStreamId'], datasetId=DATA_SET). \
                execute()
            data_list.append(dataset)
        except Exception as e:
            print("Error at " + s['dataStreamId'])
            print(e)
    saveJSON("dataset", data_list)


if __name__ == '__main__':
    main()
