# This stuff is for exception logging :)
# http://stackoverflow.com/a/16993115/2302759
import os
import sys
import logging
import traceback

exceptionLogger = logging.getLogger(__name__ + "exception")

if not os.path.exists("logs"):
    os.mkdir("logs")

exceptionHandler = logging.FileHandler("logs/exceptions.txt")
exceptionLogger.addHandler(exceptionHandler)


def handle_exception(exc_type, exc_value, exc_traceback):
    # don't handle ctrl-c
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    print(''.join(traceback.format_tb(exc_traceback)))
    print('{0}: {1}'.format(exc_type, exc_value))
    exceptionLogger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

# Expose a logger to the rest of the program, it should be used instead of a print statement
# at top of all files,
# from smgLogger import logger
#
# logger.info/debug/warning/error
logger = logging.getLogger(__name__ + "logging")
handler = logging.FileHandler("logs/logging.txt")
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())

logger.setLevel(logging.INFO)
