import logging


def create_stream_logger(name: str, formatter: logging.Formatter) -> logging.Logger:
    """Creates a Logger given a name and a formatter."""
    logger = logging.getLogger(name)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger
