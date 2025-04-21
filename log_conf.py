import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)-8s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

info_handler = logging.FileHandler('info.log', mode='a')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)

error_handler = logging.FileHandler('error.log', mode='a')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

logger.addHandler(info_handler)
logger.addHandler(error_handler)
