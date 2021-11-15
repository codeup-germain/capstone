import pandas as pd
import requests
from bs4 import BeautifulSoup
from env import api_key
import re


def prepare(jsonList):
    for response in jsonList:
        data = response.json()
        df = pd.DataFrame()
        for index in range(len(data['info']['frames'])):
            for event in data['info']['frames'][index]['events']:
                df = df.append(event, ignore_index=True)
        
    return df