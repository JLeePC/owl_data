import os
import csv
import sys
import json
import numpy as np
import pandas as pd
import matplotlib
from collections import Counter
from matplotlib import pyplot as plt

tanks = ['D.Va','Orisa','Reinhardt','Roadhog','Sigma','Winston','Wrecking Ball','Zarya']
damage = ['Ashe','Bastion','Doomfist','Genji','Hanzo','Junkrat','McCree','Mei','Pharah','Reaper','Soldier: 76','Sombra','Symmetra','Torbjörn','Tracer','Widowmaker']
support = ['Ana','Baptiste','Brigitte','Lúcio','Mercy','Moira','Zenyatta']

data = pd.read_csv('data/phs_2020_1.csv')

hero_usage = {}

for i in range(len(data)):
    if data['hero_name'][i] != 'All Heroes':
        if data['stat_name'][i] == 'Time Played':
            if not data['team_name'][i] in hero_usage:
                hero_usage[data['team_name'][i]] = []
            if not data['esports_match_id'][i] in hero_usage[data['team_name'][i]]:
                hero_usage[data['team_name'][i]][data['esports_match_id'][i]] = [] #! trying to create list inside list but its not working. How do you do it?
            add_hero = True
            for k in hero_usage[data['team_name'][i]]:
                if k['hero_name'] == data['hero_name'][i]:
                    k['time_played'] = k['time_played'] + data['stat_amount'][i]
                    add_hero = False
            if add_hero:
                builder = {}
                builder['hero_name'] = data['hero_name'][i]
                builder['time_played'] = data['stat_amount'][i]
                hero_usage[data['team_name'][i]][data['esports_match_id'][i]].append(builder)
            
# print(json.dumps(hero_usage, indent=2))

with open('team_usage.json', 'w') as json_file:
    json.dump(hero_usage, json_file, indent=2)