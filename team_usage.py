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

data = pd.read_csv('data/phs_2020_1.csv')

#* Get all match ids and the total time played in those matches
match_id_list = []
match_time = []
teams = []
last_match_map = ''
last_match_id = 0
for i in range(len(data)):
    if data['hero_name'][i] == 'All Heroes':
        if data['stat_name'][i] == 'Time Played':
            if data['esports_match_id'][i] not in match_id_list:
                match_id_list.append(data['esports_match_id'][i])
                teams.append(data['team_name'][i])
                builder = {}
                builder['match_id'] = int(data['esports_match_id'][i])
                builder['time_played'] = data['stat_amount'][i]
                match_time.append(builder)
            else:
                if not data['map_name'][i] == last_match_map:
                    if int(data['esports_match_id'][i]) == last_match_id:
                        for match in match_time:
                            if match['match_id'] == int(data['esports_match_id'][i]):
                                match['time_played'] = match['time_played'] + data['stat_amount'][i]
                last_match_map = data['map_name'][i]
                last_match_id = int(data['esports_match_id'][i])

#* Get all hero play time per team per match
hero_time = {}
match_list = []

for i in range(len(data)):
    if data['stat_name'][i] == 'Time Played':
        if data['hero_name'][i] != 'All Heroes':
            if not data['team_name'][i] in hero_time:
                hero_time[data['team_name'][i]] = []
            add_hero = True
            for k in hero_time[data['team_name'][i]]:
                if k['hero_name'] == data['hero_name'][i]:
                    if k['match_id'] == int(data['esports_match_id'][i]):
                        k['time_played'] = k['time_played'] + data['stat_amount'][i]
                        add_hero = False
            builder = {}
            if add_hero:
                builder['match_id'] = int(data['esports_match_id'][i])
                for p in match_time:
                    if p['match_id'] == int(data['esports_match_id'][i]):
                        builder['match_time'] = p['time_played']
                builder['hero_name'] = data['hero_name'][i]
                builder['time_played'] = data['stat_amount'][i]
                hero_time[data['team_name'][i]].append(builder)

for team in hero_time:
    for hero in hero_time[team]:
        hero['percentage'] = (hero['time_played'] / hero['match_time'])

hero_usage = {}
for team in hero_time:
    if not team in hero_usage:
        hero_usage[team] = []
    for hero in ow_heroes:
        # if not hero in hero_usage[team]:
        builder = {}
        builder['hero_name'] = hero
        builder['percentage'] = 0
        builder['time_played'] = 0
        hero_usage[team].append(builder)
    for hero in hero_time[team]:
        for update in hero_usage[team]:
            if update['hero_name'] == hero['hero_name']:
                if update['percentage'] > 0:
                    update['percentage'] = (update['percentage'] + hero['percentage']) / 2
                    update['time_played'] = update['time_played'] + hero['time_played']
                else:
                    update['percentage'] = hero['percentage']
                    update['time_played'] = hero['time_played']

total_usage = []

for hero in ow_heroes:
    builder = {}
    builder['hero_name'] = hero
    builder['percentage'] = 0
    builder['time_played'] = 0
    total_usage.append(builder)

for total_hero in total_usage:
    for team in hero_usage:
        for hero in hero_usage[team]:
            if total_hero['hero_name'] == hero['hero_name']:
                total_hero['percentage'] = (total_hero['percentage'] + hero['percentage']) / 2
                total_hero['time_played'] = total_hero['time_played'] + hero['time_played']


with open('hero_time.json', 'w') as json_file:
    json.dump(hero_time, json_file, indent=2)

with open('hero_usage.json', 'w') as json_file:
    json.dump(hero_usage, json_file, indent=2)

with open('total_usage.json', 'w') as json_file:
    json.dump(total_usage, json_file, indent=2)

bar_hero = []
bar_time = []
for j in range(0,10000):
    for i in total_usage:
        if int(i['percentage'] * 10000) == j:
            if i['percentage'] >= 0:
                bar_hero.append("{} - {}%".format(i['hero_name'],round(i['percentage']*100,2)))
                bar_time.append(i['percentage']*100)

plt.barh(bar_hero, bar_time)

plt.title("Most played heroes 2020")
plt.xlabel("Percentage")

plt.tight_layout()

plt.show()