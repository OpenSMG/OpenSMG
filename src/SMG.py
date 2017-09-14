import win32gui
import pywintypes
import time
import os
from PySide.QtCore import QThread, QObject, Signal
import pythoncom
import ProgramSkeleton
import Configuration
programSkeleton = ProgramSkeleton.ProgramSkeleton()
configuration = Configuration.get_config("config/config.json")
import identifiers
from smgLogger import logger
from TitleModifier import TitleModifier
from atomicFileIO import open_atomic
from enum import Enum


class SMGModes(Enum):
    # normal mode enumerates over all open windows
    # looking for music players
    NORMAL = 1
    # some music players are unfindable by
    # enumerating windows
    # these music players have custom identifier functions
    # they communicate with an API, Windows COM or perhaps something
    # else even.
    CUSTOM = 2
    # web mode will try to communicate with the smg websockets plugin
    WEB = 3


class MainProgramLoop(QObject):
    finished = Signal()

    def __init__(self):
        super().__init__()
        self.running = True


    def long_running(self):
        """
        Calls smg.enum_windows every config.refresh_rate seconds, will emit a finished
        signal when it is stopped.
        """
        # CoInitialize makes threads "work" with win32com. I don't know to what extent this "work" is.
        # but I know it "works".
        # ;_;
        pythoncom.CoInitialize()
        time_now = time.time()
        smg.execute_identify()
        refresh_rate = configuration["misc"]["refresh_rate"]
        while self.running:
            if time.time() >= time_now + refresh_rate:
                smg.execute_identify()
                time_now = time.time()
            time.sleep(0.05)
        logger.info('Worker finished')
        self.finished.emit()


    def stop(self):
        """
        Stops the main loop so this worker will emit a finished signal.
        """
        self.running = False


class SMG(QObject):
    songChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self.titleModifier     = TitleModifier(configuration)
        self.mode              = SMGModes.NORMAL
        self.selected_program  = None
        self.running           = False
        self.thread            = QThread()
        self.worker            = None

    def select_program(self, app):
        """Sets the currently selected program.
        @param app: an application
        @type app: <type 'App'>
        """

        self.selected_program = app
        self.mode = SMGModes.NORMAL

        if app.type == 'misc_music_player':
            self.mode = SMGModes.CUSTOM

    def start(self):
        """
        Start enumerating over windows
        """
        self.worker = MainProgramLoop()
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.thread.quit)
        self.thread.started.connect(self.worker.long_running)
        self.thread.start()

    def stop(self):
        """
        Stop enumerating over windows
        """
        self.worker.stop()
        self.write(configuration['misc']['no_song_playing'])

    def enum_windows(self):
        """
        Enumerate over all windows, calls self.examine_window
        """
        try:
            win32gui.EnumWindows(self.examine_window, None)
        except pywintypes.error:
            # SMG has already exited?
            pass

    def toggle_running(self):
        """
        Toggle the running variable on or off, and call self.stop or self.start accordingly.
        """
        if self.running:
            self.stop()
        else:
            self.start()
        self.running = not (self.running)

    def write(self, title):
        """
        Write a string to the current_song.txt file
        If the song name differs from last tick, Emit a signal that the song name has changed.
        @param title: The title to write
        """
        if title:
            filepath = os.path.join(configuration['directories']['output_directory'], 'current_song.txt')
            if not self.read() == title:
                self.songChanged.emit(title)

                with open_atomic(filepath, 'w', encoding='utf-8') as f:
                    logger.info("writing {}".format(title))
                    f.write(title)

    @staticmethod
    def read():
        """ Reads and returns what's in the current_song.txt"""
        filepath = os.path.join(configuration['directories']['output_directory'], 'current_song.txt')

        try:
            with open(filepath, encoding='utf-8') as f:
                string = f.read()
                return string
        except IOError:
            pass

    def execute_identify(self):
        if self.mode == SMGModes.NORMAL:
            self.enum_windows()
        elif self.mode == SMGModes.CUSTOM:
            title = self.selected_program.identify()
            if title:
                self.write(self.titleModifier.modify_title(title))

    def examine_window(self, hwnd, extra):
        """
        This function will be called for each window the win32gui.EnumWindows can find.
        It takes the window's title and the window's classname and matches it against
        a function associated with the currently selected program.
        If it matches, it will call write to update the title in the gui and in the file.

        @param hwnd: A window handle ID
        @param extra: This is a parameter required by win32gui.EnumWindows, it probably has something to do
        with lower programming languages, here we don't need it, so we don't use it.
        """
        try:
            window_title = win32gui.GetWindowText(hwnd)
            window_class = win32gui.GetClassName(hwnd)
            title = ''
        except:
            # unknown error
            return False

        if self.selected_program.type == 'music_player':
            title = self.selected_program.identify(window_title, window_class)
        elif self.selected_program.type == 'web_music_player':
            for browser in identifiers.BROWSERS:
                browser_title = browser.identify(window_title, window_class)
                if browser_title:
                    title = self.selected_program.identify(browser_title, window_class)
                    continue
        if title:
            self.write(self.titleModifier.modify_title(title))

    @staticmethod
    def find_application_by_name(name):
        """
        Looks for an application by name. Will return the application if it's found.
        @param name: The name of an <type 'App'> to find
        @type name: <type 'String'>
        @return: An application
        @rtype: <type 'App'>
        """
        for application in identifiers.APPS:
            if name == application.name:
                return application

smg = SMG()
