from PySide.QtGui import QLineEdit, QFrame, QLabel, QPushButton,\
    QFileDialog, QFont, QVBoxLayout, QHBoxLayout, QCheckBox, QLayout
from PySide.QtCore import Signal, Qt
from Configuration import get_config
from smgLogger import logger
import os

configuration = get_config("config/config.json")


class UiOptionsFrame(QFrame):
    item_switched = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # widgets
        self.output_dir_lbl = QLabel('Change Output Directory: ')
        self.select_output_dir_btn = QPushButton('...')

        self.output_cur_dir_lbl = QLineEdit(configuration['directories']['output_directory'])
        self.output_cur_dir_lbl.setReadOnly(True)

        self.no_song_playing_label = QLabel("No song playing text: ")

        self.no_song_playing_input = QLineEdit(configuration['misc']['no_song_playing'])

        self.no_song_playing_label.setToolTip('This is the text that appears when smg can\'t find a song')
        self.no_song_playing_input.setToolTip('This is the text that appears when smg can\'t find a song')

        self.minimize_on_startup_label = QLabel("Minimize SMG on startup: ")
        self.minimize_on_startup = QCheckBox()
        if configuration['gui']['startminimized']:
            self.minimize_on_startup.setCheckState(Qt.CheckState.Checked)
        else:
            self.minimize_on_startup.setCheckState(Qt.CheckState.Unchecked)

        # layout
        self.mainLayout = QVBoxLayout(self)

        self.changeOutputDirectoryLayout = QHBoxLayout()
        self.changeOutputDirectoryLayout.addWidget(self.output_dir_lbl)
        self.changeOutputDirectoryLayout.addWidget(self.select_output_dir_btn)
        self.changeOutputDirectoryLayout.addWidget(self.output_cur_dir_lbl)

        self.noSongPlayingLayout = QHBoxLayout()
        self.noSongPlayingLayout.addWidget(self.no_song_playing_label)
        self.noSongPlayingLayout.addWidget(self.no_song_playing_input)

        self.minimize_on_startup_layout = QHBoxLayout()
        self.minimize_on_startup_layout.addWidget(self.minimize_on_startup_label)
        self.minimize_on_startup_layout.addWidget(self.minimize_on_startup)
        self.minimize_on_startup_layout.setSizeConstraint(QLayout.SetFixedSize)

        self.mainLayout.addLayout(self.changeOutputDirectoryLayout)
        self.mainLayout.addLayout(self.noSongPlayingLayout)
        self.mainLayout.addLayout(self.minimize_on_startup_layout)
        self.mainLayout.addStretch(1)

        # signals
        self.select_output_dir_btn.clicked.connect(self.disp_dialog)
        self.no_song_playing_input.textChanged.connect(self.change_no_song_playing)
        self.minimize_on_startup.stateChanged.connect(self.minimize_on_startup_toggled)

    def disp_dialog(self):
        '''  displays the dialog which selects a directory for output. '''
        dirname = QFileDialog().getExistingDirectory()
        configuration["directories"]["output_directory"] = dirname
        open(os.path.join(dirname, "current_song.txt"), 'w', encoding='utf-8').close()
        configuration.save()
        self.output_cur_dir_lbl.setText(dirname)

    def change_no_song_playing(self, text):
        configuration['misc']['no_song_playing'] = text
        configuration.save()

    def minimize_on_startup_toggled(self, state):
        configuration['gui']['startminimized'] = bool(state)
        configuration.save()
