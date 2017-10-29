
from .subfolder_z.file_z1 import bar

DEFAULT_NAME = 'bernard'

TITI = ['a', 'sample', 'list']
TOTOAB = 'toto'
TATA = 421

EXCLUDED_VARIABLE = ['TOTOAB']


class People:
    """
    docstring for class People
    """

    def __init__(self, name, age=10, **kwargs):
        self.name = name
        self.age = age
        self.count = 0
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_name(self):
        """description get_name"""
        global TATA
        self.count += 1
        TATA += 1
        return self.name

    def __repr__(self):
        return 'This instance contains:\n' + str(self.__dict__)


def foo(x):
    """description function file_a1/foo"""
    return 20 * x


def baz(y, zzz=2):
    """description function file_a1/bar"""
    return 4 * y + zzz
