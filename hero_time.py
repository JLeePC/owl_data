import os
import csv
import sys
import json
import numpy as np
import pandas as pd
import matplotlib
from collections import Counter
from matplotlib import pyplot as plt

#! the percentagesdont match what OWL shows. I think its usage per match then averaged.

tanks = ['D.Va','Orisa','Reinhardt','Roadhog','Sigma','Winston','Wrecking Ball','Zarya']
damage = ['Ashe','Bastion','Doomfist','Genji','Hanzo','Junkrat','McCree','Mei','Pharah','Reaper','Soldier: 76','Sombra','Symmetra','Torbjörn','Tracer','Widowmaker']
support = ['Ana','Baptiste','Brigitte','Lúcio','Mercy','Moira','Zenyatta']

tank_time = 0
damage_time = 0
support_time = 0

played_heroes = []
hero_times = []

data = pd.read_csv('data/phs_2020_1.csv')
for i in range(len(data)):
    if data['esports_match_id'][i] >= 0:
        hero = data['hero_name'][i]
        if not 'All Heroes' in hero:
            if 'Time Played' in data['stat_name'][i]:
                if hero in played_heroes:
                    #* update time played number
                    for j in hero_times:
                        if hero in j['Hero']:
                            j['Time Played'] = j['Time Played'] + data['stat_amount'][i]
                            
                else:
                    #* add hero
                    builder = {}
                    builder['Hero'] = hero
                    if hero in tanks:
                        builder['Hero Type'] = 'Tank'
                    if hero in damage:
                        builder['Hero Type'] = 'Damage'
                    if hero in support:
                        builder['Hero Type'] = 'Support'
                    builder['Time Played'] = data['stat_amount'][i]
                    played_heroes.append(hero)
                    hero_times.append(builder)

                if hero in tanks:
                    tank_time = tank_time + data['stat_amount'][i]
                if hero in damage:
                    damage_time = damage_time + data['stat_amount'][i]
                if hero in support:
                    support_time = support_time + data['stat_amount'][i]

# print(played_heroes)
# print(hero_times)
# print(tank_time,damage_time,support_time)

for i in hero_times:
    time_played = i['Time Played']
    hero = i['Hero']
    time_percentage = time_played / (tank_time + damage_time + support_time)
    # if hero in tanks:
    #     time_percentage = time_played / tank_time
    # if hero in damage:
    #     time_percentage = time_played / damage_time
    # if hero in support:
    #     time_percentage = time_played / support_time

    i['Percentage'] = time_percentage

for i in hero_times:
    print(i)

with open('time.json', 'w') as json_file:
  json.dump(hero_times, json_file, indent=2)

bar_hero = []
bar_time = []
for j in range(0,10000):
    for i in hero_times:
        if int(i['Percentage'] * 10000) == j:
            if i['Percentage'] >= 0:
                bar_hero.append("{} - {}%".format(i['Hero'],round(i['Percentage']*100,2)))
                bar_time.append(i['Percentage']*100)

plt.barh(bar_hero, bar_time)

# for i, v in enumerate(times_played):
#     plt.text(v - 12, i - .3, str(v), color='white')

plt.title("Most played heroes 2020")
plt.xlabel("Percentage")

plt.tight_layout()

plt.show()
