import os
import copy
import json
import math
import time
import datetime
import requests
import argparse
import traceback
from itertools import permutations
from dotenv import load_dotenv


def main() -> list[str]:
    try:
        LOCALAPPDATA = os.environ["LOCALAPPDATA"]
    except Exception:
        LOCALAPPDATA = ""
    global fullpath
    fullpath = LOCALAPPDATA
    if "ed-router" not in os.listdir(LOCALAPPDATA):
        fullpath = os.path.join(LOCALAPPDATA, 'ed-router')
        os.mkdir(fullpath)
    else:
        fullpath = os.path.join(LOCALAPPDATA, 'ed-router')
    if 'temp' not in os.listdir(fullpath):
        os.mkdir(os.path.join(fullpath,'temp'))
    if 'persistent' not in os.listdir(fullpath):
        os.mkdir(os.path.join(fullpath,'persistent'))
    if 'all_sys.json' not in os.listdir(os.path.join(fullpath,'persistent')):
        f = open(os.path.join(fullpath,'persistent','all_sys.json'), 'w')
        json.dump({}, f)
        f.close()
    with open('systems.txt', 'r') as f:
        systems = f.readlines()
        f.close()

    if not (isCrash >= 0):
        sys_dict = fetchEDSM(systems)

        with open(os.path.join(fullpath,'temp','sys_info.json'), 'w') as f:
            json.dump(sys_dict, f, indent=4)
            f.close()

        for i in range(len(systems)):
            systems[i] = systems[i].removesuffix('\n')
    
    return systems

def calc() -> None:
    allPaths = {}
    z = 0
    dict_sys = json.load(open(os.path.join(fullpath,'temp','sys_info.json'), 'r'))
    sys_keys = list(dict_sys.keys())
    for i in range(len(sys_keys)):
        for j in range(i+1, len(sys_keys)):
            system1 = dict_sys[sys_keys[i]]
            system2 = dict_sys[sys_keys[j]]
            distance = math.sqrt(math.pow(system1["coords"]["x"]-system2["coords"]["x"],2) + math.pow(system1["coords"]["y"]-system2["coords"]["y"],2) + math.pow(system1["coords"]["z"]-system2["coords"]["z"], 2))
            #print(f"Distance between {system1["name"]} and {system2["name"]}: {round(distance, 2)}lys")
            if(distance > 0):
                allPaths.update({z: {"systems": {0: system1["name"], 1:system2["name"]}, "distance":distance}})
                z += 1

    with open(os.path.join(fullpath,'temp','all_paths.json'), 'w') as f:
        json.dump(allPaths, f, indent=4)
        f.close()

def sortPathBySystem() -> None:
    allPaths = json.load(open(os.path.join(fullpath,'temp','all_paths.json'), 'r'))
    dict_sys = json.load(open(os.path.join(fullpath,'temp','sys_info.json'), 'r'))
    paths_per_system = {}
    for system in list(dict_sys.keys()):
        i=0
        paths_per_system.update({dict_sys[system]["name"]:{}})
        for path in list(allPaths.keys()):
            if((dict_sys[system]["name"] in allPaths[path]["systems"]["0"]) or (dict_sys[system]["name"] in allPaths[path]["systems"]["1"])): 
                paths_per_system[dict_sys[system]["name"]].update({i:allPaths[path]})
                i += 1
    json.dump(paths_per_system, open(os.path.join(fullpath,'temp','min_paths.json'), 'w') ,indent=4)
                    
def fetchEDSM(systems:list[str]) -> dict:
    start = time.time()
    existing_dict = json.load(open(os.path.join(fullpath,'persistent','all_sys.json'), 'r'))
    existing_sys = []
    for el in list(existing_dict.keys()):
        existing_sys.append(el)
    sys_dict = {}
    i=0
    for el in systems:
        clear = el.removesuffix('\n')
        if clear not in existing_sys:
            thisSys = requests.get('https://www.edsm.net/api-v1/system', params={"systemName":clear, "showCoordinates":1}).json()
            if(type(thisSys) is list):
                print(f"\033[31mError when trying to fetch system \"{clear}\" from EDSM API, check spelling in systems.txt\033[0m")
            else:
                sys_dict.update({thisSys["name"]:thisSys})
                existing_dict.update({thisSys["name"]:thisSys})
        else:
            sys_dict.update({el:existing_dict[clear]})
        i+=1
    with open(os.path.join(fullpath,'persistent','all_sys.json'), 'w') as f:
        json.dump(existing_dict, f)
        f.close()
    print(f"Fetching all systems from EDSM api took: {round(time.time()-start,1)}s")
    return sys_dict

