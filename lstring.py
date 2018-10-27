from types import TupleType,ListType
from lmodule import *

class LString:
    def __init__(self,modules):
        self._modules = modules

    def __repr__(self):
        return repr(self._modules)
    
    def __getitem__(self,pos):
        return self._modules[pos]

    def __setitem__(self,pos,item):
        self._modules[pos] = item

    def __len__(self):
        return len(self._modules)
    
    def append(self,modules):
        self._modules.append(modules)

    def extend(self,modules):
        self._modules.extend(modules)

    
if __name__ == "__main__":
    pass    
