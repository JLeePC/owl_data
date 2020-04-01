import os
import zipfile
import requests

os.chdir('data')

os.remove('match_map_stats.csv')
match_url = 'https://assets.blz-contentstack.com/v3/assets/blt321317473c90505c/blt6227c17dad8ae329/5e67cde78286c81bdae79015/match_map_stats.zip'
r = requests.get(match_url, allow_redirects=True)
open('maps.zip', 'wb').write(r.content)
with zipfile.ZipFile('maps.zip', 'r') as zip_ref:
    zip_ref.extractall()
os.remove('maps.zip')

player_url = 'https://assets.blz-contentstack.com/v3/assets/blt321317473c90505c/blt18e13a8c2e83d9d7/5e67cde7a9f0fb732c24cf48/phs_2020.zip'
r = requests.get(player_url, allow_redirects=True)
open('2020_player.zip', 'wb').write(r.content)
with zipfile.ZipFile('2020_player.zip', 'r') as zip_ref:
    zip_ref.extractall()
os.remove('2020_player.zip')

print('Done!')