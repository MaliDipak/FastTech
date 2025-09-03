import logging

from constants import LOG_FILE_PATH


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
                    handlers=[logging.FileHandler(LOG_FILE_PATH)]
                    )


LOGGER = logging.getLogger(name="Tech App")
