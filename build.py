import os
import shutil
import subprocess
from dotenv import load_dotenv



class Builder():

    def __init__(self, debug=False) -> None:
        global isDebug
        self.isDebug = debug
        self.build()

    def build(self):
        version = self.versioning()
        compiled = self.compile_py()
        self.create_directory(version=version)
        self.merge_internal(compiled, version)
        self.create_specific(version)


    def remove_old_builds(self, pyFile:str) -> None:
        if(pyFile.removesuffix('.py') in os.listdir('dist')):
            shutil.rmtree(os.path.join('dist', pyFile.removesuffix('.py')))


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
            self.remove_old_builds(el)
            if(self.isDebug):
                subprocess.run(['pyinstaller', el])
            else:
                subprocess.run(['pyinstaller', '-w', el, '-i', 'edrouter.ico'])
        return toCompile


    def versioning(self):
        vers = input("Version build: ")
        return vers
    
    def create_specific(self, version) -> None:
        working_directory = os.path.join('dist', version)
        with open(os.path.join(working_directory, '.env'), 'w') as f:
            f.write("OUTPUT_PATH=\'%USERPROFILE%\\Downloads\\\'")
            f.close()
        with open(os.path.join(working_directory, 'systems.txt'), 'w') as f:
            f.write('Start system\n')
            f.write('Other system\n')
            f.write('Other system\n')
            f.write('Other system')
            f.close()

if __name__ == '__main__':
    Builder()
