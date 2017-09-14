from smgLogger import logger

def isDoubledText(text):
    # checks if texttext is doubled or not
    # "texttext" -> True
    # "text"     -> False
    return len(text) % 2 == 0 and text[int(len(text)/2):] == text[:int(len(text)/2)]
