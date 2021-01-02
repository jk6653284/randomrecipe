# imports
from datetime import datetime
import logging
from rich.logging import RichHandler

# create logger instance
logger = logging.getLogger(__name__)

# create dt for logging
dt = datetime.strftime(datetime.now(),"%Y%m%d-%H-%M-%S")

# handlers
shell_handler = RichHandler()
file_handler = logging.FileHandler(f"logs/{dt}.log")

# formatters
shell_formatter = logging.Formatter('%(message)s')
file_formatter = logging.Formatter('%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s')

# set formatters
shell_handler.setFormatter(shell_formatter)
file_handler.setFormatter(file_formatter)

# set levels
logger.setLevel(logging.DEBUG)
shell_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

# add handlers to logger
logger.addHandler(shell_handler)
logger.addHandler(file_handler)


