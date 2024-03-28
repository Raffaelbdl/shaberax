"""Telegram Logger.

Before using the Telegram logger, it is necessary to create a bot.
Follow the steps from: https://core.telegram.org/bots/features#botfather to create a bot.

Obtain your chat_id, you can do so by checking the code here:
https://github.com/Raffaelbdl/shaberax/blob/master/resources/get_chat_id.py
"""

import asyncio
import logging
from typing import Any, BinaryIO

try:
    from telegram import Bot
    from telegram.constants import ParseMode
    from telegram.error import TelegramError
except ImportError:
    raise ImportError("Telegram is not installed, run `pip install shaberax[telegram]`")

import yaml

from shaberax.constants import TELEGRAM, ERROR
from shaberax.logger import create_stream_logger, GeneralLogger


def telegram_logging() -> logging.Logger:
    """Creates a Logger instance for Telegram."""

    class TelegramFormatter(logging.Formatter):
        debug_fmt = TELEGRAM + " - %(asctime)s : %(message)s"
        error_fmt = TELEGRAM + " - %(asctime)s / " + ERROR + " : %(message)s"

        def __init__(self):
            super().__init__(fmt="%(message)s")

        def format(self, record) -> str:
            original_fmt = self._style._fmt
            if record.levelno == logging.DEBUG:
                self._style._fmt = TelegramFormatter.debug_fmt
            elif record.levelno == logging.ERROR:
                self._style._fmt = TelegramFormatter.error_fmt

            result = logging.Formatter.format(self, record)
            self._style._fmt = original_fmt

            return result

    return create_stream_logger("TELEGRAM", TelegramFormatter())


class TelegramLogger:
    """Logging class for Telegram."""

    _init: bool = False

    token: str = None
    chat_id: int = None

    logger: logging.Logger = telegram_logging()

    @staticmethod
    def setup(token: str, chat_id: int) -> None:
        """Setups token and chat_id."""

        if token is None or chat_id is None:
            GeneralLogger.warn("token and chat_id must not be None.")
            return

        TelegramLogger._init = True
        TelegramLogger.token = token
        TelegramLogger.chat_id = chat_id

    @staticmethod
    def log_text(text: str, *, parse_mode: ParseMode = ParseMode.MARKDOWN_V2) -> None:
        """Sends text to Telegram.

        Args:
            text: The text to send as a string.
            parse_mode: An optional ParseMode.
        """
        if not TelegramLogger._init:
            GeneralLogger.warn("Telegram Logger not initialized.")
            return

        async def _log():
            bot = Bot(TelegramLogger.token)
            try:
                async with bot:
                    response = await bot.send_message(
                        chat_id=TelegramLogger.chat_id,
                        text=text,
                        parse_mode=parse_mode,
                    )
                    if response and response.message_id:
                        TelegramLogger.logger.debug("Successfully sent log.")
                    else:
                        raise TelegramError
            except TelegramError:
                TelegramLogger.logger.error(
                    "Telegram `log_text` failed. Process will continue."
                )

        asyncio.run(_log())

    @staticmethod
    def log_image(image: str | BinaryIO) -> None:
        """Sends image to Telegram.

        Args:
            image: The path as string or the image as Binary.
        """
        if not TelegramLogger._init:
            GeneralLogger.warn("Telegram Logger not initialized.")
            return

        async def _log():
            bot = Bot(TelegramLogger.token)
            try:
                async with bot:
                    response = await bot.send_photo(
                        chat_id=TelegramLogger.chat_id, photo=image
                    )
                    if response and response.message_id:
                        TelegramLogger.logger.debug("Successfully sent log.")
                    else:
                        raise TelegramError
            except TelegramError:
                TelegramLogger.logger.error(
                    "Telegram `log_image` failed. Process will continue."
                )

        asyncio.run(_log())

    @staticmethod
    def log_dictionary(dictionary: dict[str, Any]) -> None:
        """Sends dictionary to Telegram.

        This methods use yaml to format the dictionary.
        This may result in errors if there are no available yaml handlers.

        Args:
            dictionary: The dictionary to send to Telegram.
        """
        msg = "```yaml\n" + yaml.dump(dictionary) + "\n```"
        return TelegramLogger.log_text(msg, parse_mode=ParseMode.MARKDOWN_V2)