def sortPathsByDistance() -> dict:
    systems_path = json.load(open(os.path.join(fullpath,'temp','min_paths.json'), 'r'))
    newDict = {}
    for system in list(systems_path.keys()):
        distance = []
        for path in list(systems_path[system].keys()):
            distance.append([systems_path[system][path]["distance"], systems_path[system][path]["systems"]["0"] , systems_path[system][path]["systems"]["1"]])
        distance.sort()
        newDict.update({system:distance})
    return newDict

def greedy(newDict:dict, departure:str) -> list:
    paths = []
    #departure = list(newDict.keys())[0]
    for i in range(len(list(newDict.keys()))):
        try:
            path = newDict[departure][0]
            paths.append(path)
            newDict = deleter(departure, newDict)
            if(departure == path[1]):
                departure = path[2]
            elif(departure == path[2]):
                departure = path[1]
        except IndexError:
            pass
    return paths

def deleter(system:str, diction:dict)-> dict:
    toRemove = []
    for sys in list(diction.keys()):
        for path in diction[sys]:
            if(system in path):
                toRemove.append(path)

    for el in toRemove:
        for sys in list(diction.keys()):
            try:
                diction[sys].remove(el)
            except ValueError:
                pass
    return diction
        
def findPathByDistance(distances:list[float]) -> list[dict]:
    all_paths = json.load(open(os.path.join(fullpath,'temp','all_paths.json'), 'r'))
    paths = []
    for dist in distances:
        for path in list(all_paths.keys()):
            if(all_paths[path]["distance"] == dist):
                paths.append(all_paths[path])
    return paths

def printPaths(paths:list, departure):
    if(departure == paths[0][1]):
        arrival = paths[0][2]
    elif(departure == paths[0][2]):
        temp = paths[0][1]
        paths[0][1] = departure
        paths[0][2] = temp
        arrival = paths[0][2]
    for i in range(1, len(paths)):
        if(paths[i][1] == arrival):
            departure = paths[i][1]
            arrival = paths[i][2]
        elif(paths[i][2] == arrival):
            temp = paths[i][1]
            paths[i][1] = arrival
            paths[i][2] = temp
            departure = paths[i][1]
            arrival = paths[i][2]

    if(isLoop):
        paths = calcLastLeg(paths)
    if(isSpansh):
        exportSpansh(paths)
    if(isTxt):
        exportTXT(paths)
    if(isJson):
        exportJSON(paths)
    return paths


def otherCalc(systems):
    for i in range(len(systems)):
        systems[i] = systems[i].removesuffix('\n')

    departure = systems[0]

    start = time.time()
    allPaths = searchForAllPaths(departure, systems)
    print(f"Search for all path executed in: {round(time.time()-start, 1)}s")
    i = 0
    start = time.time()
    allPaths = addDeparture(allPaths, departure)
    print(f"Change tuple to list and add departure executed in: {round(time.time()-start, 1)}s")
    
    start = time.time()
    calc()
    dict_sys = json.load(open(os.path.join(fullpath,'temp','all_paths.json'), 'r'))
    for route in allPaths:
        for i in range(len(route)-1):
            route[i] = calc_between_sys(route[i], route[i+1], dict_sys)
        route.pop(-1)
    print(f"Calculate distances for all legs of routes executed in: {round(time.time()-start, 1)}s")
    
    start = time.time()
    totalDistances = calcFullDistance(allPaths)
    print(f"Calculate total route distance executed in: {round(time.time()-start, 1)}s")
    start = time.time()
    index_min = min(range(len(totalDistances)), key=totalDistances.__getitem__)
    print(f"Find minimal route executed in: {round(time.time()-start, 1)}s")
    #print(round(totalDistances[index_min]))
    #print(allPaths[index_min])

    if(isSpansh):
        exportSpansh(list(allPaths[index_min]))
    if(isTxt):
        exportTXT(list(allPaths[index_min]))
    if(isJson):
        exportJSON(list(allPaths[index_min]))
    return allPaths[index_min]
    #with open(fullpath+'spansh_minimal_route.txt', 'w') as f:
    #    for i in range(len(allPaths[index_min])):
    #        f.write(f'{allPaths[index_min][i][1]}\n')
    #    f.close()

