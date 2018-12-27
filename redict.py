from CGRdb import Molecule, User
from CGRtools.containers import MoleculeContainer
from collections import MutableMapping
from itertools import chain
from pony.orm import db_session



class CGRdbDict(MutableMapping):

    def __init__(self, name='sandbox'):
        self._dict = {}
        self._molecule_dict = {}
        self._name = name

    def __getitem__(self, key):
        if isinstance(key, MoleculeContainer):
            return self._molecule_dict[bytes(key)]
        else:
            return self._dict[key]

    def __setitem__(self, key, value):
        if isinstance(key, MoleculeContainer):
            with db_session:
                if not Molecule[self._name].structure_exists(key):
                    Molecule[self._name](key, User[self._name][1])
            self._molecule_dict[bytes(key)] = value
        else:
            self._dict[key] = value

    def __delitem__(self, key):
        if isinstance(key, MoleculeContainer):
            del self._molecule_dict[bytes(key)]
        else:
            del self._dict[key]

    def __iter__(self):
        return chain(self._dict, (Molecule[self._name].find_structure(x).structure for x in self._molecule_dict))

    def __len__(self):
        return len(self._dict) + len(self._molecule_dict)
