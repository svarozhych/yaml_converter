import logging

logging.basicConfig(
      format='%(asctime)-8s %(message)s',
      level=logging.INFO,
      datefmt='%Y-%m-%d %H:%M:%S',
      filename='logging.log', filemode='a'
)

logger = logging.getLogger()
