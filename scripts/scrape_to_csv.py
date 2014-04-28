import os
import urllib.request
import csv
import parse_pbp as pbp

# Get all games for a set of conferences for a date range
def get_conference_game_urls(start_date, end_date, conferences, base_url, base_path):
	dates = pbp.get_dates(start_date, end_date);
	urls = {};

	for conference in conferences:
		game_urls = []
		for date in dates:
			mid_url = "".join((date[0:4], "/", date[5:7], "/", date[8:10], "/"))
			url = "".join((base_url, "scoreboards/", conference, "/", mid_url, "scoreboard.json"))
			req = urllib.request.Request(url)
			try:
				urllib.request.urlopen(req)
			except urllib.error.HTTPError as e:
				print("Error code:", e.code, "- No", conference, "games on", date)
				continue
			except urllib.error.URLError as e:
				print("We failed to reach a server.")
				print("Reason: ", e.reason)
				continue
			else: 
				urllib.request.urlopen(url)
				scoreboard = pbp.json(url, base_url, base_path)
				for game in range(0, len(scoreboard["contests"])):
					gid = str(scoreboard["contests"][game]["id"])
					url = "".join((base_url, "gameflash/", mid_url, gid, "_playbyplay.json"))
					game_urls.append(url)
				urls[conference] = game_urls
				print("Received", date, conference, "game urls")
				continue
	return(urls)

# Write headers into csv file
with open ("../data/csv/headers.csv", "w", newline="") as outputfile:
	fields = (#"date",
		#"gid",
		"half",
		"time-minutes",
		"time-seconds",
		"details",
		"player1-id",
		"player2-id",
		"player1-linkable",
		"player2-linkable",
		"player3-linkable",
		"player-first-name-1",
		"player-first-name-2",
		"player-last-name-1",
		"player-last-name-2",
		"player-team-alias-1",
		"player-team-alias-2",
		"home-score",
		"visitor-score",
		"visitor-fouls",
		"home-fouls",
		"player-fouls",
		"fastbreak",
		"in-paint",
		"second-chance",
		"off-turnover",
		"player-score",
		"points-type",
		"detail-id",
		"detail-desc",
		"event-id",
		"event-desc",
		"distance",
		"x-coord",
		"y-coord",
		"team-id-1",
		"team-id-2",
		"team-id-3")
	header_csv = csv.writer(outputfile, delimiter=",")
	header_csv.writerow(fields)

# Write game_urls into csv file
def export_urls_to_csv(urls):
	with open ("../data/csv/games.csv", "w", newline="") as outputfile:
		game_csv = csv.writer(outputfile, delimiter=",")
		for url in urls:
			game_csv.writerow([url])

# Write pbp data into csv files
def export_pbp_to_csv(urls, base_url, base_path):
	for url in urls:
		req = urllib.request.Request(url)
		try:
			urllib.request.urlopen(req)
		except urllib.error.HTTPError as e:
			print("Error code:", e.code, "- Could not read", url)
			continue
		except urllib.error.URLError as e:
			print("We failed to reach a server.")
			print("Reason: ", e.reason)
			continue
		else: 
			data = pbp.json(url, base_url, base_path)
			#gid = data["playbyplay"]["contest"]["id"]
			hometeam = data["playbyplay"]["contest"]["team"][0]["four-letter-abbr"]
			awayteam = data["playbyplay"]["contest"]["team"][1]["four-letter-abbr"]
			date = url[74:84].replace("/","")
			filename = date+"_"+hometeam+"_"+awayteam+".csv"
			if (data["playbyplay"]["gamestate"]["status"] == "PROG"):
				print("In progress", date, hometeam, awayteam, "wait till game is completed...")
			else:
				with open(base_path + filename, "w", newline="") as outputfile:
					pbp_csv = csv.writer(outputfile, delimiter=",")
					headers = csv.DictReader(open("../data/csv/headers.csv", "r"))
					pbp_csv.writerow(headers.fieldnames)
					for play in range(0, len(data["playbyplay"]["plays"]["play"])):
						play = data["playbyplay"]["plays"]["play"][play]
						row = []
						for col in headers.fieldnames:
							row.append(play[col])
						pbp_csv.writerow(row)
					print("Done writing", date, hometeam, awayteam, ".csv")

#scoreboard_url = "http://data.sportsillustrated.cnn.com/jsonp/basketball/ncaa/men/scoreboards/ncaa64/2014/03/23/scoreboard.json"
#pbp_url = "http://data.sportsillustrated.cnn.com/jsonp/basketball/ncaa/men/gameflash/2014/03/23/93932_playbyplay.json"
base_url = "http://data.sportsillustrated.cnn.com/jsonp/basketball/ncaa/men/";
base_path = "../data/";
start_date = "2014-04-05" # What happened on 2014-02-18? And 2014-03-01?
end_date = "2014-04-07" # 2014-03-16
conferences = ["nit","ncaa64"] # ncaa64, nit, big10, acc, big12, bige, pac12, sec, aac
midmajors = ["aeast","atl10","atsun","bigw","bsky","bsou","coln","cusa","horiz","indp","ivy","maac","mac","meac","mvc","mwest","nec","ovc","patr","sbelt","sland","south","sum","swac","wac","wcc"]
urls = get_conference_game_urls(start_date, end_date, conferences, base_url, base_path)
#print(urls)

# Write pbp data into csv files in respective conference directories
for conference in conferences:
	base_path = "../data/csv/"+conference+"/"
	if not os.path.exists(base_path):
		os.makedirs(base_path)
	print("Reading", conference, "games...")
	export_pbp_to_csv(urls[conference], base_url, base_path) # export_urls_to_csv(urls)