import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split


def train_validate_test_split(df, target, seed=174):
    '''
    This function takes in a dataframe, the name of the target variable
    (for stratification purposes), and an integer for a setting a seed
    and splits the data into train, validate and test. 
    Test is 20% of the original dataset, validate is .30*.80= 24% of the 
    original dataset, and train is .70*.80= 56% of the original dataset. 
    The function returns, in this order, train, validate and test dataframes. 
    '''
    train_validate, test = train_test_split(df, test_size=0.2, 
                                            random_state=seed, 
                                            stratify=df[target])
    train, validate = train_test_split(train_validate, test_size=0.3, 
                                       random_state=seed,
                                       stratify=train_validate[target])
    return train, validate, test 
    

    def get_puuid(name):
    response = requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={api_key}")
    summoner_info = response.json()
    puuid = summoner_info['puuid']
    return puuid


    def get_match_ids(puuid, api_key,url = 'https://americas.api.riotgames.com/'):
    """
    This function takes in a list of puuids and a riot games api key to gather
    and return a list of match ids.
    """
    
    #Create an empty list to store the match ids
    match_list = []


    #Build the query
    query = f'lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=45&api_key={api_key}'

    #Get the response
    response = requests.get(url + query)

    #Check response and leave a status message
    if response.status_code != 200:
        print(f'Something went wrong! Status Code {response.status_code} for puuid {puuid}. Skipping this puuid.\n')

    #Unpack the response as json
    #This should be a list of match ids
    data = response.json()

    #Extend the matches list with the data
    match_list.extend(data)

    return match_list

    def get_match_info(match_list,timeline_data,game_data, api_key, time = 20,url = 'https://americas.api.riotgames.com/'):
    
    #Store the length of the match_ids list in a var
    match_count = len(match_list)
    
    #Loop through each match_id
    for match in match_list:
        
        #Set up timeline url
        timeline_query = f'lol/match/v5/matches/{match}/timeline/?api_key={api_key}'
        
        #Grab timeline json data
        timeline_response = requests.get(url + timeline_query)
        
        #Check response and leave a status message
        if timeline_response.status_code != 200:
            print(f'Something went wrong getting TIMELINE DATA! Status Code {timeline_response.status_code} for match ID: {match}.')
            print(f'Skipping this match ID.\n')
            continue

        #Turn it into json format
        timeline_json = timeline_response.json()
        
        #Append this data to the timeline_data list
        timeline_data.append(timeline_json)

        #Set up game data url
        game_query = f'lol/match/v5/matches/{match}?api_key={api_key}'
        
        #Grab game json data
        game_response = requests.get(url + game_query)
        
        #Check response and leave a status message.
        if game_response.status_code != 200:
            print(f'Something went wrong getting OTHER GAME DATA! Status Code {game_response.status_code} for match ID: {match}.')
            print(f'Skipping this match ID and REMOVING PREVIOUS TIMELINE ENTRY.\n')
            
            #Remove the last entry in the timeline_data list
            timeline_data.pop()
            continue
        
        #Turn it into json format
        game_json = game_response.json()
        
        #Append this data to the game_data list
        game_data.append(game_json)
    
    #Finally, return the prepared df
    #return timeline_data, game_data
    return timeline_data,game_data



def final_acquire(name_list,api_key,i):
    '''
    Takes in a name list from the 2641 names scraped from op.gg, the csv file can be found in my personal file,
    also the i stands for the starting index that the name is taken from
    EXAMPLE: name_list[50:150] the i would be 50 in this situation
    Even if your script gets ended half way though all the json data is saved and will be able to be
    prepared. Just make sure not to take from the same locations. in the index.
    '''
    for name in name_list:
        i += 1
        timeline_data = []
        game_data = []
        sleep(100)
        print('sleeping:100 then pulling puuid')
        puuid = get_puuid(name)
        match_list = get_match_ids(puuid,api_key) #45
        sleep(120)
        print('sleeping:120 got match list')
        timeline_data, game_data = get_match_info(match_list,timeline_data,game_data, api_key, time = 20,url = 'https://americas.api.riotgames.com/')
        timeline_df = pd.DataFrame(timeline_data)
        game_df = pd.DataFrame(game_data)
        game_df.to_json(f'/users/jaredvahle/personal-work/league_of_legends_capstone/capstone/jared/json_folder/game_data_{i}.json')
        timeline_df.to_json(f'/users/jaredvahle/personal-work/league_of_legends_capstone/capstone/jared/json_folder/timeline_data_{i}.json')
        df = prepare.prepare(timeline_data, game_data, time = 20)
        print(f"{i+1} Completed!")
        
    return df