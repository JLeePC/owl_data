import os
import csv
import numpy as np
import pandas as pd
import matplotlib
from collections import Counter
from matplotlib import pyplot as plt

pd_data = pd.read_csv('data/match_map_stats.csv')
match_id = []
map_counter = Counter()
match_counter = Counter()
previous_round = ''
for i in range(len(pd_data)):
    pd_maps = pd_data['map_name'][i]
    pd_round = pd_data['map_round'][i]
    if pd_round == 1:
        map_counter.update(pd_maps.split('.'))
    previous_round = pd_round
maps = []
times_played = []

for i in map_counter.most_common(21):
    maps.append(i[0])
    times_played.append(i[1])

maps.reverse()
times_played.reverse()

plt.barh(maps, times_played)

for i, v in enumerate(times_played):
    plt.text(v - 12, i - .3, str(v), color='white')

plt.title("Most played maps 2018-2019")
plt.xlabel("Times played")

plt.tight_layout()

plt.show()
