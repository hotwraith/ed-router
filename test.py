import os
import json
import math
import requests
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
    with open('test.txt', 'w') as f:
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
    z = 0
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
  

def test():
    liste = [(1,2,3), (4,5,6)]
    for i in range(len(liste)):
        liste[i] = list(liste[i])
    print(liste)

if __name__ == '__main__':
    main()