import logging

from shaberax.constants import DEBUG, ERROR


def create_stream_logger(name: str, formatter: logging.Formatter) -> logging.Logger:
    """Creates a Logger given a name and a formatter."""
    logger = logging.getLogger(name)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)

    return logger


def general_logger() -> logging.Logger:
    """Creates a Logger instance for General Purpose."""

    class Formatter(logging.Formatter):
        warn_fmt = ERROR + " / %(asctime)s : %(message)s"
        debug_fmt = DEBUG + " / %(pathname)s:%(lineno)d => %(message)s"

        def __init__(self):
            super().__init__(fmt="%(message)s")

        def format(self, record: logging.LogRecord) -> str:
            original_fmt = self._style._fmt

            if record.levelno == logging.WARNING:
                self._style._fmt = Formatter.warn_fmt
            elif record.levelno == logging.DEBUG:
                self._style._fmt = Formatter.debug_fmt

            result = logging.Formatter.format(self, record)
            self._style._fmt = original_fmt

            return result

    return create_stream_logger("GENERAL", Formatter())


# use a metaclass to bypass GeneralLogger in-method call
# this allows to directly obtain the file from which the
# call is done, and enables VSCode redirection
class GeneralLoggerType(type):
    def __getattr__(cls, attr):
        if attr == "debug":
            return cls.logger.debug
        elif attr == "warning":
            return cls.logger.warning

        raise AttributeError(attr)


class GeneralLogger(metaclass=GeneralLoggerType):
    """General Purpose Logger."""

    logger: logging.Logger = general_logger()

    @staticmethod
    def start_debug() -> None:
        GeneralLogger.logger.setLevel(logging.DEBUG)

    @staticmethod
    def stop_debug() -> None:
        GeneralLogger.logger.setLevel(logging.INFO)
