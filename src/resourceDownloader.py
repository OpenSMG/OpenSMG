from threading    import Thread
from licenseUrl   import getLicenseParams
from GLOBALS      import BASEURL
from urllib.parse import urljoin
import queue
import requests


def fetchLicenseValidation(licenseKey=""):
    licenseUrl = urljoin(BASEURL, "check_license.php")
    licenseData = getLicenseParams(licenseKey)
    if not licenseData:
        return "invalid"

    response = requests.get(licenseUrl, params=licenseData, timeout=3)

    try:
        validLicense = response.text
    except:
        validLicense = "timeout"

    return validLicense


class BlockingConcurrentResourceDownloader():
    """
    This class is responsible for downloading all resources
    that need to be downloaded before SMG can run

    It's important that nothing else runs while this is running
    the requests should be blocking.
    This is almost never a good idea, except when checking for
    license validity.

    Features:
    1. Blocks until all requests have finished
    2. Sends all requests concurrently

    Responsibilities:
    1. Parsing responses, yes
       Validating responses, no
       Should only be fetching the data and storing it
       as the right data type.
    """

    def __init__(self):
        # version is float or None
        self.version = None
        # validLicense is
        self.validLicense = False

        answers = queue.Queue()

        versionThread = Thread(target=self.fetchVersion, args=[answers])
        licenseThread = Thread(target=self.fetchLicenseValidation,
                               args=[answers])
        versionThread.start()
        licenseThread.start()
        versionThread.join()
        licenseThread.join()

        while True:
            try:
                answer = answers.get_nowait()
                if "version" in answer:
                    self.version = answer["version"]
                elif "validLicense" in answer:
                    self.validLicense = answer["validLicense"]
            except queue.Empty:
                break

    def fetchVersion(self, answers):
        versionUrl = urljoin(BASEURL, "smgversion.txt")
        try:
            response = requests.get(versionUrl, timeout=3)
            version = float(response.text)
        except:
            version = None

        answers.put({"version": version})

    def fetchLicenseValidation(self, answers):
        validLicense = fetchLicenseValidation()

        answers.put({"validLicense": validLicense})


downloadedResources = BlockingConcurrentResourceDownloader()
