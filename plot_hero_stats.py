import os
import csv
import sys
import json
import time
import matplotlib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#TODO: place info in dict instead of lists so i can customize what the order is 

plt.style.use("fivethirtyeight")

with open('hero_stats.json', 'r') as json_data:
    hero_stats = json.load(json_data)

with open('hero_stats_list.json', 'r') as json_data:
    hero_stats_list = json.load(json_data)

hero_search = 'L\u00facio'
stat_search = ['Sound Barrier Efficiency', 'Sound Barrier Casts']

plot_stats = {}

for hero in hero_stats:
    if hero  == hero_search:
        bar_player = []
        bar_amount = []
        for player in hero_stats[hero][stat_search[0]]:
            if player['play_time'] / 60 >= 60:
                builder = {}
                builder['player_name'] = player['player_name']
                bar_player.append(player['player_name'])
                for p in hero_stats_list[hero]:
                    if p['stat_name'] == stat_search[0]:
                        if p['stat_state']:
                            builder['amount'] = player['per_10']
                            bar_amount.append(player['per_10'])
                        else:
                            builder['amount'] = player['stat_amount']
                            bar_amount.append(player['stat_amount'])
        if len(stat_search) >1:
            bar_amount_2 = []
            for i in bar_player:
                for player in hero_stats[hero][stat_search[1]]:
                    if player['player_name'] == i:
                        for p in hero_stats_list[hero]:
                            if p['stat_name'] == stat_search[1]:
                                if p['stat_state']:
                                    bar_amount_2.append(player['per_10'])
                                else:
                                    bar_amount_2.append(player['stat_amount'])

if len(stat_search) >1:
    average = []
    for i in range(len(bar_player)):
        average.append((bar_amount[i] + bar_amount_2[i])/2)

x_indexes = np.arange(len(bar_player))
w = 0.25
if len(stat_search) >1:
    plt.plot(x_indexes, average, color="#000000", label='Average')  
if len(stat_search) >1:
    plt.bar(x_indexes - w/2, bar_amount, width= w, color="#c71212", label=stat_search[0])
    plt.bar(x_indexes + w/2, bar_amount_2, width= w, color="#008fd5", label=stat_search[1])
else:
    plt.bar(x_indexes, bar_amount, label=stat_search[0])

plt.xticks(ticks=x_indexes, labels=bar_player, rotation='vertical')

# plt.title('Biotic Grenade / 10 mins')
# plt.xlabel('Player'.format(stat_search[0]))

plt.tight_layout()

plt.legend(loc='upper left',prop={'size':10})

plt.show()

json_data.close()
