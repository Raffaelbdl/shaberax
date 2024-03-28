import logging

from shaberax.constants import ERROR


def create_stream_logger(name: str, formatter: logging.Formatter) -> logging.Logger:
    """Creates a Logger given a name and a formatter."""
    logger = logging.getLogger(name)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger


def warning_logger() -> logging.Logger:
    return create_stream_logger(
        "WARNING", logging.Formatter("%(asctime)s / " + ERROR + " : %(message)s")
    )


class WarningLoggger:
    logger: logging.Logger = warning_logger()

    @staticmethod
    def warn(message: str) -> None:
        WarningLoggger.logger.warn(message)
