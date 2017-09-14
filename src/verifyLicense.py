from smgLogger          import logger
from resourceDownloader import downloadedResources, fetchLicenseValidation


def verifyLicense(QParent, license_key=""):
    """ Takes a license key, and checks it against the server. """
    if license_key:
        answer = fetchLicenseValidation(license_key)
    else:
        answer = downloadedResources.validLicense

    print("Verifying license!")
    print("answer is:", answer)

    if "timeout" in answer:
        # This happens at timeouts,
        # if the user is not connected, we'll just assume that she is legit! :o
        return True
    else:
        if answer == "invalid":
            return False
        elif answer == "valid":
            return True
        elif answer == "overused key":
            QParent.exitWithError("This key {key} has been overused, if you are a legitimate user, send me an email at smg@martijnbrekelmans.com".format(key=license_key))
            return False
        else:
            # ???
            logger.info(answer)
            logger.info("this shouldn't happen, server returned an invalid answer, in benefit of the doubt for the user, we'll validate this request")
            return True
