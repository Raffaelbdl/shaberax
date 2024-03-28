"""Reinforcement Learning Logger."""

import logging

from shaberax.constants import DEBUG
from shaberax.logger import create_stream_logger


def rl_logging() -> logging.Logger:
    """Creates a Logger instance for Reinforcement Learning."""
    return create_stream_logger(
        "RL", logging.Formatter("RL" + " - %(asctime)s : %(message)s")
    )


class RLLogger:
    """Logging class for Reinforcement Learning.


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
