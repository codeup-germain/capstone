import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from env import api_key
import time
import re

def get_username(table):
    username_list = []
    for i in range (1,571,6):
        name = str(table[i])
        username = str(re.findall(r'userName=.+?"', name))
        username_list.append(username)
        df = pd.DataFrame(username_list)
        df = df.rename(columns={0:"pro"})
        df['pro'] = df.pro.str.replace("\['userName=","")
        df['pro'] = df.pro.str.replace("+",' ')
        df['pro'] = df.pro.str.replace("\"']",'')
        df = df[~df.pro.str.contains('%')]
        df = df.reset_index()
    return df

def op_gg_webscrape(pages):
    player_names = []
    for i in range(pages + 1):
        url = (f'https://na.op.gg/ranking/ladder/page={i}')
        response = requests.get(url, headers = {'user-agent': 'https://github.com/JaredVahle'})
        soup = BeautifulSoup(response.text)
        table = soup.select('.ranking-table')
        table = table[0]
        table = soup.select('.ranking-table__cell')
        users_df = get_username(table)
        for pro in users_df.pro:
                player_names.append(str(pro))
    return player_names

def get_puuid(name_list,df):
    counter = 0
    for name in name_list:
        print(counter)
        counter += 1
        if counter%50 == 0:
            print('function paused')
            print
            time.sleep(180)
            print('Continue')
            response = requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={api_key}")
            summoner_info = response.json()
            info = {'puuid':summoner_info['puuid'],
                   'username':summoner_info['name']}
            df.append(info,ignore_index = True)
        else:
            response = requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={api_key}")
            summoner_info = response.json()
            if len(summoner_info) > 1:
                info = {'puuid':summoner_info['puuid'],
                       'username':summoner_info['name']}
                df.append(info,ignore_index = True)
            else:
                print(summoner_info)
    return df