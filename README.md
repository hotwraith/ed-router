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
Requires [Python 3.x](https://www.python.org/downloads/)
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
    - The [`systems_example.txt`](https://github.com/hotwraith/ed-router/blob/main/systems.txt) file contains an example route
- Open your favourite flavour of console
- run `python path/to/router.py`
    - add `--loop` to: make the route loop back to your starting system
    - add `--json` to: output a `route.json` file with the jumps
    - add `--spansh` to: output a `spansh_route.txt` file uploadable to [Spansh](https://spansh.co.uk/)
    - add `--txt` to: turn off the `route.txt` output

### .exe

- Edit `systems.txt` to add the systems you want in your route
    - The first system will be your departure, be careful of which one you put first
    - The [`systems_example.txt`](https://github.com/hotwraith/ed-router/blob/main/systems.txt) file contains an example route
- Double click `router.exe`
- Output will be in `route.txt`