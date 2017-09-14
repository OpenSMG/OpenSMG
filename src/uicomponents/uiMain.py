from PySide.QtGui import QMainWindow, QTabWidget, QIcon, QSystemTrayIcon,\
    QMessageBox, QMenu, QAction
from PySide.QtCore import Qt, QEvent, QTimer
from PySide import QtGui

import sys
import os

import GLOBALS
from resourceDownloader import downloadedResources
from verifyLicense import verifyLicense

from Configuration import get_config

from uicomponents.musicPlayers    import UiMusicPlayersFrame
from uicomponents.optionsFrame    import UiOptionsFrame
from uicomponents.editOutputFrame import UiEditOutputFrame
from uicomponents.richtextDialog  import QRichTextDialog
from uicomponents.aboutFrame      import UiAboutFrame

from smgLogger import logger

import messages

configuration = get_config("config/config.json")


class UiMain(QMainWindow):

    def __init__(self):
        super().__init__()
        # required for showing an icon in the taskbar
        self.createWinId()
        self.setWindowTitle('SMG Music Display')

        width  = configuration['gui']['centralWindowWidth']
        height = configuration['gui']['centralWindowHeight']

        self.resize(width, height)

        self.setWindowIcon(QIcon(
            os.path.join(GLOBALS.ROOT, 'resources/icon-60.png')))

        self.tabbed_windows = QTabWidget()
        self.tabbed_windows.resize(400, 300)

        # fits the widget automatically to a resized main window
        self.setCentralWidget(self.tabbed_windows)

        self.music_players = UiMusicPlayersFrame(self)
        self.options       = UiOptionsFrame     (self)
        self.output_editor = UiEditOutputFrame  (self)
        self.about         = UiAboutFrame       (self)

        self.tabbed_windows.addTab(self.music_players, 'Music players')
        self.tabbed_windows.addTab(self.options, 'Options')
        self.tabbed_windows.addTab(self.output_editor, 'Edit output')
        self.tabbed_windows.addTab(self.about, 'About')

        # minimize to system tray behavior
        self.createActions()
        self.createTrayIcon()

        if configuration['gui']['startminimized']:
            self.minimizeToSystemTray()
        else:
            self.show()

        self.onStartup()

    def onStartup(self):
        # first, check for license
        if not verifyLicense(self):
            self.askForLicense()

        # second, check for update
        version = downloadedResources.version
        if version > GLOBALS.VERSION:
            startsSinceUpdate = configuration["misc"]["hasntUpdated"]
            logger.info("update available")
            self.music_players.misc_messages.setText(
                messages.update_message(startsSinceUpdate))
            configuration["misc"]["hasntUpdated"] = startsSinceUpdate + 1

    def exitWithError(self, message):
        """
        This method should be called whenever
        you want to exit the program with an error message
        """
        QMessageBox.critical(self, "Error", message)
        sys.exit()

    def licenseActivator(self, message):
        dialog = QRichTextDialog(self)
        dialog.setText(message)
        dialog.setWindowTitle("License activator")
        text, result = dialog.prompt()

        if not result:
            self.exitWithError("You need a license to use smg, check\
<a href='http://martijnbrekelmans.com/SMG'>the site</a> for more details")
        elif verifyLicense(self, text):
            with open("licenseKey.txt", "w", encoding="utf-8") as f:
                f.write(text)
            return True
        else:
            return self.licenseActivator("That was not a valid license, please \
provide a valid license key")

    def askForLicense(self):
        self.licenseActivator("Please paste your license into the textbox below.<br />\
<a href='https://martijnbrekelmans.com/SMG'>. \
Click here to get a license if you don't have one</a>")

    def resizeEvent(self, event):
        configuration['gui']['centralWindowWidth'] = self.width()
        configuration['gui']['centralWindowHeight'] = self.height()

    # *----------------------------------------*
    # |       minimize to system tray          |
    # *----------------------------------------*
    def createActions(self):
        """
        Creates a few Qt actions that can be triggered elsewhere in the code
        """
        self.restoreAction = QAction("&Restore",
                                     self,
                                     triggered=self.restoreFromSystemTray)
        # unsure why, but QtGui.qApp.quit will only work if
        # accessed from QtGui
        # from QtGui import qApp does not work
        # "AttributeError: 'NoneType' object has no attribute 'quit'"
        # might be  some accessor magic going on
        self.quitAction = QAction("&Quit", self, triggered=QtGui.qApp.quit)

    def createTrayIcon(self):
        """Creates the icon and right-click menu for in the system tray"""
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon(os.path.join(GLOBALS.ROOT,
                                                 'resources\\icon-60.png')))
        self.trayIcon.setContextMenu(self.trayIconMenu)

        self.trayIcon.activated.connect(self.onActivated)

    def onActivated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.restoreFromSystemTray()

    def minimizeToSystemTray(self):
        """Minimizes the application to the system tray"""
        self.hide()
        self.trayIcon.show()
        if QSystemTrayIcon.supportsMessages():
            if not configuration['gui']['startminimized']:
                self.trayIcon.showMessage("Still running!",
                                          "SMG will keep running in the background, \
doubleclick to restore",
                                          timeout=10000)
            else:
                self.trayIcon.showMessage("Running in the background",
                                          "Doubleclick SMG's icon to restore",
                                          timeout=2000)

    def restoreFromSystemTray(self):
        """Restores the window from being minimized at the system tray"""
        self.trayIcon.hide()
        self.show()
        self.setWindowState(Qt.WindowActive)

    def changeEvent(self, event):
        """
        Override changeEvent, this event gets called whenever the
        window's state changes.
        E.g. from focused to minimized/closed/maximized etc
        it's used to change the behavior of minimization from minimizing
        to the taskbar to mnimizing to the system tray"""
        if event.type() == QEvent.WindowStateChange:
            event.ignore()
            if self.windowState() & Qt.WindowMinimized:
                # Normally, you should be able to call
                # self.minimizeToSystemTray()
                # but for some reason, calling self.hide() directly
                # (which is what minimizeToSystemTray() does)
                # doesn't actually hide the window
                # instead, really weird behavior gets shown.
                # The window minimizes
                # the taskbar icon dissappears (.hide()) for half a second
                # the taskbar icon immediately reappears
                # (which is what .show would do if it were called)
                # http://stackoverflow.com/questions/16036336/how-to-change-minimize-event-behavior-in-pyqt-or-pyside#comment22942660_16048802
                # "The code above works fine over here, that looks like
                # some OS related issue, try using a QTimer,
                # that would be
                # QtCore.QTimer.singleShot(0, self.close)
                # instead of self.close()"
                QTimer.singleShot(0, self.minimizeToSystemTray)
                return

        # if the statechange was not the desired one as is checked for above,
        # let Qt's default changeEvent handler run
        super().changeEvent(event)
