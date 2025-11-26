# ED Router

## Contents

- [Setup](#setup)
    - [Python](#python)
    - [exe build from Python](#python-to-exe-build)
    - [.exe standalone](#exe-standalone)
- [Usage](#usage)
    - [Python](#python1)
    - [.exe standalone](#exe)
- [Notes](#notes)

## Setup
### Python 
Requires [Python 3.x](https://www.python.org/downloads/) and the [Requests library](https://requests.readthedocs.io/en/latest/) as well as the [Dotenv library](https://pypi.org/project/python-dotenv/)
- Open your favourite flavour of console
- Navigate to where you want to clone the repository
- Run `git clone https://github.com/hotwraith/ed-router`
- Run `cd ed-router`

**OR**

- Download the `python_standalone.zip` archive
- Extract it (always keep the `systems.txt` at the same level than `router.py`)

### Python to .exe build
Requires [Pyinstaller](https://pyinstaller.org/en/stable/) as well as the aformentioned requirements

- Open your favourite flavour of console
- Navigate to where you want to clone the repository
- Run `git clone https://github.com/hotwraith/ed-router`
- Run `cd ed-router`
- Run `python build.py`
- The script will ask you for a version name, the current one is [there](https://github.com/hotwraith/ed-router/releases/latest) but this doesn't really matter
- The result should then appear under `dist\version_number`, you can copy this directory wherever you want to use it
- The usage is identical to the one described for the [.exe standalone](#exe)

### .exe standalone

- [Download the installer](https://github.com/hotwraith/ed-router/releases/latest)
- Run the installer, keep the shortcuts, they're useful
- Tadam

## Usage

### Python

- Edit `systems.txt` to add the systems you want in your route
    - The first system will be your departure, be careful of which one you put first
    - The [`systems_example.txt`](https://github.com/hotwraith/ed-router/blob/main/systems_example.txt) file contains an example route
- Open your favourite flavour of console
- run `python path/to/router.py`
    - add `--loop`, `-l` to: make the route loop back to your starting system
    - add `--json`, `-j` to: output a `route.json` file with the jumps
    - add `--spansh`, `-s` to: output a `spansh_route.txt` file uploadable to [Spansh](https://spansh.co.uk/)
    - add `--txt`, `-t` to: turn off the `route.txt` output
    - add `--greedy`, `-g` to: use a greedy algorithm when searching for routes
    - add `-d`, `--debug` to: triggers debug logging when an error is catched
    - add `-c n`, `--crash n` to: print the nth most recent crash log, where n must be an integer between 0 and the number of crash logs you have (the script will tell you how many you have if you input a number too big). 0 will print the most recent crash log.
    - add `-h`, `--help` to: display the help message about args

### .exe

- By default the app will try to store the outputs in your downloads folder, you can choose to change this if you want to
- The left hand side is the equivalent of `systems.txt` described elsewhere in the documentation, the right hand side is the equivalent of the output `route.txt` described elsewhere in the documentation
- The options available are equivalent to `--loop`, `--json`, `--spansh` and `--greedy` described above
- If the display on the right doesn't work, try to:
    - Check if you didn't make a typo in system names or left blank lines, this breaks the router
    - Change the output location
    - Restart the app
    - If none of these things work you can [create an issue](https://github.com/hotwraith/ed-router/issues/new), where you describe your issue more in detail

## Notes

- By default the script will try to store temporary and persistent data in `~\AppData\Local\ed-router\`.
    - `temp` only contains temporary files that are replaced/rewritten each time the router is ran.
    - `persistent` contains some permanent/semi-permanent file to optimize the router/log errors:
        - `all_sys.json`: a local copy of all systems you've ever put through the router to diminish the number of requests to EDSM's API, unless you plan on routing between the entirety of systems in EDSM's database the file size should stay relatively small
        - `crash.txt`: Contains crash reports and time of crashes of when the router failed, using the `-c` option while running the router allows to nicely print those errors in your console to understand the issue better (more often than never it'll be a spelling error in a name you put in `systems.txt`)

- By default the app (`.exe`) version will try to store outputs in `~\Downloads\`