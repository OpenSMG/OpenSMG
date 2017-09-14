from PySide.QtGui import QFrame, QLabel, QComboBox, QPushButton,\
    QVBoxLayout, QFormLayout
import messages
import SMG
from smgLogger import logger
import identifiers
from Configuration import get_config

configuration = get_config("config/config.json")


class UiMusicPlayersFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # widgets
        self.app_select_box = QComboBox(self)

        self.selector_lbl        = QLabel('Select your music player: ')
        self.current_playing_lbl = QLabel('Current playing song: ')
        self.current_playing     = QLabel(configuration['misc']['no_song_playing'])

        self.misc_messages = QLabel(self)
        self.misc_messages.setText(messages.random_message())
        self.misc_messages.setOpenExternalLinks(True)
        self.misc_messages.setWordWrap(True)

        self.repopulate_app_select_box()

        self.start_btn = QPushButton('Start')
        # self.start_btn.resize(10, 30)

        # layout
        self.mainLayout = QVBoxLayout(self)

        self.formLayout = QFormLayout()
        self.formLayout.addRow(self.selector_lbl, self.app_select_box)
        self.formLayout.addRow(self.current_playing_lbl, self.current_playing)

        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addWidget(self.misc_messages)
        self.mainLayout.addWidget(self.start_btn)
        self.mainLayout.addSpacing(100)

        # signals
        SMG.smg.songChanged.connect(self.change_song)
        self.app_select_box.activated[str].connect(self.select_new_app)
        self.start_btn.clicked.connect(self.start)

        self.startup()


    def startup(self):
        '''called on startup of smgui'''

        try:
            last_active_player = configuration['startup']['last_active_player']
        except KeyError:
            last_active_player = None

        logger.info("last active player was {}".format(last_active_player))

        if last_active_player:
            program = identifiers.find_application_by_name(last_active_player)
            self.app_select_box.setCurrentIndex(self.app_select_box.findText(program.name))
            SMG.smg.select_program(program)
            if program.startup and self.app_select_box.count() > 1:
                self.start()

        try:
            first_time = configuration['startup']['first_time']
        except KeyError:
            first_time = None

        if first_time == 'True':
            configuration["misc"]["hasntUpdated"] = 0
            configuration.save()
            self.misc_messages.setText(messages.first_time)


    def change_song(self, new_song):
        '''Shows the current playing song in the gui'''
        self.current_playing.setText(new_song)


    def repopulate_app_select_box(self):
        ''' Clears the application selection ComboBox and then refills it with
            one empty field and all currently activated programs.
        '''
        self.app_select_box.clear()
        self.app_select_box.addItem(None)

        apps = sorted(identifiers.APPS, key=lambda a: a.name.lower())

        for app in apps:
            self.app_select_box.addItem(app.name)


    def start(self):
        '''Called when the start button is clicked, will start or stop the program
        depending on what it was previously doing, also alters the start button text'''
        if SMG.smg.selected_program:
            if not SMG.smg.running:
                self.start_btn.setText('Stop')
                self.app_select_box.setDisabled(True)
            else:
                self.start_btn.setText('Start')
                self.app_select_box.setDisabled(False)
            SMG.smg.toggle_running()


    def select_new_app(self, program_name):
        ''' Sets the new application to check for '''
        if program_name:
            program = identifiers.find_application_by_name(program_name)
            SMG.smg.select_program(program)
            if program.needsGroovemarklet:
                self.misc_messages.setText(messages.get_groovemarklet)
            if program.name == 'Zune' or program.name == 'Windows media player':
                self.misc_messages.setText(messages.windows_message)
            if program.name == 'Spotify after update':
                logger.info(messages.new_spotify_message + "l")
                self.misc_messages.setText(messages.new_spotify_message)
            if program.name == 'Media Player Classic Home Cinema':
                self.misc_messages.setText(messages.MPCHC_message)
            configuration['startup']['last_active_player'] = program.name
            configuration.save()
