SMG is a Windows exclusive application written in 32-bit [Python 3.3.5](https://www.python.org/downloads/release/python-335/)

# Development setup

First of all, install 32-bit Python 3.3.5.
When python's installed, the next step is to install the dependencies. The easiest way to install the dependencies is to use pip, python's package manager.

Python 3.3.5 is the last version of Python that does *not* include pip with the default installation, so you need to install it manually. Download and run [this script](https://bootstrap.pypa.io/get-pip.py) to install pip.

Now to install the dependencies

1. Pywin32 -- `pip install -U pypiwin32`
2. PySide -- `pip install -U PySide`
3. Pyinstaller -- `pip install -U pyinstaller`
4. requests -- `pip install -U requests`

**PyWin32** is a Python interface to the Windows 32 api, which SMG uses to grab titles from Windows to retrieve song names.

**PySide** is a Pythonic port of Qt in which SMG's GUI has been built. You don't have to worry about installing Qt itself, the required Qt dependencies come with `pip install -U PySide`, so you automatically get those.

**Pyinstaller** is used to package SMG up as a .exe, as this is not natively supported by Python.

**requests** is used by SMG to perform HTTP requests.

# SIP dependency

SMG has another dependency called `sip`. Sip is a library used to port large C++ codebases to Python. Unfortunately, due to a bug in PySide and PyQt4, on exit, sip doesn't always clean up all Qt objects properly (freeing freed pointers... why), this prompts a windows error "python.exe has stopped working". In `SMG.py`, "sip.setdestroyonexit(False)" needs to be called just before "sys.exit(app.exec_())".

Installing sip is quite a hassle, it's not available via pip for our chosen python version, so we have to install it manually.

1. Install mingWG (oh yes we need to do some c++ compiling, yay), mingGW needs to be installed with g++ support, MSYS is probably necessary as well
2. Follow these instructions: http://pyqt.sourceforge.net/Docs/sip4/installation.html

It can be a bit complicated. I found a way to compile it. I'm using python 3.4 (64-bit) win32. The win32 part confused the living shit out of me, the 64-bit is true, win32!=32-bit.

Alright, so download sip, extract it, open the folder and open a terminal. I'm not going over how to install Microsoft's dev toolkit, since I honestly don't remember which one I downloaded, try to get the same version as me (14.0). I was unable to get it working with mingw, but if you want to use mingw, I think it's possible to do so, try to look up how to set up the 64-bit mingw environment in your terminal.

```
$ "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC" amd64
$ python configure.py
$ nmake
...
$ nmake install
...
$ done!
```

Where `amd64` means "build for python 64-bit". `python configure.py` generates a makefile. `nmake` is Microsoft's `make`.

Used references:
1. vcvarsall environments: https://msdn.microsoft.com/en-us/library/x4d2c09s.aspx
2. Stackoverflow guide to compiling sip: http://stackoverflow.com/a/40779370/2302759

Note that it is technically possible to run smg without sip at all, the consequences of doing this is that smg will randomly crash on exit fairly often. Another downside is that you'll have to remove two lines of code in `smgui.py`, the `import sip` and `sip.setdestroyonexit(False)` lines. The upside is that this saves you two days. I won't allow this for official smg distributions, but for dev setups it's alright.
# Running SMG

To run SMG, open up a terminal, move to the `SMG/src` folder, and run `python smgui.py`. You will be prompted for a license, if you have access to this readme and project, you should have a license.

Any exceptions produced during runtime will be saved to logs/exceptions.txt

# Creating an executable

To create an executable, I've made a script called 'distribute.py'.
Give it the version number of the new release as an argument.

Usage:
`python distribute.py <version>`

To run the script, you need to have pyinstaller installed `pip install pyinstaller`. The script has two options which it will ask you for, option one is to create a distribution and upload it to the server (what server is configured within distribute.py), this is not recommended unless you are me. The other option is to create a local distribution, within the folder `distributions` it will create a new folder named the version number you gave it. Within this will be a zip file, `SMG.zip` which is what you would normally upload, and a folder `dist`, within this folder you can test out the generated executable, it is the same one as in the generated zip.
