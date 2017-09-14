## Groovemarklet testsuite
## testing wooooh

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import service
import subprocess
import unittest
import time

# chrome requires the chrome webdriver to be running, start it.
subprocess.Popen("chromedriver", stdout=subprocess.PIPE)
opera_webdriver_service = service.Service("operadriver", 1338)

class DigitallyImportedInternetExplorer(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Ie("./IEDriverServer")
        self.setUpGeneral()

    def setUpGeneral(self):
        self.addCleanup(self.browser.quit)
        self.browser.get("https://di.fm")
        time.sleep(3)

    def test_siteExists(self):
        self.assertIn("Digitally Imported", self.browser.title)

    def test_groovemarkletLoads(self):
        # at this point, "a" song should start playing
        self.browser.find_element_by_css_selector("a.tune-in-link").click()
        # Load the groovemarklet
        self.browser.execute_script('(function(){document.body.appendChild(document.createElement("script")).src="https://martijnbrekelmans.com/SMG/groovemarklet-release.js"})()')
        # long sleep to load groovemarklet, we don't want any false negatives
        time.sleep(10)
        self.assertIn("DI.fm - ", self.browser.title)

    def test_songIsRecognized(self):
        # at this point, "a" song should start playing
        self.browser.find_element_by_css_selector("a.tune-in-link").click()
        # Load the groovemarklet
        self.browser.execute_script('(function(){document.body.appendChild(document.createElement("script")).src="https://martijnbrekelmans.com/SMG/groovemarklet-release.js"})()')
        # long sleep to load groovemarklet, we don't want any false negatives
        time.sleep(10)
        self.assertTrue(len(self.browser.title) > len("DI.fm - "))

# class DigitallyImportedFirefox(DigitallyImportedInternetExplorer):
#     def setUp(self):
#         self.browser = webdriver.Firefox()
#         super().setUpGeneral()

# class DigitallyImportedChrome(DigitallyImportedInternetExplorer):
#     def setUp(self):
#         self.browser = webdriver.Chrome()
#         super().setUpGeneral()

class DigitallyImportedOpera(DigitallyImportedInternetExplorer):
	def setUp(self):
		# Opera requires that its run as a remote
		self.browser = webdriver.Remote(opera_webdriver_service, {})
		# self.browser = webdriver.Opera()
		super().setUpGeneral()

if __name__ == "__main__":
    unittest.main(verbosity=1)