def addDeparture(allPaths:list[tuple], departure:str) -> list[list]:
    for i in range(len(allPaths)):
        allPaths[i] = list(allPaths[i])
        if(isLoop):
            allPaths[i].append(departure)
        allPaths[i].insert(0, departure)
    return allPaths #type:ignore


def calcFullDistance(allPaths):
    totalDistances = []
    for route in allPaths:
        distance = 0
        for leg in route:
            distance += leg[0]
        totalDistances.append(distance)
    return totalDistances


def calc_between_sys(sys1, sys2, dict_sys):
    searchSys1, searchSys2 = False, False
    i = -1
    while not (searchSys1 and searchSys2):
        i+=1
        searchSys1, searchSys2 = False, False
        if(dict_sys[str(i)]["systems"]["0"] == sys1):
            searchSys1 = True
        elif(dict_sys[str(i)]["systems"]["0"] == sys2):
            searchSys2 = True
        if(dict_sys[str(i)]["systems"]["1"] == sys1):
            searchSys1 = True
        elif(dict_sys[str(i)]["systems"]["1"] == sys2):
            searchSys2 = True

    distance = dict_sys[str(i)]["distance"]
    
    if(distance > 0):
        return [distance, sys1, sys2]
    return None


def searchForAllPaths(departure, systems:list) -> list[tuple]:
    newsys = copy.deepcopy(systems)
    newsys.remove(departure)
    return list(permutations(newsys))


def exportJSON(paths:list) -> bool:
    try:
        with open(os.path.join(OUTPUT_PATH, "route.json"), 'w') as f:
            dump = {}
            for i in range(len(paths)):
                dump.update({i:paths[i]})
            json.dump(dump, f, indent=4)
            f.close()
        return True
    except Exception as e:
        print(e)
        return False

def exportSpansh(paths:list) -> bool:
    try:
        with open(os.path.join(OUTPUT_PATH, "spansh_route.txt"), 'w') as f:
            for jump in paths:
                f.write(f"{jump[2]}\n")
            f.close()

        return True
    except Exception as e:
        print(e)
        return False

def exportTXT(paths:list) -> bool:
    try:
        with open(os.path.join(OUTPUT_PATH, "route.txt"), 'w') as f:
            for jump in paths:
                f.write(f"{jump[1]} -> {jump[2]} ({round(jump[0])} lys)\n")
            f.write(f"Total distance: {round(calcFullDistance([paths])[0], 2)} lys")
            f.close()

        return True
    except Exception as e:
        print(e)
        return False


def calcLastLeg(paths:list) -> list:
    departure = requests.get('https://www.edsm.net/api-v1/system', params={"systemName":paths[-1][2], "showCoordinates":1}).json()
    arrival = requests.get('https://www.edsm.net/api-v1/system', params={"systemName":paths[0][1], "showCoordinates":1}).json()
    distance = math.sqrt(math.pow(departure["coords"]["x"]-arrival["coords"]["x"],2) + 
                         math.pow(departure["coords"]["y"]-arrival["coords"]["y"],2) + 
                         math.pow(departure["coords"]["z"]-arrival["coords"]["z"], 2))
    if(distance > 0):
        paths.append([distance, departure["name"], arrival["name"]])
    return paths

