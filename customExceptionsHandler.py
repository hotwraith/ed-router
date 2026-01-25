import os
import json
import datetime
import traceback
import customExceptions

class Handler():

    state = {}

    def __init__(self, state:dict) -> None:
        self.state = state

    def handle(self, e) -> None:
        match type(e):
            case customExceptions.MissingSystem:
                self.__missingSys(e)
            case _:
                self.__unkownException(e)

    def __missingSys(self, e:customExceptions.MissingSystem) -> None:
        task = " when trying to fetch systems from EDSM\'s API"
        message = 'Try checking the spelling of your systems, particularly in :'
        for sys in e.systems:
            message += f'\n- {sys}'
        self.__writeToApp(e, task, message)
        
    def __unkownException(self, e:Exception) -> None:
        router = ""
        router = "greedy router" if self.state['isGreedy'] else "default router"
        print(f"Unknown error while using {router}: {type(e)}")
        write_mode = "a" if "crash.txt" in os.listdir() else "w"
        with open(os.path.join(self.state['FULL_PATH'],'persistent','crash.txt'), write_mode) as f:
            f.write(json.dumps({str(datetime.datetime.now()):traceback.format_exc().split("\n")})+"\n")
        message = f'More information can be found at: {os.path.join(self.state['FULL_PATH'], 'persistent', 'crash.txt')}'
        self.__writeToApp(e, customMessage=message)

    def __writeToApp(self, e, task='', customMessage='') -> None:
        OUTPUT_PATH = self.state['OUTPUT_PATH']
        with open(os.path.join(OUTPUT_PATH, "route.txt"), 'w') as f:
            f.write(f'{type(e)} was raised by the router{task}.\n')
            f.write(customMessage)
