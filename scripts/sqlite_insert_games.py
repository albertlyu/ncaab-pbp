import sqlite3
import os
import simplejson as json

db = sqlite3.connect("../data/pbp.db")
c = db.cursor()

# Fetch all scoreboard paths
scoreboard_paths = [];
for root, dirs, files in os.walk("..\\data\\scoreboards"):
	for file in files:
		if file.endswith("scoreboard.json"):
			scoreboard_paths.append(os.path.join(root, file))

# For each scoreboard_path...
# 1. INSERT OR IGNORE INTO teams (team_id, team_alias, team_name, team_mascot, team_div, team_conf) VALUES ()
# 2. INSERT OR IGNORE INTO games (game_id, date, home_team_id, away_team_id, json) VALUES ()

c.execute('DELETE FROM teams')
c.execute('DELETE FROM games')

for scoreboard_path in scoreboard_paths:
	scoreboard = json.load(open(scoreboard_path))
	for contest in range(len(scoreboard['contests'])):
		home_team_id = scoreboard['contests'][contest]['homeTeam']['id']
		home_team_alias = scoreboard['contests'][contest]['homeTeam']['abrv']
		home_team_name = scoreboard['contests'][contest]['homeTeam']['name']
		home_team_mascot = scoreboard['contests'][contest]['homeTeam']['mascot']
		home_team_div = scoreboard['contests'][contest]['homeTeam']['division']
		home_team_conf = scoreboard['contests'][contest]['homeTeam']['conference']
		
		away_team_id = scoreboard['contests'][contest]['visitorTeam']['id']
		away_team_alias = scoreboard['contests'][contest]['visitorTeam']['abrv']
		away_team_name = scoreboard['contests'][contest]['visitorTeam']['name']
		away_team_mascot = scoreboard['contests'][contest]['visitorTeam']['mascot']
		away_team_div = scoreboard['contests'][contest]['visitorTeam']['division']
		away_team_conf = scoreboard['contests'][contest]['visitorTeam']['conference']

		game_id = scoreboard['contests'][contest]['id']
		date = scoreboard['contests'][contest]['dateYearMonthDay']
		year = scoreboard['contests'][contest]['seasonYear']
		venue_name = scoreboard['contests'][contest]['venue']['venueName']
		venue_city = scoreboard['contests'][contest]['venue']['venueCity']
		venue_state = scoreboard['contests'][contest]['venue']['venueState']

		c.execute('INSERT OR IGNORE INTO teams VALUES (?, ?, ?, ?, ?, ?)',
			(home_team_id, home_team_alias, home_team_name, home_team_mascot, home_team_div, home_team_conf))
		c.execute('INSERT OR IGNORE INTO teams VALUES (?, ?, ?, ?, ?, ?)',
			(away_team_id, away_team_alias, away_team_name, away_team_mascot, away_team_div, away_team_conf))
		c.execute('INSERT OR IGNORE INTO games VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
			(game_id, date, year, home_team_id, away_team_id, venue_name, venue_city, venue_state))
		c.execute('INSERT OR IGNORE INTO games VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
			(game_id, date, year, home_team_id, away_team_id, venue_name, venue_city, venue_state))

	print("Inserted records into teams and games from", scoreboard_path)

db.commit()
