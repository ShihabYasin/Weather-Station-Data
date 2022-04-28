from logging.handlers import TimedRotatingFileHandler
import logging, os

def get_logger(log_file_name, log_level='INFO'):
    log_formatter = logging.Formatter ('%(asctime)s [%(levelname)-5.5s]  %(message)s')
    logger = logging.getLogger (__name__)
    file_handler = logging.FileHandler (log_file_name, mode='a')
    file_handler.setFormatter (log_formatter)
    # rotation_handler = RotatingFileHandler (log_file_name, maxBytes=50 * 1024 * 1024, backupCount=100)
    rotation_handler = TimedRotatingFileHandler (log_file_name, when='midnight', interval=1, backupCount=9999)
    logger.addHandler (file_handler)
    logger.addHandler (rotation_handler)
    if log_level == 'DEBUG':
        logger.setLevel (logging.DEBUG)
    else:
        logger.setLevel (logging.INFO)
    return logger


# All project vars
debug = False
deveopment_port = 8080
production_port = 8080
SECRET_KEY = os.urandom (24)

## Redis config
redis_config = {'CACHE_TYPE': 'RedisCache',
                'CACHE_REDIS_URL': 'redis://redis:6379/0',
                'CACHE_REDIS_HOST': 'redis',
                'CACHE_REDIS_PORT': 6379,
                'CACHE_REDIS_DB': 0,
                'CACHE_DEFAULT_TIMEOUT': 300
                }

## Api detail
NWS_URL = "https://tgftp.nws.noaa.gov/data/observations/metar/stations/"
NWS_RESPONSE_FILE_TYPE = '.TXT'

if not debug:
    logger = get_logger (log_file_name='log_prod_', log_level='INFO')  # choose log_level='INFO' or 'DEBUG'
else:
    logger = get_logger (log_file_name='log_debug_', log_level='DEBUG')

if __name__ == "__main__":
    pass
