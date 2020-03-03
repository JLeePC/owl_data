import os
import csv
import sys
import json
import numpy as np
import pandas as pd
import matplotlib
from collections import Counter
from matplotlib import pyplot as plt

ow_heroes = ['D.Va','Orisa','Reinhardt','Roadhog','Sigma','Winston','Wrecking Ball','Zarya',
            'Ashe','Bastion','Doomfist','Genji','Hanzo','Junkrat','McCree','Mei','Pharah','Reaper','Soldier: 76','Sombra','Symmetra','Torbjörn','Tracer','Widowmaker',
            'Ana','Baptiste','Brigitte','Lúcio','Mercy','Moira','Zenyatta']

match_id_list = []
match_time = []

data = pd.read_csv('data/phs_2020_1.csv')
for i in range(len(data)):
    if data['hero_name'][i] == 'All Heroes':
        if data['stat_name'][i] == 'Time Played':
            if data['esports_match_id'][i] not in match_id_list:
                match_id_list.append(data['esports_match_id'][i])
                builder = {}
                builder['match_id'] = data['esports_match_id'][i]
                builder['time_played'] = data['stat_amount'][i]
                match_time.append(builder)
            else:
                for match in match_time:
                    match['time_played'] =+ data['stat_amount'][i]
                
usage = {}
for match in match_id_list:
    copy = False
    match_id = []
    heroes = []
    for i in range(len(data)):
        if data['esports_match_id'][i] == match:
            if 'Time Played' in data['stat_name'][i]:
                if not 'All Heroes' in data['hero_name'][i]:
                    if data['hero_name'][i] in heroes:
                        for k in match_id:
                            if k['Hero'] == data['hero_name'][i]:
                                k['Time Played'] =+ data['stat_amount'][i]
                    else:
                        builder = {}
                        builder['Hero'] = data['hero_name'][i]
                        builder['Time Played'] = data['stat_amount'][i]
                        match_id.append(builder)
                        heroes.append(data['hero_name'][i])
    for hero in ow_heroes:
        if hero not in heroes:
            builder = {}
            builder['Hero'] = hero
            builder['Time Played'] = float(0)
            match_id.append(builder)

    usage[str(match)] = match_id

matches = {'Matches':usage}

for match_id in match_time:
    for match in matches['Matches']:
        if int(match) == int(match_id['match_id']):
            for hero in matches['Matches'][str(match_id['match_id'])]:
                hero['Percentage'] = hero['Time Played'] / match_id['time_played']

hero_usage = []
heroes = []
for match in matches['Matches']:
    for hero in matches['Matches'][str(match)]:
        if hero['Hero'] not in heroes:
            builder = {}
            builder['Hero'] = hero['Hero']
            builder['Usage'] = hero['Percentage']
            hero_usage.append(builder)
            heroes.append(hero['Hero'])
        else:
            for i in hero_usage:
                if i['Hero'] == hero['Hero']:
                    i['Usage'] = (i['Usage'] + hero['Percentage'])/2


with open('usage.json', 'w') as json_file:
    json.dump(hero_usage, json_file, indent=2)

bar_hero = []
bar_time = []
for j in range(0,10000):
    for i in hero_usage:
        if int(i['Usage'] * 10000) == j:
            if i['Usage'] >= 0:
                bar_hero.append("{} - {}%".format(i['Hero'],round(i['Usage']*100,2)))
                bar_time.append(i['Usage']*100)

plt.barh(bar_hero, bar_time)

# for i, v in enumerate(times_played):
#     plt.text(v - 12, i - .3, str(v), color='white')

plt.title("Most played heroes 2020")
plt.xlabel("Percentage")

plt.tight_layout()

plt.show()