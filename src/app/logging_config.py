import logging


def configure_logger(logger_name, level=logging.INFO):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] "
                                  "%(name)s "
                                  "%(levelname)s "
                                  "%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
