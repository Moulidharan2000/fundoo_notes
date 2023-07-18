import logging

logging.basicConfig(filename="log_file.log", level=logging.ERROR, filemode="a",
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger()

