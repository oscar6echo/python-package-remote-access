
import logging
import connexion

# NECESSARY - triggers package structure exploration
import api


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == '__main__':

    app = connexion.FlaskApp(__name__,
                             port=9090,
                             specification_dir='api/swagger/')

    app.add_api('app-api.yaml')

    logger.info('Start App')
    app.run()
