import os
import zipfile
import requests

os.chdir('data')

os.remove('match_map_stats.csv')
match_url = 'https://assets.blz-contentstack.com/v3/assets/blt321317473c90505c/bltef5373d24b5cddc6/5eb9afb7a84f2107d1775bed/match_map_stats.zip'
r = requests.get(match_url, allow_redirects=True)
open('maps.zip', 'wb').write(r.content)
with zipfile.ZipFile('maps.zip', 'r') as zip_ref:
    zip_ref.extractall()
os.remove('maps.zip')

player_url = 'https://assets.blz-contentstack.com/v3/assets/blt321317473c90505c/blta399d2c02e1fdb82/5eb9afc82c37305d4d9dde35/phs_2020.zip'
r = requests.get(player_url, allow_redirects=True)
open('2020_player.zip', 'wb').write(r.content)
with zipfile.ZipFile('2020_player.zip', 'r') as zip_ref:
    zip_ref.extractall()
os.remove('2020_player.zip')

print('Done!')