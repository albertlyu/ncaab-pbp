import sqlite3
import os
import simplejson as json

db = sqlite3.connect("../data/pbp.db")
c = db.cursor()

# Fetch all playbyplay paths
playbyplay_paths = [];
for root, dirs, files in os.walk("..\\data\\gameflash"):
	for file in files:
		if file.endswith("_playbyplay.json"):
			playbyplay_paths.append(os.path.join(root, file))

# For each playbyplay_path...
# 1. INSERT OR IGNORE INTO players (player_id, player_first_name, player_last_name, player_team_id) VALUES ()
# 2. INSERT OR IGNORE INTO plays () VALUES ()
# 3. INSERT OR IGNORE INTO shots () VALUES ()

c.execute('DELETE FROM players')
c.execute('DELETE FROM plays')

for playbyplay_path in playbyplay_paths: 
	playbyplay = json.load(open(playbyplay_path))

	for play in range(len(playbyplay['playbyplay']['plays']['play'])):
		if (playbyplay['playbyplay']['plays']['play'][play]['player1-id'] != ""):
			c.execute('INSERT OR IGNORE INTO players VALUES (?, ?, ?, ?)', (
				playbyplay['playbyplay']['plays']['play'][play]['player1-id'],
				playbyplay['playbyplay']['plays']['play'][play]['player-first-name-1'],
				playbyplay['playbyplay']['plays']['play'][play]['player-last-name-1'],
				playbyplay['playbyplay']['plays']['play'][play]['team-id-1']
				)
			)
		c.execute('INSERT OR IGNORE INTO plays VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
			playbyplay['playbyplay']['contest']['id'],
			playbyplay['playbyplay']['plays']['play'][play]['half'],
			playbyplay['playbyplay']['plays']['play'][play]['time-minutes'],
			playbyplay['playbyplay']['plays']['play'][play]['time-seconds'],
			playbyplay['playbyplay']['plays']['play'][play]['details'],
			playbyplay['playbyplay']['plays']['play'][play]['player1-id'],
			playbyplay['playbyplay']['plays']['play'][play]['player2-id'],
			playbyplay['playbyplay']['plays']['play'][play]['player1-linkable'],
			playbyplay['playbyplay']['plays']['play'][play]['player2-linkable'],
			playbyplay['playbyplay']['plays']['play'][play]['player3-linkable'],
			playbyplay['playbyplay']['plays']['play'][play]['player-first-name-1'],
			playbyplay['playbyplay']['plays']['play'][play]['player-first-name-2'],
			playbyplay['playbyplay']['plays']['play'][play]['player-last-name-1'],
			playbyplay['playbyplay']['plays']['play'][play]['player-last-name-2'],
			playbyplay['playbyplay']['plays']['play'][play]['home-score'],
			playbyplay['playbyplay']['plays']['play'][play]['visitor-score'],
			playbyplay['playbyplay']['plays']['play'][play]['visitor-fouls'],
			playbyplay['playbyplay']['plays']['play'][play]['home-fouls'],
			playbyplay['playbyplay']['plays']['play'][play]['player-fouls'],
			playbyplay['playbyplay']['plays']['play'][play]['player-score'],
			playbyplay['playbyplay']['plays']['play'][play]['points-type'],
			playbyplay['playbyplay']['plays']['play'][play]['detail-desc'],
			playbyplay['playbyplay']['plays']['play'][play]['event-desc'],
			playbyplay['playbyplay']['plays']['play'][play]['distance'],
			playbyplay['playbyplay']['plays']['play'][play]['x-coord'],
			playbyplay['playbyplay']['plays']['play'][play]['y-coord'],
			playbyplay['playbyplay']['plays']['play'][play]['team-id-1'],
			playbyplay['playbyplay']['plays']['play'][play]['team-id-2'],
			playbyplay['playbyplay']['plays']['play'][play]['team-id-3']
			)
		)
		if (playbyplay['playbyplay']['plays']['play'][play]['x-coord'] != "" and playbyplay['playbyplay']['plays']['play'][play]['y-coord'] != ""):
			c.execute('INSERT OR IGNORE INTO shots VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
				playbyplay['playbyplay']['contest']['id'],
				playbyplay['playbyplay']['plays']['play'][play]['half'],
				playbyplay['playbyplay']['plays']['play'][play]['time-minutes'],
				playbyplay['playbyplay']['plays']['play'][play]['time-seconds'],
				playbyplay['playbyplay']['plays']['play'][play]['details'],
				playbyplay['playbyplay']['plays']['play'][play]['player1-id'],
				playbyplay['playbyplay']['plays']['play'][play]['player2-id'],
				playbyplay['playbyplay']['plays']['play'][play]['home-score'],
				playbyplay['playbyplay']['plays']['play'][play]['visitor-score'],
				playbyplay['playbyplay']['plays']['play'][play]['visitor-fouls'],
				playbyplay['playbyplay']['plays']['play'][play]['home-fouls'],
				playbyplay['playbyplay']['plays']['play'][play]['player-fouls'],
				playbyplay['playbyplay']['plays']['play'][play]['player-score'],
				playbyplay['playbyplay']['plays']['play'][play]['points-type'],
				playbyplay['playbyplay']['plays']['play'][play]['detail-desc'],
				playbyplay['playbyplay']['plays']['play'][play]['event-desc'],
				playbyplay['playbyplay']['plays']['play'][play]['distance'],
				playbyplay['playbyplay']['plays']['play'][play]['x-coord'],
				playbyplay['playbyplay']['plays']['play'][play]['y-coord'],
				playbyplay['playbyplay']['plays']['play'][play]['team-id-1']
				)
			)
	print("Inserted records into plays from", playbyplay_path)

db.commit()
