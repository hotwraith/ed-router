import os
import subprocess
from dotenv import load_dotenv



class Builder():

    def __init__(self) -> None:
        self.build()

    def build(self):
        version = self.versioning()
        toCompile = []
        for el in os.listdir():
            if '.py' in el and 'build' not in el:
                toCompile.append(el)
        for el in toCompile:
            subprocess.run(['pyinstaller', '-w', el])
        



    def versioning(self):
        vers = input("Version build: ")
        return vers
    


if __name__ == '__main__':
    Builder()