import os
import shutil
import subprocess
from dotenv import load_dotenv



class Builder():

    def __init__(self) -> None:
        self.build()

    def build(self):
        version = self.versioning()
        compiled = self.compile_py()
        self.create_directory(version=version)
        self.merge_internal(compiled, version)
        self.create_specific(version)

    def create_directory(self, version:str) -> None:
        if(version in os.listdir('dist')):
            shutil.rmtree(os.path.join('dist', version))
        os.mkdir(os.path.join('dist', version))
            

    def merge_internal(self, compiled:list[str], version) -> None:
        working_directory = os.path.join('dist', version)
        internals = []
        for file in compiled:
            position = file.removesuffix(".py")
            shutil.copy(os.path.join('dist', position , f"{position}.exe"), working_directory)
            internals.append(os.listdir(os.path.join('dist', position, '_internal')))
        os.mkdir(os.path.join(working_directory, '_internal'))
        i = 0
        for internal in internals:
            for package in internal:
                if(package not in os.listdir(os.path.join(working_directory, '_internal'))):
                    if(os.path.isdir(os.path.join('dist', compiled[i].removesuffix(".py") , "_internal", package))):
                        shutil.copytree(os.path.join('dist', compiled[i].removesuffix(".py") , "_internal", package), os.path.join(working_directory, '_internal', package))
                    else:
                        shutil.copy(os.path.join('dist', compiled[i].removesuffix(".py") , "_internal", package), os.path.join(working_directory, '_internal', package))
            i += 1

        
    def compile_py(self) -> list[str]:
        toCompile = []
        for el in os.listdir():
            if '.py' in el and 'build' not in el:
                toCompile.append(el)
        for el in toCompile:
            subprocess.run(['pyinstaller', '-w', el])
            #subprocess.run(['pyinstaller', el])
        return toCompile


    def versioning(self):
        vers = input("Version build: ")
        return vers
    
    def create_specific(self, version) -> None:
        working_directory = os.path.join('dist', version)
        running = True
        while running:
            newFile = input("File name (with extension): ")
            if(newFile.upper() != 'EXIT'):
                with open(os.path.join(working_directory, newFile), 'w') as f:
                    run2 = True
                    lines = []
                    while run2:
                        line = input("Line content: ")
                        if(line.upper() != 'EXIT'):
                            lines.append(line)
                        else:
                            run2 = False
                    for el in lines:
                        f.write(el+'\n')
                    f.close()
            else:
                running = False

if __name__ == '__main__':
    Builder()
