import os
import json

def build():
    with open('hero_stats.json', 'r') as json_data:
        hero_stats = json.load(json_data)

    hero_stats_list = {}

    for hero in hero_stats:
        hero_stats_list[hero] = []
        for stat in hero_stats[hero]:
            if 'Time' in stat or 'Percentage' in stat or 'Efficiency' in stat or 'Average' in stat or 'Accuracy' in stat:
                builder = {stat: False}
            else:
                builder = {stat: True}
            hero_stats_list[hero].append(builder)

    with open('hero_stats_list.json', 'w') as json_file:
        json.dump(hero_stats_list, json_file, indent=2)

if __name__ == "__main__":
    build()