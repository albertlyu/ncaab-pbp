import urllib.request
import parse_pbp

# Get and save scoreboards given a set of conferences for a date range
def get_scoreboards(start_date, end_date, conferences, base_url, base_path):
	scoreboard_urls = []
	dates = parse_pbp.get_dates(start_date, end_date);
	for conference in conferences:
		for date in dates:
			mid_url = "".join((date[0:4], "/", date[5:7], "/", date[8:10], "/"))
			url = "".join((base_url, "scoreboards/", conference, "/", mid_url, "scoreboard.json"))
			if parse_pbp.validate_url(url) == True:
				scoreboard_urls.append(url)
				parse_pbp.save_json(url, base_url, base_path)
	return(scoreboard_urls)

# Get and save games given a set of scoreboard urls, which end in /scoreboards/CONF/YYYY/MM/DD/scoreboard.json
def get_games(scoreboard_urls, base_url, base_path):
	game_urls = []
	for scoreboard_url in scoreboard_urls:
		fpath = parse_pbp.split_url(scoreboard_url, base_url, base_path)
		if parse_pbp.validate_url(scoreboard_url) == True:
			urllib.request.urlopen(scoreboard_url)
			scoreboard = parse_pbp.parse_json(scoreboard_url, base_url, base_path)
			for game in range(0, len(scoreboard["contests"])):
				gid = str(scoreboard["contests"][game]["id"])
				date = str(scoreboard["contests"][game]["dateYearMonthDay"])
				url = "".join((base_url, "gameflash/", date, "/", gid, "_playbyplay.json"))
				if parse_pbp.validate_url(url) == True:
					game_urls.append(url)
					parse_pbp.save_json(url, base_url, base_path)
			print("Saved", fpath["date"], "game urls")
	return(game_urls)

# Start getting games here:
## You'll need start_date, end_date (in the form YYYY-MM-DD), conferences, base_url, base_path

scoreboard_urls = get_scoreboards(start_date, end_date, conferences, base_url, base_path) # Get scoreboard urls
game_urls = get_games(scoreboard_urls, base_url, base_path) # Get game urls