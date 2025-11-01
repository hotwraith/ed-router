# ED Router

## Contents

- [Setup](#setup)
    - [Python](#python)
    - [.exe standalone](#exe-standalone)
- [Usage](#usage)
    - [Python](#python1)
    - [.exe standalone](#exe)

## Setup
### Python 
Requires [Python 3.x](https://www.python.org/downloads/) and the [Requests library](https://requests.readthedocs.io/en/latest/)
- Open your favourite flavour of console
- Navigate to where you want to clone the repository
- Run `git clone https://github.com/hotwraith/ed-router`
- Run `cd ed-router`

**OR**

- Download the `python_standalone.zip` archive
- Extract it (always keep the `systems.txt` at the same level than `router.py`)

### .exe standalone

Warning: the .exe standalone doesn't allow to use some options, the python version is recommended.

- Download the `exe_standalone.zip` archive
- Extract it (always keep the `systems.txt` at the same level than `router.exe`)

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
    - add `-h`, `--help` to: display the help message about args

### .exe

- Edit `systems.txt` to add the systems you want in your route
    - The first system will be your departure, be careful of which one you put first
    - The [`systems_example.txt`](https://github.com/hotwraith/ed-router/blob/main/systems_example.txt) file contains an example route
- Double click `router.exe`
- Output will be in `route.txt`