def printConsole(tentative:list) -> None:
    for el in tentative:
        print(f"{el[1]} to {el[2]} ({round(el[0], 1)}lys)")
    print(f"\033[1mTotal distance: {round(calcFullDistance([tentative])[0], 2)} lys\033[0m")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script that calculates optimal route between multiple Elite: Dangerous star systems")
    parser.add_argument("--loop", "-l", required=False, default=False,  action='store_true', help="This argument makes the route end in your starting system")
    parser.add_argument("--txt", "-t", required=False, default=True,  action='store_false', help="Disables route.txt output")
    parser.add_argument("--json", "-j", required=False, default=False,  action='store_true', help="Enables route.json output")
    parser.add_argument("--spansh", "-s", required=False, default=False,  action='store_true', help="Enables spansh_route.txt output, uploadable directly to Spansh")
    parser.add_argument("--greedy", "-g", required=False, default=False,  action='store_true', help="Uses a greedy algorithm to find a different path")
    parser.add_argument("--first", "-f", required=False, default=False,  action='store_true', help="Deprecated, doesn't do anything")
    parser.add_argument("--debug", "-d", required=False, default=False,  action='store_true', help="Debug log")
    parser.add_argument("--crash", "-c", required=False, default=-1, type=int, help="Will print the nth oldest crash traceback (0 will yield the last crash)")
    args = parser.parse_args()
    global isLoop, isTxt, isJson, isSpansh, isGreedy, isDebug, isCrash
    isLoop, isTxt, isJson, isSpansh, isGreedy, isFirst, isDebug, isCrash = args.loop, args.txt, args.json, args.spansh, args.greedy, args.first, args.debug, args.crash
    load_dotenv()
    global OUTPUT_PATH
    OUTPUT_PATH = os.getenv('OUTPUT_PATH', '')
    systems = main()
    try:
        if(isCrash >= 0):
            with open(os.path.join(fullpath,'persistent','crash.txt')) as f:
                lines = f.readlines()
                if(len(lines) > 0):
                    if(isCrash < len(lines)):
                        index = len(lines) - isCrash - 1
                        error_dict = json.loads(lines[index].removesuffix("\n"))
                        #print(error_dict)
                        error_time = list(error_dict.keys())[0]
                        for el in error_dict[error_time]:
                            print(el+"\n")
                    else:
                        print(f"Please input 0<=n<={len(lines)-1}")
                else:
                    print("No crash logs !")
        else:
            if(len(systems) > 9): #fix: default to greedy algorithm when too much systems are added
                isGreedy = True
                print(f"\033[1mWarning: too many systems ({len(systems)}), defaulted to greedy router\033[0m")
            if not isGreedy:
                tentative = otherCalc(systems)
                print("="*50)
                printConsole(tentative)
                printPaths(tentative, systems[0])
            if(isGreedy):
                isLoopFR = isLoop
                isLoop = True
                calc()
                sortPathBySystem()
                newDict = sortPathsByDistance()
                tentatives = []
                for i in range(len(list(newDict.keys()))):
                    copyDict  = copy.deepcopy(newDict)
                    tentatives.append(greedy(copyDict, list(newDict.keys())[i]))
                for i in range(len(tentatives)):
                    printPaths(tentatives[i], systems[i])

                for i in range(len(tentatives)):
                    while tentatives[i][0][1] != systems[0]:
                            tentatives[i].insert(0, tentatives[i][-1])
                            tentatives[i].pop(-1)

                if not isLoopFR:
                    for el in tentatives:
                        if (el[-1][0] >= el[0][0]):
                            el.pop(-1)
                        elif (el[-1][0] < el[0][0]):
                            el.pop(0)
                totalDistances = calcFullDistance(tentatives)
                index_min = min(range(len(totalDistances)), key=totalDistances.__getitem__)

                while (tentatives[index_min][0][1] != systems[0]) and (tentatives[index_min][0][2] != systems[0]):
                        tentatives[index_min].insert(0, tentatives[index_min][-1])
                        tentatives[index_min].pop(-1)


                #print(totalDistances)
                isLoop = isLoopFR
                #print(totalDistances)
                #print(systems[index_min])
                printPaths(tentatives[index_min], systems[0])
                print("="*50)
                printConsole(tentatives[index_min])
                '''
                if not (isFirst):
                    lastSystem = tentative[-1][1]
                    tentative2 = greedy(copyDict, lastSystem)
                    tentative2 = printPaths(tentative2)
                    tentatives = [tentative, tentative2]
                    fullDistances = calcFullDistance(tentatives)
                    index_min = min(range(len(fullDistances)), key=fullDistances.__getitem__)
                    if tentatives[index_min][0][1] != systems[0]:
                        if(isLoop):
                            tentatives[index_min].pop(-1)
                        print("\033[1mFound a shorter alternative path !\033[0m")
                        tentatives[index_min].reverse()
                        #for i in range(len(tentatives[index_min])):
                        #    tentatives[index_min][i].insert(1, tentatives[index_min][i][-1])
                        #    tentatives[index_min][i].pop(-1)
                        while tentatives[index_min][0][1] != systems[0]:
                            tentatives[index_min].insert(0, tentatives[index_min][-1])
                            tentatives[index_min].pop(-1)
                printPaths(tentatives[index_min])
                printConsole(tentatives[index_min])
                '''
    except Exception as e:
        if(isDebug):
            print(traceback.format_exc())
        router = ""
        router = "greedy router" if isGreedy else "default router"
        print(f"Unknown error while using {router}: {e}")
        write_mode = "a" if "crash.txt" in os.listdir() else "w"
        with open(os.path.join(fullpath,'persistent','crash.txt'), write_mode) as f:
            f.write(json.dumps({str(datetime.datetime.now()):traceback.format_exc().split("\n")})+"\n")
