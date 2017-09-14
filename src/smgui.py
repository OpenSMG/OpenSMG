import sys
import ctypes
import sip

from PySide.QtGui import QApplication
from smgLogger import logger
from uicomponents.uiMain import UiMain

from Configuration import get_config

configuration = get_config("config/config.json")

logger.info("--------------------")
logger.info("Starting up program!")
logger.info("--------------------")

myappid = 'Azeirah.SMG.Azeirah.15'
if hasattr(ctypes.windll.shell32, 'SetCurrentProcessExplicitAppUserModelID'):
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

app = None

def on_exit():
    app.exec_()
    configuration['startup']['first_time'] = False
    configuration.save()
    logger.info("---------------")
    logger.info("Exiting program")
    logger.info("---------------")
    return 0

def main():
    global app
    app = QApplication(sys.argv)
    UI = UiMain()
    sip.setdestroyonexit(False)
    sys.exit(on_exit())

if __name__ == '__main__':
    main()
