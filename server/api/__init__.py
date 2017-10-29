
import os
import logging

from .struct import build_struct, create_struct_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

here = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(here, 'swagger', 'packages.txt')
with open(path, 'r') as f:
    li_package = f.readlines()
    li_package = [e.strip() for e in li_package] 
    logger.info('{}'.format(li_package))


logger.info('Build structure for packages:')
dic_struct = {}
for p in li_package:
    logger.info('\t' + p)
    dic_struct[p] = build_struct(p)

logger.info('Show structure - store in api/struct.json')
logger.info(dic_struct)

create_struct_file(dic_struct)
