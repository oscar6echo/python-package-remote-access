
import os
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Build dic_server:')
here = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(here, 'swagger', 'servers.txt')
with open(path, 'r') as f:
    data = f.readlines()
    try:
        data = [[e.strip() for e in s.split(',')] for s in data]
        dic_server = {}
        for d in data:
            dic_server[d[0]] = {'ip': d[1],
                                'port': d[2],
                                'version': d[3],
                                }
        logger.info(dic_server)
    except Exception as e:
        msg = 'invalid servers.txt file'
        raise Exception(msg)
