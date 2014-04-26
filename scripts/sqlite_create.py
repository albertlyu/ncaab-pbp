import sqlite3

db = sqlite3.connect("../data/pbp.db")
c = db.cursor()

# DROP TABLE IF EXISTS tables
c.execute('''DROP TABLE IF EXISTS teams''')
c.execute('''DROP TABLE IF EXISTS games''')
c.execute('''DROP TABLE IF EXISTS players''')
c.execute('''DROP TABLE IF EXISTS lkup_shot''')
c.execute('''DROP TABLE IF EXISTS lkup_event''')
c.execute('''DROP TABLE IF EXISTS plays''')
c.execute('''DROP TABLE IF EXISTS shots''')

# INSERT OR IGNORE INTO teams (team_id, team_alias) VALUES (123, 'XYZ')
c.execute('''CREATE TABLE teams (
	team_id INTEGER PRIMARY KEY,
	team_alias TEXT UNIQUE
	)
''')

# INSERT INTO games (game_id, date, home_team_id, away_team_id, json) VALUES ()
c.execute('''CREATE TABLE games (
	game_id INTEGER PRIMARY KEY,
	date NUMERIC,
	home_team_id INTEGER,
	away_team_id INTEGER,
	json BLOB,
	FOREIGN KEY(home_team_id) REFERENCES teams(team_id),
	FOREIGN KEY(away_team_id) REFERENCES teams(team_id)
	)
''')

# INSERT OR IGNORE INTO players (player_id, player_first_name, player_last_name, player_team_id) VALUES ()
c.execute('''CREATE TABLE players (
	player_id INTEGER PRIMARY KEY,
	player_first_name TEXT,
	player_last_name TEXT,
	player_team_id INTEGER,
	FOREIGN KEY(player_team_id) REFERENCES teams(team_id) 
	)
''')

# manual inserts
c.execute('''CREATE TABLE lkup_shot (
	detail_id INTEGER PRIMARY KEY,
	detail_desc TEXT
	)
''')

# manual inserts
c.execute('''CREATE TABLE lkup_event (
	event_id INTEGER PRIMARY KEY,
	event_desc TEXT
	)
''')

# insert NULL into play_id so that it autoincrements
c.execute('''CREATE TABLE plays (
	play_id INTEGER PRIMARY KEY,
	game_id INTEGER,
	half INTEGER,
	time_minutes INTEGER,
	time_seconds INTEGER,
	details TEXT,
	player_id_1 INTEGER,
	player_id_2 INTEGER,
	player_id_1_linkable NUMERIC,
	player_id_2_linkable NUMERIC,
	player_id_3_linkable NUMERIC,
	player_first_name_1 TEXT,
	player_first_name_2 TEXT,
	player_last_name_1 TEXT,
	player_last_name_2 TEXT,
	player_team_alias_1 TEXT,
	player_team_alias_2 TEXT,
	home_score INTEGER,
	visitor_score INTEGER,
	visitor_fouls INTEGER,
	home_fouls INTEGER,
	player_fouls INTEGER,
	fastbreak INTEGER,
	in_paint INTEGER,
	second_chance INTEGER,
	off_turnover INTEGER,
	player_score INTEGER,
	points_type INTEGER,
	detail_id INTEGER,
	event_id INTEGER,
	distance INTEGER,
	x_coord REAL,
	y_coord REAL,
	team_id_1 INTEGER,
	team_id_2 INTEGER,
	team_id_3 INTEGER,
	FOREIGN KEY(game_id) REFERENCES games(game_id),
	FOREIGN KEY(detail_id) REFERENCES lkup_shot(detail_id),
	FOREIGN KEY(event_id) REFERENCES lkup_event(event_id),
	FOREIGN KEY(team_id_1) REFERENCES teams(team_id),
	FOREIGN KEY(team_id_2) REFERENCES teams(team_id),
	FOREIGN KEY(team_id_3) REFERENCES teams(team_id)
	)
''')

# insert NULL into shot_id so that it autoincrements
c.execute('''CREATE TABLE shots (
	shot_id INTEGER PRIMARY KEY,
	play_id INTEGER,
	game_id INTEGER,
	team_id INTEGER,
	home_team_id INTEGER,
	away_team_id INTEGER,
	player_id INTEGER,
	player_id_assist INTEGER,
	detail_id INTEGER,
	event_id INTEGER,
	details TEXT,
	points_type INTEGER,
	made NUMERIC,
	x REAL,
	y REAL,
	FOREIGN KEY(play_id) REFERENCES plays(play_id),
	FOREIGN KEY(game_id) REFERENCES games(game_id),
	FOREIGN KEY(team_id) REFERENCES teams(team_id),
	FOREIGN KEY(home_team_id) REFERENCES teams(team_id),
	FOREIGN KEY(away_team_id) REFERENCES teams(team_id),
	FOREIGN KEY(player_id) REFERENCES players(player_id),
	FOREIGN KEY(player_id_assist) REFERENCES players(player_id),
	FOREIGN KEY(detail_id) REFERENCES lkup_shot(detail_id),
	FOREIGN KEY(event_id) REFERENCES lkup_event(event_id)
    )
''')