"""
API test account information:

Application name 	SMG
API key			 	cece9f83caf1b91b78a06680bf295664
Shared secret 		e8118a483c12380abd03856d1e9db3a9
Registered to 		Azeirah

<dataset> is the filename of the dataset you want to test against
the lastfm api
usage: python lastfm.py <dataset>
"""

import pylast
import sys
import json
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

from time import sleep

if len(sys.argv) < 2:
	print("usage: python extraction.py <filename>")
	sys.exit()

dataset = sys.argv[1]

with open(dataset, "r", encoding="utf-8") as f:
	data = json.load(f)

API_KEY = "cece9f83caf1b91b78a06680bf295664"
API_SECRET = "e8118a483c12380abd03856d1e9db3a9"

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

total = len(data)
succeeded = 0
count = 1
failures = []
for track in data:
	sleep(1)

	result = network.search_for_track("", track["input"]).get_next_page()
	# no tracks found similar to search input
	if len(result) == 0:
		count += 1
		failures.append({
			"in": track,
			"out": {
				"name": "Track was not found",
				"artist": "Track was not found"
			}
		})
		continue

	best_match = result[0]

	name, artist = (best_match.get_name(), best_match.get_artist())
	# print("Checking how similar {0} and {1} are".format(
		# name, track["expected"]["name"]))
	if similar(str(name), track["expected"]["name"]) > .7 and similar(str(artist), track["expected"]["artist"]) > .7:
		succeeded += 1
	else:
		failures.append({
			"in": track,
			"out": {
				"name": str(name),
				"artist": str(artist)
			}
		})

	print("{0}: {1} out of {2} succeeded. That's {3}%".format(
		count, succeeded, total, succeeded/total * 100))

	count += 1


reportname = dataset.split(".")[0] + ".txt"
with open(reportname, "w") as f:
	json.dump(failures, f)

print("{0} out of {1} succeeded. That's {2}%".format(
		succeeded, total, succeeded/total * 100))
print("You can find a report of the failures in {0}".format(reportname))