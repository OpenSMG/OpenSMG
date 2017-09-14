import types
import re
import json
import os
# enable this import if you want to play around with zune
# and or windows media player, see commented code below
import pywintypes
import win32com
import win32com.client
import helpers
from smgLogger import logger

APPS = []
BROWSERS = []

class App:
    def __init__(self, parameters):
        '''
        Init takes one dictionary with the following parameters.

        @param identifiers: A list containing one or more windows title identifiers.
        A window title is the title of a window in windows, usually this
        text is used as the title on the application bar (the one with minimize, maximize and close)
        @param window_class_name: optional, name of the window class.
        @param gui_name: What will show up in the list of selectable programs in the GUI
        A window class is the name of a window in windows (windows windows windows)
        @param identify: Optional, a replacement function for the standard identify.
        @param replace_title: Optional, toggle on or off if identify should
        replace the identifier in the title with nothing or not.

        Note that optional parameters will NOT function when you replace the identify function by
        specifying the identify parameter.
        '''
        self.name              = parameters['name']
        self.type              = parameters['apptype']
        self.identifiers       = parameters.get('identifiers', [])
        self.replace_title     = parameters.get('replace_title', True)
        self.window_class_name = parameters.get('window_class_name', '')
        self.remove_characters = parameters.get('remove_characters', [])
        self.gui_name          = parameters.get('gui_name', self.name)
        self.startup           = parameters.get('startup', True)

        self.needsGroovemarklet = False
        if parameters['apptype'] == 'web_music_player':
            # true by default, false if so specified
            if "needsGroovemarklet" not in parameters.keys():
                self.needsGroovemarklet = True

        try:
            if not parameters['apptype'] == 'webbrowser':
                APPS.append(self)
        except KeyError:
            pass

        try:
            self.identify = types.MethodType(parameters['identify'], App)
        except KeyError:
            pass


    def identify(self, title, window_class_name):
        '''Takes any window title (or any string, really) and tries to match it
        to some conditions, if it\'s correctly matched, the title will be returned.
        If not, it will return False.

        Valid title example: "Spotify - some song by some band",
         this contains a clearly identifyable music player (spotify)
        Invalid title example: "Python 3.3.2 Shell",
         contains no identifyable music player.

        @param title: The title of a window
        @param window_class_name: optional, can be empty. The class name of a window.
        '''
        for identifier in self.identifiers:
            for string in self.remove_characters:
                title = title.replace(string, '')

            if identifier in title and self.window_class_name in window_class_name:
                if self.replace_title:
                    title = title.replace(identifier, '')

                return title

        return False


    def __repr__(self):
        return "{type} {name}".format(type=self.type, name=self.name)


