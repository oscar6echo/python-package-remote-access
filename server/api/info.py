
import os
import json

from . import dic_struct


def get():
    """
    Get struct.json data located in same directory

    :return: dict
    """

    return dic_struct, 200
