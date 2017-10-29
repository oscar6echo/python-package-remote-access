

import os
import pickle
import json
import flask

from importlib import import_module

from . import logger, dic_struct


def post(request_data):
    '''
    Execute a local function with args passed through the API.

    3 cases are covered:
        - remote user executes a function
            The result is returned through the API.
        - remote user creates an instance of a class (i.e.
            executes the __init__ method). The instance is
            created locally, and then its __dict__ and its
            methods' signatures are returned through the API.
        - remote user executes a class method.
            An instance of the class is created locally.
            The attributes of this instance are populated
            with the remote instance's __dict__, passed
            through the API. Then the method is executed.
            If it returns any result, it is also returned through
            the API. The method may also modify the instance in-place.
            Then the instance's __dict__ is also returned through
            the API. Thus the API only works if it's able to pickle
            the instance's __dict__.

    :param binary request_data: pickled data sent by remote user
        contains up to module_name, class_name, function_name,
        method_name, li_args, dic_kwargs

    :return: Flask response (pickled data or error message)
    '''

    def xor(a, b):
        """
        logical xor
        """
        return (a and not b) or (not a and b)

    try:
        request_json = pickle.loads(request_data)
    except Exception as e:
        msg = 'invalid payload: error unpickling'
        logger.debug(msg)
        return {'msg': msg, 'error': e.args[0]}, 461

    module_name = request_json.get('module')
    class_name = request_json.get('class', None)
    method_name = request_json.get('method', None)
    function_name = request_json.get('function', None)
    variable_name = request_json.get('variable', None)
    li_args = request_json.get('li_args', [])
    dic_kwargs = request_json.get('dic_kwargs', {})

    logger.info('request_data params')
    logger.info('\tmodule_name=' + module_name)
    logger.info('\tclass_name=' + class_name)
    logger.info('\tmethod_name=' + method_name)
    logger.info('\tfunction_name=' + function_name)
    logger.info('\tvariable_name=' + variable_name)
    logger.info('\tli_args=' + str(li_args))
    logger.info('\tdic_kwargs=' + str(dic_kwargs))

    try:
        assert xor(xor(function_name, class_name and method_name), variable_name)
    except Exception as e:
        msg = 'wrong params: must have function_name xor (class_name and method_name)'
        logger.debug(msg)
        return {'msg': msg, 'error': e.args[0]}, 462

    try:
        module = import_module(module_name)
    except Exception as e:
        msg = 'error importing module {}'
        msg = msg.format(module_name)
        logger.debug(msg)
        return {'msg': msg, 'error': e.args[0]}, 463

    if variable_name:
        logger.debug('get variable')
        try:
            variable = getattr(module, variable_name)
        except Exception as e:
            msg = 'error getting function {}'
            msg = msg.format(function_name)
            logger.debug(msg)
            return {'msg': msg, 'error': e.args[0]}, 464

        # get variable value
        result = variable
        status_code = 200

    elif function_name:
        logger.debug('execute function')
        try:
            function = getattr(module, function_name)
        except Exception as e:
            msg = 'error getting function {}'
            msg = msg.format(function_name)
            logger.debug(msg)
            return {'msg': msg, 'error': e.args[0]}, 464

        # exec function
        result = function(*li_args, **dic_kwargs)
        status_code = 201

    elif class_name:
        try:
            class_obj = getattr(module, class_name)
        except Exception as e:
            msg = 'error getting class {}'
            msg = msg.format(class_name)
            logger.debug(msg)
            return {'msg': msg, 'error': e.args[0]}, 465

        if method_name == '__init__':
            # new instance
            logger.debug('create instance')

            try:
                instance = class_obj(*li_args, **dic_kwargs)
            except Exception as e:
                msg = 'error instantiating class {}'
                msg = msg.format(class_name)
                logger.debug(msg)
                return {'msg': msg, 'error': e.args[0]}, 466

            _dic = instance.__dict__
            # remove any function from _dic
            _dic = {k: v for k, v in _dic.items()
                    if not hasattr(v, '__call__')}

            class_path = module_name.split('.') + [class_name]

            d = dic_struct
            for p in class_path:
                d = d[p]
            methods = d['methods']

            result = {'_dic': _dic,
                      'methods': methods}
            status_code = 202
            logger.info(status_code)
            logger.info(result)

        else:
            # other method on existing object
            logger.debug('execute method on existing instance')

            instance = class_obj.__new__(class_obj)
            instance.__dict__ = dic_kwargs.pop('_dic')

            try:
                method = getattr(instance, method_name)
            except Exception as e:
                msg = 'error getting method {} from class {}'
                msg = msg.format(method_name, class_name)
                logger.debug(msg)
                return {'msg': msg, 'error': e.args[0]}, 467

            try:
                method_result = method(*li_args, **dic_kwargs)
            except Exception as e:
                msg = 'error executing method {} from class {}'
                msg = msg.format(method_name, class_name)
                logger.debug(msg)
                return {'msg': msg, 'error': e.args[0]}, 468

            _dic = instance.__dict__
            # remove any function from _dic
            _dic = {k: v for k, v in _dic.items()
                    if not hasattr(v, '__call__')}

            result = {'_dic': _dic,
                      'method_result': method_result}
            status_code = 203
            logger.debug(status_code)
            logger.debug(result)

    response_data = pickle.dumps(result, pickle.HIGHEST_PROTOCOL)

    # make custom response
    response = flask.make_response(response_data)
    response.headers['content-type'] = 'application/octet-stream'
    response.status_code = status_code

    return response