class Browser(App):
    '''Almost the same as an App, but will append itself to BROWSERS
        instead of APPS'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        BROWSERS.append(self)


def _mediamonkey_identify(self, title, window_class_name):
    for identifier in MEDIAMONKEY.identifiers:
        if identifier in title and MEDIAMONKEY.window_class_name in window_class_name:
            title = title.replace(identifier, '')
            title = title[title.find(' ') + 1:]
            return title

    return False


def _winamp_identify(self, title, window_class_name):
    for identifier in WINAMP.identifiers:
        # winamp has numbers in front of its text, probably for albums and stuff
        # ex:
        # 1. Goddess - Hania Lee
        # 2. Suicide - Hania Lee
        #
        # The regex removes these numbers and turns them into
        # Goddess - Hania Lee
        # etc...
        if identifier in title and WINAMP.window_class_name in window_class_name:
            title = title.replace(identifier, '')
            title = re.sub('^[0-9]+\. ', '', title)
            return title

    return False


def _foobar_identify(self, title, window_class_name):
    for identifier in FOOBAR.identifiers:
        if identifier in title and FOOBAR.window_class_name in window_class_name:
            title  = title[:title.find(identifier)]
            first  = title.find('[')
            second = title.find(']')
            title  = title[:first] + title[second + 1:]

            # there's a bug with foobar that the title is doubled
            # check if the title length is even, and then check if the first half
            # and second half are the same
            # additionally, sometimes foobar might double the text and add a space at the end
            # check for that as well
            if helpers.isDoubledText(title) or helpers.isDoubledText(title[:-1]):
                logger.info("detected double title @ foobar")
                # return the first half if double title is detected.
                return title[int(len(title)/2):]

            return title

    return False


def _jrivermp_identify(self):
    ''' uses the jriver api to find song name + artist '''
    jriver = win32com.client.Dispatch('MediaJukebox Application')
    playlist = jriver.GetCurPlaylist()
    pos = playlist.position
    track = playlist.GetFile(pos)
    return track.Name + ' - ' + track.Artist


def _itunes_identify(self):
    ''' Uses the itunes api to find song name + artist '''
    itns = win32com.client.Dispatch('iTunes.Application')

    try:
        name = itns.CurrentTrack.Name
        artist = itns.CurrentTrack.Artist
    except AttributeError:
        return False
    except pywintypes.com_error as e:
        logger.info('itunes: com error; {}'.format(e))
        return False

    return name + ' - ' + artist


# def wmp(self):
#     w = win32com.client.Dispatch('WMPlayer.OCX')
#     # logger.info(w.settings.requestMediaAccessRights)
#     # logger.info(dir(w.settings))
#     playlist = w.Controls
#     s = playlist[0]
#     # logger.info(s.name, s.duration)
#     # return "hello kitty warrior island"
#     for process in psutil.get_process_list():
#         try:
#             if process.name() == 'wmplayer.exe':
#                 files = process.get_open_files()
#                 mp3s = [file.path for file in files if '.mp3' in file.path]
#                 # [logger.info(mp3.split('\\')[-1]) for mp3 in mp3s]
#                 for i in files:
#                     file = i[0]
#                     if '.mp3' in file:
#                         title = file.split('\\')[-1]
#                         return title.replace('.mp3', '')
#         except:
#             # logger.info("Something went wrong during windows media player identifying")
#             pass


# def zune(self):
#     for pid in psutil.pids():
#         process = psutil.Process(pid)
#         if "Zune" in process.name():
#             logger.info("found zune! {}".format(pid))

#     for process in psutil.get_process_list():
#         try:
#             process_name = process.name()
#         except AccessDenied:
#             logger.info("failed getting process.name @ zune media player")

#         if "Zune" in process_name:
#         # if process_name == 'Zune.exe':
#             for i in process.get_open_files():
#                 file = i[0]
#                 if '.mp3' in file:
#                     title = file.split('\\')[-1]
#                     logger.info('starting reading')
#                     file_info = MusicFileInfo.MusicFileInfo(file)
#                     file_info.parse()
#                     logger.info('done reading')
#                     return title.replace('.mp3', '')


def _vlc_identify(self, title, window_class_name):
    # VLC had some problems in the past with multilingual settings, the title differs per language
    # What we do now, is split the title in three parts based on ' - '. And then take everything but the last (which is VLC)
    if 'VLC' in title and window_class_name == 'QWidget':
        text = title.split("-")
        return "-".join(text[:len(text) - 1])
    return None

def _clementine_identify(self, title, window_class_name):
    if 'QWidget' in window_class_name and not 'SMG' in title:
        if re.match('.+ - .+', title):
            return title


def find_application_by_name(name):
    return next(app for app in APPS if app.name == name)


_jrivermp_identify.jriver = None

CHROME                  = Browser({'name': 'Google Chrome',                  'apptype': 'webbrowser',        'identifiers': [' - Google Chrome'] })
CHROME_APPLICATION_MODE = Browser({'name': 'Google Chrome Application mode', 'apptype': 'webbrowser',        'identifiers': ['- Google Chrome'], 'window_class_name': 'Chrome_WidgetWin_1' })
FIREFOX                 = Browser({'name': 'Mozilla Firefox',                'apptype': 'webbrowser',        'identifiers': [' - Mozilla Firefox'] })
FIREFOX_DEV             = Browser({'name': 'Mozilla Firefox Dev edition',    'apptype': 'webbrowser',        'identifiers': [' - Firefox Developer Edition'] })
PALEMOON                = Browser({'name': 'Palemoon',                       'apptype': 'webbrowser',        'identifiers': [' - Pale Moon'] })
OPERA                   = Browser({'name': 'Opera',                          'apptype': 'webbrowser',        'identifiers': [' - Opera'] })
WATERFOX                = Browser({'name': 'Waterfox',                       'apptype': 'webbrowser',        'identifiers': [' - Waterfox']})
VIVALDI                 = Browser({'name': 'Vivaldi',                        'apptype': 'webbrowser',        'identifiers': [''],                'window_class_name': 'Chrome_WidgetWin_1', 'remove_characters': [' - Google Chrome', '- Google Chrome']})

CLEMENTINE              = App({    'name': 'Clementine',                     'apptype': 'music_player',      'identify': _clementine_identify})
VLC                     = App({    'name': 'VLC media player',               'apptype': 'music_player',      'identifiers': ['VLC'], 'window_class_name': 'QWidget', 'identify': _vlc_identify })
MEDIAMONKEY             = App({    'name': 'Media monkey',                   'apptype': 'music_player',      'identifiers': ['- MediaMonkey'], 'identify': _mediamonkey_identify })
WINAMP                  = App({    'name': 'Winamp',                         'apptype': 'music_player',      'identifiers': [' - Winamp'], 'identify': _winamp_identify, 'window_class_name': 'Winamp v1.x'})
FOOBAR                  = App({    'name': 'Foobar2000',                     'apptype': 'music_player',      'identifiers': ['[foobar2000'], 'window_class_name': '{97E27FAA-C0B3-4b8e-A693-ED7881E99FC1}', 'identify': _foobar_identify })
JRIVER                  = App({    'name': 'Jriver media center',            'apptype': 'misc_music_player', 'identify': _jrivermp_identify })
ITUNES                  = App({    'name': 'iTunes',                         'apptype': 'misc_music_player', 'identify': _itunes_identify, 'startup': False })
# WMP                     = App({    'name': 'Windows media player',           'apptype': 'misc_music_player', 'identify': wmp })
# ZUNE                    = App({    'name': 'Zune',                           'apptype': 'misc_music_player', 'identify': zune })

def loadMusicplayers():
    try:
        json_obj = json.load(open(os.path.join('config', 'music_players.json'), encoding='utf-8'))
    except FileNotFoundError:
        json_obj = []

    for music_player in json_obj:
        globals()[music_player] = App(json_obj[music_player])

loadMusicplayers()
