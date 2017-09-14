from hashlib import md5
import os.path
from uuid import getnode as get_mac


def getLicenseKey():
    """ Read license from local file, return none if none was found. """
    if os.path.exists("licenseKey.txt"):
        with open("licenseKey.txt", "r", encoding="utf-8") as f:
            return f.read()
    else:
        return None


def getLicenseParams(licenseKey=""):
    uniqueIdentifier = md5(str(get_mac()).encode('utf-8')).hexdigest()

    if not licenseKey:
        licenseKey = getLicenseKey()

    if licenseKey is None:
        return False

    return {
        "key": licenseKey,
        "hash": uniqueIdentifier
    }
