# Groovemarklet testsuite

The groovemarklet testsuite is meant to ensure the stability of the groovemarklet SMG addon.
Groovemarklet uses JQuery in combination with css selectors to find the currently playing music, because online music players tend to change their layout very often, the Groovemarklet often loses compatibility with websites.

So, the goal of this testsuite is to visit each of the supposedly supported websites in the four major browsers, Chrome, Firefox, IE and Opera (no reason to support Safari since SMG is Windows-only).

## So, how does this suite work?

The test suite uses [selenium](http://www.seleniumhq.org/) to automate each of these browsers.

The steps to be taken for each online music players are approximately these, written in pseudo-python

```python
for browser in browsers:
	browserHandle = openWebbrowser(browser)
	for music_player in music_players:
		browserHandle.visit_website(music_player.url)
		# search for a specific song on the website
		searchForSong(browserHandle, music_player)
		playTheSong(browserHandle, music_player)
		startGroovemarklet(browserHandle)
		assertEqual(music_player.expectedSong, getCurrentSongFromGroovemarklet(browserHandle))
```

## How do I run these tests?

### Installation

First, make sure you've installed python and pip as is described in the main readme of this project, then install selenium: `pip install -U selenium`.

Because we're going to test 4 different browsers, of course, all three need to be installed on the computer. Download and install the most recent versions of all four major webbrowsers.

Out of the box, selenium doesn't work with Chrome, you need to install the Chrome webdriver, which you can [get here](https://sites.google.com/a/chromium.org/chromedriver/getting-started).

Similarly for IE, you need to get the IE webdriver, which you can [download here](http://www.seleniumhq.org/download/). Some additional steps need to be taken to get Internet Explorer running with selenium, some security settings need to be adjusted, although I am not too sure which ones.

Of course, Opera needs a separate webdriver as well, you can download it [right here](https://github.com/operasoftware/operachromiumdriver/releases). Get the latest 64-bit version.

### Running

There are no tests yet :(