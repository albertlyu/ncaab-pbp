import os
import simplejson as json
import urllib.request
import datetime
import time

# Get dates in range
def get_dates(start_date, end_date):
	start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
	end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
	date_range = end_date - start_date
	dates = []
	for day in range(date_range.days + 1):
		dates.append((start_date + datetime.timedelta(day)).isoformat())
	return(dates)

# Parse JSON for a specific url
def parse_json(url, base_url, base_path):
	fpath = split_url(url, base_url, base_path);
	if os.path.exists(fpath["file_path"]):
		print("JSON already stored on disk")
		if fpath["file_name"] == "scoreboard.json":
			print("Retrieving from file path instead...")
			data = open(fpath["file_path"])
			result = json.load(data)
			return(result)
	else:
		urlRead = urllib.request.urlopen(url).read();
		urlReadClean = urlRead[urlRead.find(b"(")+1:len(urlRead)-2] # strip callbackwrapper so return is valid json
		while True:
			try:
				result = json.loads(urlReadClean)
				break
			except Exception as e:
				bad = str(e)[str(e).rfind("char ")+len("char "):-1]
				bad = int(bad)
				if bad == 0: # if the json is invalid because it"s missing a character, just give up
					result = "Invalid JSON"
					print(result)
					break
				urlReadClean = urlReadClean[:bad-1] + urlReadClean[bad+1:] # escape bad characters so return is valid json
		return(result)
		time.sleep(0.1)

# Split url into components given base_url
def split_url(url, base_url, base_path):
	fpath = {}
	fpath["file_path"] = "".join((base_path, url.replace(base_url, '')));
	fpath["file_name"] = fpath["file_path"].split("/")[-1];
	fpath["dir_path"] = fpath["file_path"].replace(fpath["file_name"], ''); # must be a simpler way to strip file name from file_path
	fpath["year"] = fpath["file_path"].split("/")[-4];
	fpath["month"] = fpath["file_path"].split("/")[-3];
	fpath["day"] = fpath["file_path"].split("/")[-2];
	fpath["mid_path"] = "/".join((fpath["year"], fpath["month"], fpath["day"]));
	fpath["date"] = "-".join((fpath["year"], fpath["month"], fpath["day"]));
	return(fpath)

# Validate url
def validate_url(url):
	req = urllib.request.Request(url)
	filename = url.split("/")[-1]
	try:
		urllib.request.urlopen(req)
	except urllib.error.HTTPError as e:
		print("Error code:", e.code, "-", filename, "does not exist at url")
	except urllib.error.URLError as e:
		print("We failed to reach a server.")
		print("Reason: ", e.reason)
	else:
		return True

# Save JSON data from url to file path
def save_json(url, base_url, base_path):
	fpath = split_url(url, base_url, base_path)
	file_path = fpath["file_path"]
	file_name = fpath["file_name"]
	dir_path = fpath["dir_path"]
	if os.path.isfile(file_path):
		print(file_name, "already exists at", dir_path)
	else:
		if validate_url(url) == True:
			data = parse_json(url, base_url, base_path);
			if not os.path.exists(dir_path): # create path if it does not exist
				os.makedirs(dir_path)
			# Will need to handle both boxscores and playbyplays in progress here
			#if data["boxscore"]["gamestate"]["status"] == "PROG":# or data["playbyplay"]["gamestate"]["status"] == "PROG":
			#	print(file_name, "still in progress, wait till game is completed...")
			else:
				with open (file_path, "w", newline="") as outputfile:
					json.dump(data, outputfile)
					print(file_name, "saved to disk at", dir_path)