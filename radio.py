import requests
from bs4 import BeautifulSoup
from collections import defaultdict

tmp = []

website = ('https://onlineradiobox.com/us/wjis/playlist/1')
r = requests.get(website)

soup = BeautifulSoup(r.text, 'html.parser')


tracks = soup.find_all(class_="track_history_item")

for track in tracks:
    str_track = str(track)
    str_track = str_track.split('/">')
    for line in range(1, len(str_track), 2):
        tmp.append(str_track[line])

tmp = [s.replace("</a>\n</td>", "") for s in tmp]

songs = defaultdict(list)

for s in tmp:
    if ' - ' in s:
        artist, song = s.split(' - ')
        songs[artist].append(song)

for line, value in songs.items():
    print(f"{line}: {value}")
