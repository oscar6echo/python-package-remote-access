
import sys
import requests as rq

from ._builder import Builder

from . import global_dic_store
from . import logger


class Connect:

    def __init__(self,
                 url_server=None,
                 url_nameserver=None,
                 server_name=None):
        """
        TBD
        """
        if url_nameserver and server_name:
            self.url_nameserver = url_nameserver
            self.server_name = server_name
            self.url_server = self.get_url_server()
            if self.url_server:
                self.connect()
                return
            else:
                logger.error(
                    'server {} unknown to nameserver'.format(server_name))
                return
        if url_server:
            self.url_server = url_server
            self.connect()
            return

        logger.error('missing connection info')
        logger.error(
            'Must have url_server or (url_nameserver and server_name)')

    def connect(self):
        """
        TBD
        """
        self.url_info = self.url_server + '/info'
        self.url_exec = self.url_server + '/exec'

        r = rq.get(self.url_info)
        self.struct = r.json()

        print('struct received from server')

    def get_url_server(self):
        """
        TBD
        """
        url_nameserver_info = self.url_nameserver + '/info'

        r = rq.get(url_nameserver_info)
        dic_server = r.json()
        logger.debug(dic_server)

        d = dic_server.get(self.server_name, None)
        if d:
            url_server = 'http://{}:{}/{}'.format(
                d['ip'], d['port'], d['version'])
            return url_server

    def build_remote_package(self,
                             update_sys_modules=False,
                             verbose=False):
        """
        TBD
        """
        if not self.struct:
            logger.error('missing struct')
            return

        b = Builder(self.struct,
                    self.url_exec)
        global_dic_store['builder'] = b

        b.build_remote_package()
        
        if update_sys_modules:
        
            for name, obj in b.li_module:
                sys.modules[name] = obj
        
            if verbose:
                print('The remote modules were added to sys.modules')
                for name, obj in b.li_module:
                    print('\t{}'.format(name))
                print('You can import them as if they were local modules')

        return b.remote_package
