import os
from smgLogger import logger

ROOT = os.getcwd()

BASEURL = "https://martijnbrekelmans.com/SMG/"

VERSION = 2.17
MUSIC_PLAYERS_JSON = """{
    "SPOTIFY": {
        "name": "Spotify desktop",
        "apptype": "music_player",
        "identifiers": [""],
        "window_class_name": "SpotifyMainWindow",
        "remove_characters": ["Spotify -"]
    },
    "AIMP3": {
        "name": "Aimp3",
        "apptype": "music_player",
        "identifiers": [" - "],
        "window_class_name": "TAIMPMainForm",
        "replace_title": false
    },
    "MUSICBEE":  {
        "name": "Musicbee",
        "apptype": "music_player",
        "identifiers": [" - MusicBee"]
    },
    "YOUTUBE": {
        "name": "Youtube",
        "apptype": "web_music_player",
        "identifiers": ["- YouTube", "YouTube - "],
        "remove_characters": ["▶ "],
        "needsGroovemarklet": false
    },
    "GROOVESHARK": {
        "name": "Grooveshark",
        "apptype": "web_music_player",
        "identifiers": ["Grooveshark - "]
    },
    "SOUNDCLOUD": {
        "name": "Soundcloud",
        "apptype": "web_music_player",
        "identifiers": ["Soundcloud - "]
    },
    "PANDORA": {
        "name": "Pandora",
        "apptype": "web_music_player",
        "identifiers": ["Pandora - "]
    },
    "ZAYCEV": {
        "name": "Zaycev",
        "apptype": "web_music_player",
        "identifiers": ["Zaycev - "]
    },
    "PLUGDJ": {
        "name": "Plug.dj",
        "apptype": "web_music_player",
        "identifiers": ["Plug.dj - "]
    },
    "EIGHTTRACKS": {
        "name": "8tracks",
        "apptype": "web_music_player",
        "identifiers": ["8tracks - "]
    },
    "RDIO": {
        "name": "Rdio",
        "apptype": "web_music_player",
        "identifiers": ["Rdio - "]
    },
    "MPC-HC": {
        "name": "Media Player Classic Home Cinema",
        "apptype": "music_player",
        "identifiers": [""],
        "window_class_name": "MediaPlayerClassicW"
    },
    "DEEZER": {
        "name": "Deezer",
        "apptype": "web_music_player",
        "identifiers": ["Deezer - "]
    },
    "OSU": {
        "name": "Osu! (yes, osu)",
        "apptype": "music_player",
        "identifiers": ["osu! - ", "osu!  - "]
    },
    "SPOTIFYWEB": {
        "name": "Spotify web player",
        "apptype": "web_music_player",
        "identifiers": [" - Spotify", "Spotify - "],
        "remove_characters": ["▶ "]
    },
    "MIXCLOUD": {
        "name": "Mixcloud",
        "apptype": "web_music_player",
        "identifiers": ["Mixcloud - "]
    },
    "VKMUSIC": {
        "name": "Vk.com music",
        "apptype": "web_music_player",
        "identifiers": ["Vk - "]
    },
    "DUBTRACK": {
        "name": "dubtrack.fm",
        "apptype": "web_music_player",
        "identifiers": ["Dubtrack - "]
    },
    "MICROSOFTMUSIC": {
        "name": "microsoft.music.com",
        "apptype": "web_music_player",
        "identifiers": ["Microsoft Music - "]
    },
    "NIGHTBOT": {
        "name": "Nightbot song requests",
        "apptype": "web_music_player",
        "identifiers": ["Nightbot - "]
    },
    "LASTFM": {
        "name": "Last.fm",
        "apptype": "web_music_player",
        "identifiers": ["Last.fm - "]
    },
    "DIFM": {
        "name": "Digitally Imported - di.fm",
        "apptype": "web_music_player",
        "identifiers": ["DI.fm - "]
    },
    "GOOGLEPLAYMUSIC": {
        "name": "Google play music",
        "apptype": "web_music_player",
        "identifiers": [" - Google Play", "Google Play - ", "Driveplayer - "]
    },
    "NICOVIDEO": {
        "name": "Nicovideo",
        "apptype": "web_music_player",
        "identifiers": [" - Niconico Video:GINZA",  "- Niconico Video", "Niconico Video - "]
    },
    "QQMUSIC": {
        "name": "QQ Music",
        "apptype": "web_music_player",
        "identifiers": ["QQMusic - "]
    },
    "PHANTOMBOT": {
        "name": "Phantombot",
        "apptype": "web_music_player",
        "identifiers": ["Phantombot - "]
    },
    "TIDALWEB": {
        "name": "Tidal web player",
        "apptype": "web_music_player",
        "identifiers": ["Tidal - "]
    },
    "TIDAL": {
        "name": "Tidal desktop player",
        "apptype": "music_player",
        "identifiers": [" TIDAL"]
    },
    "NERDBOT": {
        "name": "Nerdbot",
        "apptype": "web_music_player",
        "identifiers": ["Nerdbot - "]
    },
    "HYPEMACHINE": {
        "name": "Hypemachine",
        "apptype": "web_music_player",
        "identifiers": ["Hypemachine - "]
    },
    "MELON": {
        "name": "Melon player",
        "apptype": "music_player",
        "identifiers": [" - Melon Player"]
    },
    "AMAZONMUSIC": {
        "name": "Amazon Music",
        "apptype": "web_music_player",
        "identifiers": ["Amazon music - "]
    },
    "GOOGLEPLAYMUSICDESKTOP": {
        "name": "Google play music desktop (community)",
        "window_class_name": "Chrome_WidgetWin_1",
        "apptype": "music_player",
        "identifiers": [" - "],
        "replace_title": false
    }
}"""
