
import pickle

import datetime as dt
import requests as rq

from ._simple import RemoteException
from . import global_dic_store, logger


def generic_func(module_name=None,
                 class_name=None,
                 method_name=None,
                 function_name=None,
                 variable_name=None,
                 tag=None,
                 li_args=[],
                 **kwargs
                 ):
    """
    Executes remote function over API
    """

    if tag:
        _obj = global_dic_store[tag]
        _dic = {k: v for k, v in _obj.__dict__.items()
                if not hasattr(v, '__call__')}
        kwargs['_dic'] = _dic
        logger.debug('tag ={}'.format(tag))
        logger.debug(_obj.__dict__)

    data = {'module': module_name,
            'class': class_name,
            'method': method_name,
            'function': function_name,
            'variable': variable_name,
            'li_args': li_args,
            'dic_kwargs': kwargs,
            }
    logger.debug('in generic function - print data')
    logger.debug(data)

    req = rq.post(global_dic_store['builder'].url_exec,
                  data=pickle.dumps(data))

    if req.status_code > 460:
        msg = req.json()
        raise RemoteException(msg)

    res = pickle.loads(req.content)

    logger.debug('status code = {}'.format(req.status_code))

    if req.status_code == 200:
        # variable value
        logger.debug('variable value')

        return res

    if req.status_code == 201:
        # function output
        logger.debug('function result')

        return res

    elif req.status_code == 202:
        # create instance of class
        logger.debug('create object')

        _dic = res['_dic']
        tag = str(dt.datetime.now())
        _obj = global_dic_store['builder'].build_remote_instance(module_name,
                                                                 class_name,
                                                                 _dic,
                                                                 tag)
        global_dic_store[tag] = _obj

        return _obj

    elif req.status_code == 203:
        # execute method on existing instance and update it
        logger.debug('method result and update instance')

        _dic = res['_dic']
        method_result = res['method_result']
        _obj.__dict__.update(_dic)

        return method_result
