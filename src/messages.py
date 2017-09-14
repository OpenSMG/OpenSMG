from random import choice, randint
from smgLogger import logger

import time

no_song_playing     = "No song is currently playing"
first_time          = "Since this is your first time using SMG <a href='http://www.youtube.com/watch?v=2yeSfw4iJrw'>watch the introduction video</a>!"
get_groovemarklet   = "This music player requires the <a href='http://martijnbrekelmans.com/SMG/smg_web.php'>browser plugin</a>! Otherwise it won't work :("
visit_forums        = "Stop by the forums if you need any additional help. <a href='http://www.obsproject.com/forum/viewtopic.php?f=22&t=4223'>OBS</a>."
windows_message     = 'WMP and Zune also unlikely to work at all on Windows 7 or higher, try running in Administrator mode Fixes will come later'
new_spotify_message = 'Spotify support is finally here! Pause and play your song in Spotify to start getting spotify\'s song'
MPCHC_message       = 'MPC-HC gets the song name from the song\'s filename, they can be incorrect.'

def timeOfDayMessage():
    hour = time.localtime().tm_hour

    if hour >= 0 and hour < 6:
        return "Nightowl! (don't play loud music!)"
    elif hour > 6 and hour < 12:
        return "Good morning, time for SMG!"
    elif hour > 12 and hour < 18:
        return "Have a nice afternoon"
    elif hour > 18 and hour <= 24:
        return "Have a nice evening                    :)"

commonMessages = [
    'For feedback, questions or bug reports, contact us at smg@martijnbrekelmans.com',
    "Have any suggestions? Stop by the <a href='http://www.obsproject.com/forum/viewtopic.php?f=22&t=4223'>obsforums</a> or send us an email.",
    "Something's not working right? Remove the configuration folder and restart smg.",
    'Found a bug? Send us an email, smg@martijnbrekelmans.com',
    "Your player isn't supported? Send us an email, smg@martijnbrekelmans.com",
    'Have a good day! :)',
    'Thanks for using smg.',
    'This program was made by Streamsoft.',
    'You can enable and disable music apps in the Options tab!',
    'You can change your output directory in the Options tab!',
    "Want darude :: songstorm instead of darude - songstorm? Check out the edit tab!",
    "Spotify used to be unsupported by all music programs for over 2 months!",
    "Did you know music makes plants grow faster?",
    "Did you know Astronaut Chris Hadfield recorded an album in space?",
    "Did you know that over 1500 people use SMG?",
    timeOfDayMessage(),
]

uncommonMessages = [
    "There's a 1 in 60 chance that smg will say your currently playing song is 'darude sandstorm'",
    "One of the messages that can appear here is a lie!"
]

def update_message(hasntUpdatedForSoManyTimes):
    logger.info(hasntUpdatedForSoManyTimes)

    if hasntUpdatedForSoManyTimes < 1:
        return "Hey, there's an update available.. <a href='http://martijnbrekelmans.com/SMG/download.php'>get it here!</a>"
    elif 1 < hasntUpdatedForSoManyTimes < 5:
        return "Pssh, there's an <a href='http://martijnbrekelmans.com/SMG/download.php'>update</a>"
    elif 5 < hasntUpdatedForSoManyTimes < 10:
        return "You should really <a href='http://martijnbrekelmans.com/SMG/download.php'>update</a>"
    elif 10 < hasntUpdatedForSoManyTimes < 25:
        return "SMG is feeling old, consider <a href='http://martijnbrekelmans.com/SMG/download.php'>updating!</a>"
    elif hasntUpdatedForSoManyTimes > 25:
        return "Woah, you haven't updated for so long :( <a href='http://martijnbrekelmans.com/SMG/download.php'>you can update me here!</a>"


def random_message():
    n = randint(1, 3)
    if n < 3:
        return choice(commonMessages)
    elif n == 3:
        return choice(uncommonMessages)
