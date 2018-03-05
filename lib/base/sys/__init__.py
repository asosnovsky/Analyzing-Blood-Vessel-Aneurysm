
# Files
import ntpath
from os import path, makedirs, remove
from shutil import rmtree

def delete_file_if_exists(filename: str):
    try:
        remove(filename)
    except OSError:
        pass

def create_clean_folder(foldername: str, do_not_delete:bool = False):
    if path.exists(foldername):
        if not do_not_delete:
            rmtree(foldername)
            makedirs(foldername)
    else:
        makedirs(foldername)

def path_leaf(path:str) -> str:
    head, tail = ntpath.split(path)
    leaf:str = tail or ntpath.basename(head)
    leaf.replace("\.")

class FileSaver:
    def __init__(self, file_name:str, start_clean:bool = False):
        self.__file_name = file_name
        self.___file = open(file_name, 'a')
        if start_clean:
            delete_file_if_exists(file_name)

    @property
    def _file(self):
        if self.___file.closed:
            self.___file = open(self.__file_name, 'a')
        else:
            self.___file.close()
            self.___file = open(self.__file_name, 'a')
        return self.___file

    @property
    def row_marker(self):
        if not path.isfile(self.__file_name):
            return 0
        f = open(self.__file_name)
        count:int = sum(1 for row in f)
        f.close()
        return count

    def write(self, message:str, ext:str='\n'):
        self._file.writelines(message + ext)

# Processes

from subprocess import Popen , PIPE

def sh(*args, quiet:bool=True):
    popen = Popen(args, stdout=PIPE)
    popen.wait()
    if not quiet:
        print(popen.stdout.read())
    return popen.stdout
