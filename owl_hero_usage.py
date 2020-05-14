import os
import csv
import sys
import json
import time
import matplotlib
import progressbar
import numpy as np
import pandas as pd
from collections import Counter
from matplotlib import pyplot as plt

ow_heroes = ['D.Va','Orisa','Reinhardt','Roadhog','Sigma','Winston','Wrecking Ball','Zarya',
            'Ashe','Bastion','Doomfist','Genji','Hanzo','Junkrat','McCree','Mei','Pharah','Reaper','Soldier: 76','Sombra','Symmetra','Torbjörn','Tracer','Widowmaker',
            'Ana','Baptiste','Brigitte','Lúcio','Mercy','Moira','Zenyatta']

data = pd.read_csv('data/phs_2020_1.csv')

print('Compiling data..')

hero_usage = {}
with progressbar.ProgressBar(max_value=len(data)) as bar:
    for i in range(len(data)):
        match_id = int(data['esports_match_id'][i])
        if match_id >= 0:
            if data['stat_name'][i] == 'Time Played':
                if data['hero_name'][i] != 'All Heroes':
                    builder = {}
                    builder['hero_name'] = data['hero_name'][i]
                    builder['time_played'] = data['stat_amount'][i]

                    try:
                        hero_usage[data['team_name'][i]][match_id][data['map_name'][i]]['heroes'].append(builder)
                    except KeyError:
                        try:
                            hero_usage[data['team_name'][i]][match_id][data['map_name'][i]]['heroes'] = []
                            hero_usage[data['team_name'][i]][match_id][data['map_name'][i]]['heroes'].append(builder)
                        except KeyError:
                            try:
                                hero_usage[data['team_name'][i]][match_id][data['map_name'][i]] = {}
                                hero_usage[data['team_name'][i]][match_id][data['map_name'][i]]['heroes'] = []
                                hero_usage[data['team_name'][i]][match_id][data['map_name'][i]]['heroes'].append(builder)
                            except KeyError:
                                try:
                                    hero_usage[data['team_name'][i]][match_id] = {}
                                    hero_usage[data['team_name'][i]][match_id][data['map_name'][i]] = {}
                                    hero_usage[data['team_name'][i]][match_id][data['map_name'][i]]['heroes'] = []
                                    hero_usage[data['team_name'][i]][match_id][data['map_name'][i]]['heroes'].append(builder)
                                except KeyError:
                                    hero_usage[data['team_name'][i]] = {}
                                    hero_usage[data['team_name'][i]][match_id] = {}
                                    hero_usage[data['team_name'][i]][match_id][data['map_name'][i]] = {}
                                    hero_usage[data['team_name'][i]][match_id][data['map_name'][i]]['heroes'] = []
                                    hero_usage[data['team_name'][i]][match_id][data['map_name'][i]]['heroes'].append(builder)

                else:
                    #* get map play times
                    try:
                        hero_usage[data['team_name'][i]][match_id][data['map_name'][i]]['map_time']  = float(data['stat_amount'][i])
                    except KeyError:
                        try:
                            hero_usage[data['team_name'][i]][match_id][data['map_name'][i]] = {}
                            hero_usage[data['team_name'][i]][match_id][data['map_name'][i]]['map_time']  = float(data['stat_amount'][i])
                        except KeyError:
                            try:
                                hero_usage[data['team_name'][i]][match_id] = {}
                                hero_usage[data['team_name'][i]][match_id][data['map_name'][i]] = {}
                                hero_usage[data['team_name'][i]][match_id][data['map_name'][i]]['map_time']  = float(data['stat_amount'][i])
                            except KeyError:
                                hero_usage[data['team_name'][i]] = {}
                                hero_usage[data['team_name'][i]][match_id] = {}
                                hero_usage[data['team_name'][i]][match_id][data['map_name'][i]] = {}
                                hero_usage[data['team_name'][i]][match_id][data['map_name'][i]]['map_time']  = float(data['stat_amount'][i])
        bar.update(i)

print('Averaging team percentages..')

team_hero_usage = {}
with progressbar.ProgressBar(max_value=len(hero_usage)) as bar:
    x = 0
    for team in hero_usage:
        maps_played = 0
        team_hero_usage[team] = {}
        team_hero_usage[team]['team_percentage'] = []
        team_hero_usage[team]['heroes_used'] = []
        for match in hero_usage[team]:
            maps_played = maps_played + len(hero_usage[team][match])
            for match_map in hero_usage[team][match]:
                for hero in hero_usage[team][match][match_map]['heroes']:
                    hero['percentage'] = hero['time_played'] / hero_usage[team][match][match_map]['map_time']
                    if not hero['hero_name'] in team_hero_usage[team]['heroes_used']:
                        builder = {}
                        builder['hero_name'] = hero['hero_name']
                        builder['percentage'] = hero['percentage']
                        team_hero_usage[team]['team_percentage'].append(builder)
                        team_hero_usage[team]['heroes_used'].append(hero['hero_name'])
                    else:
                        for i in team_hero_usage[team]['team_percentage']:
                            if i['hero_name'] == hero['hero_name']:
                                i['percentage'] = i['percentage'] + hero['percentage']

        hero_usage[team]['maps_played'] = maps_played
        team_hero_usage[team]['maps_played'] = maps_played

        for i in team_hero_usage[team]['team_percentage']:
            i['percentage'] = i['percentage'] / hero_usage[team]['maps_played']
        x = x + 1
        bar.update(x)

with progressbar.ProgressBar(max_value=len(team_hero_usage)) as bar:
    x = 0
    for team in team_hero_usage:
        for hero in ow_heroes:
            if not hero in team_hero_usage[team]['heroes_used']:
                builder = {}
                builder['hero_name'] = hero
                builder['percentage'] = 0
                team_hero_usage[team]['team_percentage'].append(builder)
                team_hero_usage[team]['heroes_used'].append(hero)
        x = x + 1
        bar.update(x)
    

print('Averaging league percentages..')

owl_hero_usage = []
with progressbar.ProgressBar(max_value=len(ow_heroes)) as bar:
    x = 0
    for hero in ow_heroes:
        percentage = 0
        for team in team_hero_usage:
            for i in team_hero_usage[team]['team_percentage']:
                if i['hero_name'] == hero:
                    percentage = percentage + i['percentage']
        percentage = percentage / len(team_hero_usage)
        builder = {}
        builder['hero_name'] = hero
        builder['percentage'] = percentage
        owl_hero_usage.append(builder)
        x = x + 1
        bar.update(x)

with open('hero_usage.json', 'w') as json_file:
    json.dump(hero_usage, json_file, indent=2)

with open('team_hero_usage.json', 'w') as json_file:
    json.dump(team_hero_usage, json_file, indent=2)

with open('owl_hero_usage.json', 'w') as json_file:
    json.dump(owl_hero_usage, json_file, indent=2)

bar_hero = []
bar_time = []
for j in range(0,10000):
    for i in owl_hero_usage:
        if int(i['percentage'] * 10000) == j:
            if i['percentage'] >= 0:
                bar_hero.append("{} - {}%".format(i['hero_name'],round(i['percentage']*100,2)))
                bar_time.append(i['percentage']*100)

plt.barh(bar_hero, bar_time)

plt.title("Most played heroes 2020")
plt.xlabel("Percentage")

plt.tight_layout()

plt.show()