import os
import GLOBALS
import requests
from Configuration import get_config
from smgLogger import logger
from urllib.parse import urljoin


configuration = None


class ProgramSkeleton:
    """
    ProgramSkeleton is here to save the day.
    Users often completely fuck up their installations, I don't know how, I don't know why.
    What programskeleton does is check what files and folder are there, and if anything is missing
    it'll repair it.
    """
    def __init__(self):
        global configuration

        try:
            configuration = get_config("config/config.json")
            current_song_path = configuration['directories']['output_directory']
        except:
            current_song_path = "."

        self.structure = {
            current_song_path: [
                ('current_song.txt', self.error_current_song_file)],
            'config': [
                ('music_players.json', self.error_json),
                ('config.json', self.error_config)],
            'resources': [
                ('icon-16.png', self.error_resources),
                ('icon-16.ico', self.error_resources),
                ('icon-32.png', self.error_resources),
                ('icon-60.ico', self.error_resources),
                ('icon-60.png', self.error_resources)]}
        self.root = GLOBALS.ROOT
        self.verify_structure()
        configuration = get_config("config/config.json")


    def get_root(self):
        """
        @return: absolute root to this file
        """
        return self.root

    def verify_structure(self):
        """
        Use self.structure to check for all important files and directories.
        If a directory is missing, it will create the directory.
        If a file is missing, it will fire a function associated with that file missing
        """
        logger.info("Verifying structure")
        for (directory, files) in self.structure.items():
            if not os.path.exists(directory):
                logger.info("dir {}, doesn't exist, creating.".format(directory))
                os.makedirs(directory)
            for (aFile, error) in files:
                filepath = os.path.join(directory, aFile)
                if not os.path.exists(filepath):
                    error(aFile)
                    continue

    def error_current_song_file(self, missingResource):
        current_song_path = os.path.join(
            configuration['directories']['output_directory'], "current_song.txt")
        """Error handler for when current_song.txt is missing, create the file"""
        open(current_song_path, 'w', encoding='utf-8').close()

    def error_config(self, missingResource):
        """Error handler for when config.json is missing, create the file with a default
        configuration"""
        global configuration
        logger.info("configuration file doesn't exist, creating config file")
        configuration = get_config("config/config.json")
        configuration.default_configuration_file()

    def error_resources(self, missingResource):
        """
        Error handler for when any of the icons is missing,
        will download the resource from my website"""
        logger.info('missing resource {}'.format(missingResource))
        logger.info("Downloading {}".format(missingResource))

        # oddly enough, urljoin takes only two params
        # and doesn't support variadic amount of arguments
        url = urljoin(
            urljoin(GLOBALS.BASEURL, 'smg/resources/'),
            missingResource)
        response = requests.get(url)
        directoryPath = os.path.join('resources', missingResource)

        with open(directoryPath, 'wb') as f:
            if response.status_code == requests.codes.ok:
                logger.info("Saving {}".format(missingResource))
                f.write(response.content)

    def error_json(self, missingResource):
        """Error handler for when music_players.json is missing, will create a new one
        with default configuration (located in GLOBALS.MUSIC_PLAYERS_JSON)"""
        path = os.path.join(self.root, 'config', 'music_players.json')
        logger.info("Music players config doesn't exist, creating {}".format(path))
        with open(path, 'w', encoding='utf-8') as f:
            f.write(GLOBALS.MUSIC_PLAYERS_JSON)
