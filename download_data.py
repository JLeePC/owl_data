import os
import zipfile
import requests

os.chdir('data')

os.remove('match_map_stats.csv')
match_url = 'https://assets.blz-contentstack.com/v3/assets/blt321317473c90505c/blt3c792ae164693de8/5e95026d297b4d1b5ff03d35/match_map_stats.zip'
r = requests.get(match_url, allow_redirects=True)
open('maps.zip', 'wb').write(r.content)
with zipfile.ZipFile('maps.zip', 'r') as zip_ref:
    zip_ref.extractall()
os.remove('maps.zip')

os.remove('phs_2020_1.csv')
player_url = 'https://assets.blz-contentstack.com/v3/assets/blt321317473c90505c/blt45c4e7fb827663e5/5e9502ce297b4d1b5ff03d3b/phs_2020.zip'
r = requests.get(player_url, allow_redirects=True)
open('2020_player.zip', 'wb').write(r.content)
with zipfile.ZipFile('2020_player.zip', 'r') as zip_ref:
    zip_ref.extractall()
os.remove('2020_player.zip')

print('Done!')