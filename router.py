import os
import json
import math
import requests
import argparse
from itertools import permutations


def main() -> None:
    if 'temp' not in os.listdir():
        os.mkdir('temp')
    with open('systems.txt', 'r') as f:
        systems = f.readlines()
        f.close()

    sys_dict = {}

    i=0
    for el in systems:
        clear = el.removesuffix('\n')
        sys_dict.update({i:requests.get('https://www.edsm.net/api-v1/system', params={"systemName":clear, "showCoordinates":1}).json()})
        i+=1


    with open('temp/sys_info.json', 'w') as f:
        json.dump(sys_dict, f, indent=4)
        f.close()

    if(isMin):
        otherCalc(systems)

def calc() -> None:
    allPaths = {}
    z = 0
    dict_sys = json.load(open('temp/sys_info.json', 'r'))
    for i in range(len(list(dict_sys.keys()))):
        for j in range(i+1, len(list(dict_sys.keys()))):
            system1 = dict_sys[str(i)]
            system2 = dict_sys[str(j)]
            distance = math.sqrt(math.pow(system1["coords"]["x"]-system2["coords"]["x"],2) + math.pow(system1["coords"]["y"]-system2["coords"]["y"],2) + math.pow(system1["coords"]["z"]-system2["coords"]["z"], 2))
            #print(f"Distance between {system1["name"]} and {system2["name"]}: {round(distance, 2)}lys")
            if(distance > 0):
                allPaths.update({z: {"systems": {0: system1["name"], 1:system2["name"]}, "distance":distance}})
                z += 1

    with open("temp/all_paths.json", 'w') as f:
        json.dump(allPaths, f, indent=4)
        f.close()

def sortPathBySystem() -> None:
    allPaths = json.load(open('temp/all_paths.json', 'r'))
    dict_sys = json.load(open('temp/sys_info.json', 'r'))
    paths_per_system = {}
    for system in list(dict_sys.keys()):
        i=0
        paths_per_system.update({dict_sys[system]["name"]:{}})
        for path in list(allPaths.keys()):
            if((dict_sys[system]["name"] in allPaths[path]["systems"]["0"]) or (dict_sys[system]["name"] in allPaths[path]["systems"]["1"])): 
                paths_per_system[dict_sys[system]["name"]].update({i:allPaths[path]})
                i += 1
    json.dump(paths_per_system, open('temp/min_paths.json', 'w') ,indent=4)
                    
                
def sortPathsByDistance() -> dict:
    systems_path = json.load(open('temp/min_paths.json', 'r'))
    newDict = {}
    for system in list(systems_path.keys()):
        distance = []
        for path in list(systems_path[system].keys()):
            distance.append([systems_path[system][path]["distance"], systems_path[system][path]["systems"]["0"] , systems_path[system][path]["systems"]["1"]])
        distance.sort()
        newDict.update({system:distance})
    return newDict

def greedy(newDict:dict) -> list:
    paths = []
    departure = list(newDict.keys())[0]
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
    all_paths = json.load(open('temp/all_paths.json', 'r'))
    paths = []
    for dist in distances:
        for path in list(all_paths.keys()):
            if(all_paths[path]["distance"] == dist):
                paths.append(all_paths[path])
    return paths

def printPaths(paths:list):
    departure = paths[0][1]
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
    allPaths = searchForAllPaths(departure, systems)
    fullRoutes = {}
    i = 0
    for i in range(len(allPaths)):
        allPaths[i] = list(allPaths[i])
        allPaths[i].append(departure)
        allPaths[i].insert(0, departure)
    
    for route in allPaths:
        for i in range(len(route)-1):
            route[i] = calc_between_sys(route[i], route[i+1])
        route.pop(-1)
    
    totalDistances = calcFullDistance(allPaths)
    index_min = min(range(len(totalDistances)), key=totalDistances.__getitem__)
    print(round(totalDistances[index_min]))
    print(allPaths[index_min])
    with open('minimal_route.txt', 'w') as f:
        for i in range(len(allPaths[index_min])):
            f.write(f'{allPaths[index_min][i][1]}\n')
        f.close()


def calcFullDistance(allPaths):
    totalDistances = []
    for route in allPaths:
        distance = 0
        for leg in route:
            distance += leg[2]
        totalDistances.append(distance)
    return totalDistances


def calc_between_sys(sys1, sys2):
    dict_sys = json.load(open('temp/sys_info.json', 'r'))
    for i in range(len(list(dict_sys.keys()))):
        if(dict_sys[str(i)]["name"] == sys1):
            system1 = dict_sys[str(i)]
        if(dict_sys[str(i)]["name"] == sys2):
            system2 = dict_sys[str(i)]


    distance = math.sqrt(math.pow(system1["coords"]["x"]-system2["coords"]["x"],2) + math.pow(system1["coords"]["y"]-system2["coords"]["y"],2) + math.pow(system1["coords"]["z"]-system2["coords"]["z"], 2))
    #print(f"Distance between {system1["name"]} and {system2["name"]}: {round(distance, 2)}lys")
    if(distance > 0):
        return (sys1, sys2, distance)
    return None


def searchForAllPaths(departure, systems:list) -> list[tuple]:
    systems.remove(departure)
    return list(permutations(systems))


def exportJSON(paths:list) -> bool:
    try:
        with open("route.json", 'w') as f:
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
        with open("spansh_route.txt", 'w') as f:
            for jump in paths:
                f.write(f"{jump[2]}\n")
            f.close()

        return True
    except Exception as e:
        print(e)
        return False

def exportTXT(paths:list) -> bool:
    try:
        with open("route.txt", 'w') as f:
            for jump in paths:
                f.write(f"{jump[1]} -> {jump[2]} ({round(jump[0])} lys)\n")
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
    paths.append([distance, departure["name"], arrival["name"]])
    return paths


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script that adds 3 numbers from CMD"    )
    parser.add_argument("--loop", required=False, default=False,  action='store_true')
    parser.add_argument("--txt", required=False, default=True,  action='store_true')
    parser.add_argument("--json", required=False, default=False,  action='store_true')
    parser.add_argument("--spansh", required=False, default=False,  action='store_true')
    parser.add_argument("--min", required=False, default=False,  action='store_true')
    args = parser.parse_args()
    global isLoop, isTxt, isJson, isSpansh, isMin
    isLoop, isTxt, isJson, isSpansh, isMin = args.loop, args.txt, args.json, args.spansh, args.min
    main()
    if(not isMin):
        calc()
        sortPathBySystem()
        newDict = sortPathsByDistance()
        tentative = greedy(newDict)
        tentative = printPaths(tentative)
        for el in tentative:
            print(f"{el[1]} to {el[2]} ({round(el[0], 1)}lys)")