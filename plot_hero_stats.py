import os
import csv
import sys
import json
import time
import matplotlib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

with open('hero_stats.json', 'r') as json_data:
    hero_stats = json.load(json_data)

with open('hero_stats_list.json', 'r') as json_data:
    hero_stats_list = json.load(json_data)

hero_search = 'Ana'
stat_search = ['Damage - Biotic Grenade']

for hero in hero_stats:
    if hero  == hero_search:
        for search in stat_search:
            bar_player = []
            bar_amounr = []
            for player in hero_stats[hero][search]:
                if player['play_time'] / 60 >= 90:
                    bar_player.append("{} - {}".format(player['player_name'],round(player['per_10'],2)))
                    bar_amounr.append(player['per_10'])

            plt.barh(bar_player, bar_amounr)

            plt.title(hero_search)
            plt.xlabel('{} / 10 mins'.format(search))

            plt.tight_layout()

            plt.show()

json_data.close()
