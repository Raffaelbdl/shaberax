"""Reinforcement Learning Logger."""

import logging

from shaberax.constants import DEBUG
from shaberax.logger import create_stream_logger


def rl_logging() -> logging.Logger:
    """Creates a Logger instance for Reinforcement Learning"""

    class RLFormatter(logging.Formatter):
        debug_fmt = "RL - " + DEBUG + " %(pathname)s:%(lineno)d => %(message)s"
        info_fmt = "RL" + " - %(asctime)s : %(message)s"

        def __init__(self):
            super().__init__(fmt="%(message)s")

        def format(self, record):
            original_fmt = self._style._fmt
            if record.levelno == logging.DEBUG:
                self._style._fmt = RLFormatter.debug_fmt
            elif record.levelno == logging.INFO:
                self._style._fmt = RLFormatter.info_fmt

            result = logging.Formatter.format(self, record)
            self._style._fmt = original_fmt

            return result

    return create_stream_logger("RL", RLFormatter())


class RLLogger:
    """Logging class for Reinforcement Learning.

    For debugging purposes, directly use RLLogger.logger.debug(msg).
    This allows redirection in VSCode console.

    Verbose specifies if information should be displayed:
        - 0: nothing is displayed
        - > 1: episode return is displayed
    """

    verbose: int = 10

    logger: logging.Logger = rl_logging()

    @staticmethod
    def set_verbose(verbose: int) -> None:
        """Sets verbose."""

        RLLogger.verbose = verbose

    @staticmethod
    def log_episode_end(global_step: int, episode_return: float) -> None:
        if RLLogger.verbose < 1:
            return

        RLLogger.logger.info(f"STEP {int(global_step)} : {episode_return:.3f}")
