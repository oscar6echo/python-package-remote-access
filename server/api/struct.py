
import os
import glob
import json
import inspect

from importlib import import_module


def create_struct_file(dic_struct):
    '''
    Creates struct.json on disk next to this file
    Adds build_struct(package_name) to struct.json
    struct.json may contain the dicts of several packages

    :param str package_name: name of the module to describe
    '''

    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, 'struct.json')

    content = json.dumps(dic_struct, indent=2)
    with open(path, 'w') as f:
        f.write(content)


def build_struct(package_name):
    '''
    Builds a dict describing the structure of a package
    The package must be located 2 dir up from this file ie next to folder api

    :param str package_name: name of the package to describe

    :return: dict describing the package package_name
    '''

    # packages must be 2 dir up, in package_remote_access/server
    root = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(root)
    os.chdir(root)

    li_path = []
    for file_name in glob.iglob(package_name + '/**/*.py', recursive=True):
        li_path.append(file_name)

    dic_tree = {}

    for path in li_path:
        dic = dic_tree
        cur_path = []
        split_path = path.split('/')
        for e in split_path[:-1]:
            if e not in dic:
                dic[e] = {}
            cur_path.append(e)
            dic = dic[e]

        last = split_path[-1].split('.py')[0]
        cur_path.append(last)
        file_name = '.'.join(cur_path)
        file = import_module(file_name)
        dic[last] = build_dic_file(file)

    return dic_tree[package_name]


def build_dic_file(file):
    '''
    Builds a dict describing the structure of the file:
        variables, functions and classes

    :param module file: module (result from importlib.import_module)
    :param list EXCLUDED_CLASS: names (str) of classes to ignore
    :param list EXCLUDED_FUNCTION: names (str) of functions to ignore
    :param list EXCLUDED_VARIABLE: names (str) of variables to ignore

    :return: dict describing the module file
    '''

    def is_builtin(name):
        if name.startswith('__') and name.endswith('__'):
            return True
        return False

    def get_args_from_func_sig(sig):
        return str(sig)[1:-1].replace(' ', '').split(',')

    li_class = {}
    li_func = {}
    li_var = {}

    EXCLUDED_CLASS = []
    EXCLUDED_FUNCTION = []
    EXCLUDED_VARIABLE = []

    for (name, member) in inspect.getmembers(file):
        if not is_builtin(name):
            if name == 'EXCLUDED_CLASS':
                EXCLUDED_CLASS = member
            if name == 'EXCLUDED_FUNCTION':
                EXCLUDED_FUNCTION = member
            if name == 'EXCLUDED_VARIABLE':
                EXCLUDED_VARIABLE = member

    for (name, member) in inspect.getmembers(file):
        if not is_builtin(name):
            if inspect.isclass(member):
                if not(name in EXCLUDED_CLASS):
                    li_class[name] = member
            elif inspect.isfunction(member):
                if not(name in EXCLUDED_FUNCTION):
                    li_func[name] = member
            elif not inspect.ismodule(member):
                if not(name in EXCLUDED_VARIABLE):
                    li_var[name] = member

    dic_file = {}

    for class_name, class_obj in li_class.items():
        dic_class = {}
        for name, member in inspect.getmembers(class_obj):
            if inspect.isfunction(member):
                sig = inspect.signature(member)
                args = get_args_from_func_sig(sig)

                if 'self' in args:
                    args.remove('self')

                dic_class[name] = {'_type': 'method',
                                   'args': args,
                                   '__doc__': member.__doc__}
        dic_file[class_name] = {'_type': 'class',
                                'methods': dic_class,
                                '__doc__': class_obj.__doc__}

    for func_name, func in li_func.items():
        sig = inspect.signature(func)
        args = get_args_from_func_sig(sig)
        dic_file[func_name] = {'_type': 'func',
                               'args': args,
                               '__doc__': func.__doc__}

    for name, value in li_var.items():
        dic_file[name] = {'_type': 'var', 'value': value}

    return dic_file
