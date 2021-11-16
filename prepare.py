import pandas as pd
import requests
from bs4 import BeautifulSoup
from env import api_key
import re


def prepare(jsonList, time):
    df = pd.DataFrame()
    
    for index, data in enumerate(jsonList):
        if (data['info']['frames'][-1]['events'][-1]['timestamp']/60000) >= 20:
            final_d = {}
            kda = get_player_kda(data, time)
            final_d.update(kda)
            final_d.update(get_player_stats(data, time))
            df = df.append(final_d, ignore_index=True)
            print(f"Finished with: {index} of {len(jsonList)}")
        else:
            print(f"Skipping: {index} due to <20 min")
    return df



def get_player_kda(data, time):
    df = pd.DataFrame()
    for index in range(len(data['info']['frames'])):
        for event in data['info']['frames'][index]['events']:
            if event['type'] == 'CHAMPION_KILL':
                df = df.append(event, ignore_index =True)
            

    df.timestamp = df.timestamp / 60_000

    kills_df = df[(df.type== 'CHAMPION_KILL') & (df.timestamp <= time)]

    d = {}
    mylist = []
    for value in kills_df.assistingParticipantIds:
        if type(value) == list:
            for assist in value:
                mylist.append(assist)
    temp = pd.DataFrame(mylist)

    for index, player in enumerate(kills_df.killerId.value_counts().sort_index()):

        # Grabbing kills and saving values to same dictionary
        d['killsplayer_'+str(int(kills_df.killerId.value_counts().sort_index().index[index]))] =\
        kills_df.killerId.value_counts().sort_index().iloc[index]

        # Grabbing deaths and saving values to same dictionary
    for index, player in enumerate(kills_df.victimId.value_counts().sort_index()):
        d['deathsplayer_'+str(int(kills_df.victimId.value_counts().sort_index().index[index]))] =\
        kills_df.victimId.value_counts().sort_index().iloc[index]

        # Grabbing assists and saving values to same dictionary
    for index, player in enumerate(temp[0].value_counts().sort_index()):
        d['assistsplayer_'+str(temp[0].value_counts().sort_index().index[index])] = temp.value_counts().sort_index().iloc[index]

    df = pd.DataFrame()
    for index in range(len(data['info']['frames'])):
        for event in data['info']['frames'][index]['events']:
            if event['type'] == 'ELITE_MONSTER_KILL':
                df = df.append(event, ignore_index =True)
            elif event['type']== 'GAME_END':
                df = df.append(event, ignore_index =True)

    kills_df = df[df.type == 'ELITE_MONSTER_KILL']
    for index, player in enumerate(kills_df[kills_df.monsterType=='DRAGON'].killerTeamId.value_counts().sort_index()):

        # Grabbing dragons and saving values to same dictionary
        d['dragon_team'+str(int(kills_df[kills_df.monsterType=='DRAGON'].killerTeamId.value_counts().sort_index().index[index]))] =\
        kills_df[kills_df.monsterType=='DRAGON'].killerTeamId.value_counts().sort_index().iloc[index]

    for index, player in enumerate(kills_df[kills_df.monsterType=='RIFTHERALD'].killerTeamId.value_counts().sort_index()):

        # Grabbing riftherald and saving values to same dictionary
        d['riftherald_team'+str(int(kills_df[kills_df.monsterType=='RIFTHERALD'].killerTeamId.value_counts().sort_index().index[index]))] =\
        kills_df[kills_df.monsterType=='RIFTHERALD'].killerTeamId.value_counts().sort_index().iloc[index]

    for index, player in enumerate(kills_df[kills_df.monsterType=='BARON_NASHOR'].killerTeamId.value_counts().sort_index()):

        # Grabbing baron and saving values to same dictionary
        d['baron_team'+str(int(kills_df[kills_df.monsterType=='BARON_NASHOR'].killerTeamId.value_counts().sort_index().index[index]))] =\
        kills_df[kills_df.monsterType=='BARON_NASHOR'].killerTeamId.value_counts().sort_index().iloc[index]

    # Grabbing target, winning team
    d['winningTeam'] = int(df[df.type == 'GAME_END'].winningTeam)
    return d

def get_player_stats(data, time):
    player_stats = []

    #Here, each timeframe represents about one minute
    timeframe = data['info']['frames'][time]
    players = timeframe['participantFrames']
    #Now create a dicitonary to hold the players' stats from this timeframe
    players_dict = {}
    for i in range(1, len(players) + 1):
        #Now create a temp dict to store the current players stats
        #Use formatted strings to automatically increment the player label
        temp_dict = {
            f'currentGold_{i}': players[str(i)]['currentGold'],
            f'magicDamageDoneToChampions_{i}': players[str(i)]['damageStats']['magicDamageDoneToChampions'],
            f'physicalDamageDoneToChampions_{i}': players[str(i)]['damageStats']['physicalDamageDoneToChampions'],
            f'trueDamageDoneToChampions_{i}': players[str(i)]['damageStats']['trueDamageDoneToChampions'],
            f'totalDamageDoneToChampions_{i}': players[str(i)]['damageStats']['totalDamageDoneToChampions'],
            f'goldPerSecond_{i}': players[str(i)]['goldPerSecond'],
            f'jungleMinionsKilled_{i}': players[str(i)]['jungleMinionsKilled'],
            f'level_{i}': players[str(i)]['level'],
            f'minionsKilled_{i}': players[str(i)]['minionsKilled'],
            f'timeEnemySpentControlled_{i}': players[str(i)]['timeEnemySpentControlled'],
            f'totalGold_{i}': players[str(i)]['totalGold'],
            f'xp_{i}': players[str(i)]['xp']
            }
        #Now that I have the current players stats, extend it to the overall players_dict
        players_dict.update(temp_dict)
    #Update the players_dict one more time with the timestamp for the timeframe
    players_dict.update({'timestamp' : timeframe['timestamp']})
    #Append the players_dict to the overall player_stats list of dicts
    player_stats.append(players_dict)
    return player_stats[0]