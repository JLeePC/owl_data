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

hero_usage = {}

for i in range(len(data)):
    match_id = int(data['esports_match_id'][i])
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

for team in hero_usage:
    team_percentage_builder = []
    heroes_used_builder = []
    hero_usage[team]['team_percentage'] = []
    hero_usage[team]['heroes_used'] = []
    for match in hero_usage[team]:
        for match_map in hero_usage[team][match]:
            for hero in hero_usage[team][match][match_map]['heroes']:
                hero['percentage'] = hero['time_played'] / hero_usage[team][match][match_map]['map_time']
                if not hero['hero_name'] in hero_usage[team]['heroes_used']:
                    builder = {}
                    builder['hero_name'] = hero['hero_name']
                    builder['percentage'] = hero['percentage']
                    team_percentage_builder.append(builder)
                    heroes_used_builder.append(hero['hero_name'])
                # else:
                #     for team_2 in hero_usage:
                #         for hero_2 in hero_usage[team]:
                #             if hero['hero_name'] == hero_2['hero_name']:
                #                 hero_2['percentage'] = hero_2['percentage'] + hero['percentage']
    hero_usage[team]['team_percentage'].append(team_percentage_builder)
    hero_usage[team]['heroes_used'].append(heroes_used_builder)
                
# for i in hero_usage['Dallas Fuel']:
#     print(len(hero_usage['Dallas Fuel'][i]))

with open('owl_hero_usage.json', 'w') as json_file:
    json.dump(hero_usage, json_file, indent=2)