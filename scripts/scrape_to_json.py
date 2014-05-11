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

# Get and save boxscore json files given a set of scoreboard urls, which end in /scoreboards/CONF/YYYY/MM/DD/scoreboard.json
def get_boxscores(scoreboard_urls, base_url, base_path):
	boxscore_urls = []
	for scoreboard_url in scoreboard_urls:
		fpath = parse_pbp.split_url(scoreboard_url, base_url, base_path)
		if parse_pbp.validate_url(scoreboard_url) == True:
			urllib.request.urlopen(scoreboard_url)
			scoreboard = parse_pbp.parse_json(scoreboard_url, base_url, base_path)
			for game in range(0, len(scoreboard["contests"])):
				gid = str(scoreboard["contests"][game]["id"])
				date = str(scoreboard["contests"][game]["dateYearMonthDay"])
				url = "".join((base_url, "gameflash/", date, "/", gid, "_boxscore.json"))
				if parse_pbp.validate_url(url) == True:
					boxscore_urls.append(url)
					parse_pbp.save_json(url, base_url, base_path)
			print("Saved", fpath["date"], "boxscore urls")
	return(boxscore_urls)

# Get and save playbyplay json files given a set of scoreboard urls, which end in /scoreboards/CONF/YYYY/MM/DD/scoreboard.json
def get_playbyplays(scoreboard_urls, base_url, base_path):
	playbyplay_urls = []
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
					playbyplay_urls.append(url)
					parse_pbp.save_json(url, base_url, base_path)
			print("Saved", fpath["date"], "playbyplay urls")
	return(playbyplay_urls)

# Start getting games here:
## You'll need start_date, end_date (in the form YYYY-MM-DD), conferences, base_url, base_path

start_date = "2013-11-08" # 2013-11-08
end_date = "2014-04-07" # 2014-03-16
conferences = ["ncaa64", "nit" "big10", "acc", "big12", "bige", "pac12", "sec", "aac"]
midmajors = ["aeast","atl10","atsun","bigw","bsky","bsou","coln","cusa","horiz","indp","ivy","maac","mac","meac","mvc","mwest","nec","ovc","patr","sbelt","sland","south","sum","swac","wac","wcc"]
base_url = "http://data.sportsillustrated.cnn.com/jsonp/basketball/ncaa/men/"
base_path = "../data/"
#scoreboard_url = "http://data.sportsillustrated.cnn.com/jsonp/basketball/ncaa/men/scoreboards/ncaa64/2014/03/23/scoreboard.json"
#boxscore_url = "http://data.sportsillustrated.cnn.com/jsonp/basketball/ncaa/men/gameflash/2014/03/23/93932_boxscore.json"
#playbyplay_url = "http://data.sportsillustrated.cnn.com/jsonp/basketball/ncaa/men/gameflash/2014/03/23/93932_playbyplay.json"

scoreboard_urls = get_scoreboards(start_date, end_date, ["divia"], base_url, base_path) # Get scoreboard urls
boxscore_urls = get_boxscores(scoreboard_urls, base_url, base_path) # Get boxscore urls
#playbyplay_urls = get_playbyplays(scoreboard_urls, base_url, base_path) # Get playbyplay urls