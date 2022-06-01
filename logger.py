import logging
Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="logs.log",
                    filemode="a",
                    format=Log_Format,
                    level=logging.DEBUG)
logger = logging.getLogger()
