
import pickle

import requests as rq
import datetime as dt

from ._obj_from_dict import ObjFromDict
from ._simple import RemoteException, BaseClass
from ._generic_func import generic_func
from . import logger


class Builder:

    def __init__(self,
                 dic_struct,
                 url_exec):
        """
        TBD
        """
        self.dic_struct = dic_struct
        self.url_exec = url_exec
        self.li_module = None

    def build_remote_package(self):
        """
        TBD
        """

        class RemotePackage:
            """
            TBD
            """

            def __init__(self2,
                         dic,
                         path=[]):

                module_name = '.'.join(path)

                for k, v in dic.items():
                    if '_type' in v:
                        if v['_type'] == 'class':
                            class_name = k
                            self2.__dict__[k] = self.build_remote_init(module_name,
                                                                       class_name)
                        elif v['_type'] == 'func':
                            function_name = k
                            self2.__dict__[k] = self.build_remote_function(module_name,
                                                                           function_name)
                        elif v['_type'] == 'var':
                            variable_name = k
                            self2.__dict__[k] = self.build_remote_variable(module_name,
                                                                           variable_name)
                        self.li_module.append((module_name, self2))
                    else:
                        path2 = path[:] + [k]
                        self2.__dict__[k] = RemotePackage(v,
                                                          path=path2)
                        if path:
                            self.li_module.append((module_name, self2))

            def __repr__(self):
                return str(self.__dict__)

        self.li_module = []
        self.remote_package = RemotePackage(self.dic_struct)

    def build_remote_variable(self,
                              module_name,
                              variable_name):
        """
        TBD
        """
        func = self.build_func(module_name=module_name,
                               variable_name=variable_name,
                               )
        return func

    def build_remote_function(self,
                              module_name,
                              function_name):
        """
        TBD
        """
        args, docstring = self.get_function_data(module_name,
                                                 function_name)

        func = self.build_func(module_name=module_name,
                               function_name=function_name,
                               li_args=args,
                               docstring=docstring
                               )
        return func

    def build_remote_init(self,
                          module_name,
                          class_name):
        """
        TBD
        """
        methods, docstring = self.get_class_data(module_name,
                                                 class_name)
        args = methods['__init__']['args']

        func = self.build_func(module_name=module_name,
                               class_name=class_name,
                               method_name='__init__',
                               li_args=args,
                               docstring=docstring
                               )
        return func

    def build_remote_instance(self,
                              module_name,
                              class_name,
                              _dic,
                              tag):
        """
        TBD
        """
        obj = ObjFromDict(_dic)

        methods, docstring = self.get_class_data(module_name,
                                                 class_name)
        dic_method = {'__doc__': 'REMOTE DOCSTRING: ' + docstring}

        for k, v in methods.items():
            method_docstring = v['__doc__']
            args = v['args']

            func = self.build_func(module_name=module_name,
                                   class_name=class_name,
                                   method_name=k,
                                   li_args=args,
                                   docstring=method_docstring,
                                   tag=tag,
                                   )
            if k.startswith('__') and k.endswith('__'):
                dic_method[k] = func
            else:
                setattr(obj, k, func)

        obj.__class__ = type(class_name,
                             (BaseClass,),
                             dic_method)
        return obj

    def get_class_data(self,
                       module_name,
                       class_name):
        """
        TBD
        """
        d = self.dic_struct
        for e in module_name.split('.'):
            d = d[e]
        d = d[class_name]

        methods = d['methods']
        docstring = d['__doc__']

        return methods, docstring

    def get_function_data(self,
                          module_name,
                          function_name):
        """
        TBD
        """
        d = self.dic_struct
        for e in module_name.split('.'):
            d = d[e]
        d = d[function_name]

        args = d['args']
        docstring = d['__doc__']

        return args, docstring

    def build_func(self,
                   module_name='',
                   class_name='',
                   method_name='',
                   function_name='',
                   variable_name='',
                   li_args=[],
                   docstring='',
                   tag=None,
                   ):
        """
        Returns lambda function
        to execute remote function
        or remote class methods
        """

        li_args = [e.strip().replace(' ', '') for e in li_args]

        is_kwargs = False
        if li_args and li_args[-1] == '**kwargs':
            is_kwargs = True
            li_args = li_args[:-1]

        str_args_input = ','.join(li_args)
        if str_args_input == '':
            str_args_input = '_=0'

        if is_kwargs:
            str_args_input += ',**kwargs'

        str_args = ''
        for a in li_args:
            li_part = a.split('=')
            str_args += li_part[0] + ','
        str_args = str_args[:-1]

        if str_args != '':
            str_args = 'li_args=[' + str_args + ']'

        logger.debug('in build func: generic_func params')
        logger.debug(li_args)
        logger.debug(str_args_input)
        logger.debug(str_args)
        logger.debug(is_kwargs)

        s = 'f = lambda {}: generic_func(' + \
            'module_name="{}",' + \
            'class_name="{}",' + \
            'method_name="{}",' + \
            'function_name="{}",' + \
            'variable_name="{}",' + \
            'tag={},' + \
            '{}' + \
            '{})'
        s = s.format(str_args_input,
                     module_name,
                     class_name,
                     method_name,
                     function_name,
                     variable_name,
                     '"{}"'.format(tag) if tag else 'None',
                     str_args,
                     ',**kwargs' if is_kwargs else ''
                     )
        if docstring:
            s += ';f.__doc__="""REMOTE DOCSTRING: {}"""'.format(docstring)

        exec(s)
        return locals()['f']
