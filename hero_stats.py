import os
import csv
import sys
import json
import time
import matplotlib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv('data/phs_2020_1.csv')

start_time = time.time()

print('Compiling stats..')

hero_stats = {}

for i in range(len(data)):
    match_id = int(data['esports_match_id'][i])
    # if not data['hero_name'][i] == 'All Heroes':
    hero_name = data['hero_name'][i]
    stat_name = data['stat_name'][i]
    builder = {}
    builder['player_name'] = data['player_name'][i]
    builder['team_name'] = data['team_name'][i]
    builder['stat_amount'] = data['stat_amount'][i]

    try:
        add_player = True
        for player in hero_stats[hero_name][stat_name]:
            if player['player_name'] == data['player_name'][i]:
                add_player = False
                player['stat_amount'] = player['stat_amount'] + data['stat_amount'][i]
        if add_player:
            hero_stats[hero_name][stat_name].append(builder)
    except KeyError:
        try:
            hero_stats[hero_name][stat_name] = []
            hero_stats[hero_name][stat_name].append(builder)
        except KeyError:
            hero_stats[hero_name] = {}
            hero_stats[hero_name][stat_name] = []
            hero_stats[hero_name][stat_name].append(builder)

print('Calculating per 10 mins..')

#* amount / (time/600)

for hero in hero_stats:
    for stat in hero_stats[hero]:
        if stat != 'Time Played':
            for player in hero_stats[hero][stat]:
                stat_amount = player['stat_amount']
                for stat_2 in hero_stats[hero]:
                    if stat_2 == 'Time Played':
                        for player_2 in hero_stats[hero][stat_2]:
                            if player_2['player_name'] == player['player_name']:
                                play_time = player_2['stat_amount']
                player['play_time'] = play_time
                player['per_10'] = stat_amount / (play_time / 600)
                # sys.exit()

with open('hero_stats.json', 'w') as json_file:
    json.dump(hero_stats, json_file, indent=2)

print(round(time.time() - start_time,3))