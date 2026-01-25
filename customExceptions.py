class MissingSystem(Exception):
    '''
    Raised when a system inputed through 'systems.txt' isn't found in EDSM's database.
    '''
    systems = []
    path = ""
    description = "Raised when a system inputed through 'systems.txt' isn't found in EDSM's database."
    message = ""
    def __init__(self, systems:list[str], OUTPUT_PATH:str,*args: object) -> None:
        super().__init__(*args)
        self.systems = systems
        self.path = OUTPUT_PATH
