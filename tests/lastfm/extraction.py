"""
This file is a helper.
It takes as input a JSON response from the spotify playlist api, and outputs
testdata for the lastfm test in <filename>

Spotify playlist api response needs to be manually retrieved at the moment
See: https://developer.spotify.com/web-api/get-playlist/

usage: python extraction.py <filename>
"""

import json
import sys

if len(sys.argv) < 2:
	print("usage: python extraction.py <filename>")
	sys.exit()

dataFile = "testsongs.json"
outputFile = sys.argv[1]

with open(dataFile, "r", encoding="utf-8") as f:
	data = json.load(f)

tracks = data["tracks"]["items"]
songs = [{
	"input": "",
	"expected": {
		"name": track["track"].get("name", ""),
		"album": track["track"].get("album", {"name": ""})["name"],
		"artist": track["track"].get("artists", [{"name": ""}])[0].get("name", "")
	}
} for track in tracks]

for song in songs:
	song["input"] = song["expected"]["name"] + " " + song["expected"]["artist"]

with open(outputFile, "w", encoding="utf-8") as f:
	json.dump(songs, f)