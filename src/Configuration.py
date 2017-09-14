import GLOBALS
from smgLogger import logger
# TODO: use atomicFileIO in confy
# from atomicFileIO import open_atomic
from confy import Confy

class Configuration(Confy):
    def __init__(self, filename):
        print("Configuration")
        super().__init__(filename)

        if len(self.keys()) == 0:
            self.default_configuration_file()

    def default_configuration_file(self):
        '''
        This method is called when the config.json file needs to be reset
        It creates config.json with default values.
        '''
        logger.info('creating default config file')

        self['directories'] = {
            'root_directory': GLOBALS.ROOT,
            'output_directory': GLOBALS.ROOT
        }

        self['edit_output'] = {
            'append_state': False,
            'prepend_state': False,
            'filter_state': False,
            'replace_state': False,
            'append': "",
            'prepend': "",
            'filter': "",
            'replace_in': "",
            'replace_out': ""
        }

        self['startup'] = {
            'first_time': True
        }

        self['misc'] = {
            'hasntUpdated': 0,
            'no_song_playing': "No song is currently playing",
            'refresh_rate': 1.5
        }

        self['gui'] = {
            'centralWindowWidth': 400,
            'centralWindowHeight': 300,
            'startminimized': False
        }

        self.save()


_configs = {}


def get_config(filename):
    if filename in _configs:
        return _configs[filename]
    else:
        conf = Configuration(filename)
        _configs[filename] = conf
        return conf
