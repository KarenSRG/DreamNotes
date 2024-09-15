import logging
import os
from logging.handlers import TimedRotatingFileHandler

log_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs")
os.makedirs(log_directory, exist_ok=True)

log_file = os.path.join(log_directory, 'app.log')

handler = TimedRotatingFileHandler(
    log_file,
    when='midnight',
    interval=1,
    backupCount=7
)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
