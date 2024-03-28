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
from shaberax.logger import create_stream_logger


def telegram_logging() -> logging.Logger:
    """Creates a Logger instance for Telegram."""

    class TelegramFormatter(logging.Formatter):
        debug_fmt = TELEGRAM + " - %(asctime)s : %(message)s"
        info_fmt = TELEGRAM + " - %(asctime)s : %(message)s"
        error_fmt = TELEGRAM + " - %(asctime)s / " + ERROR + " : %(message)s"

        def __init__(self):
            super().__init__(fmt="%(message)s")

        def format(self, record) -> str:
            original_fmt = self._style._fmt
            if record.levelno == logging.DEBUG:
                self._style._fmt = TelegramFormatter.debug_fmt
            if record.levelno == logging.INFO:
                self._style._fmt = TelegramFormatter.info_fmt
            elif record.levelno == logging.ERROR:
                self._style._fmt = TelegramFormatter.error_fmt

            result = logging.Formatter.format(self, record)
            self._style._fmt = original_fmt

            return result

    return create_stream_logger("TELEGRAM", TelegramFormatter())


class TelegramLogger:
    """Logging class for Telegram."""

    def __init__(self, token: str, chat_id: int) -> None:
        """Instantiates a Telegram Logger.

        Args:
            token: A token string, obtained when creating a bot with @BotFather.
                See https://core.telegram.org/bots/features#botfather
            chat_id: A private int of the chat between you and your bot.
        """
        self.logging = telegram_logging()

        self.token = token
        self.chat_id = chat_id

    def log_text(
        self, text: str, *, parse_mode: ParseMode = ParseMode.MARKDOWN_V2
    ) -> None:
        """Sends text to Telegram.

        Args:
            text: The text to send as a string.
            parse_mode: An optional ParseMode.
        """

        async def _log():
            bot = Bot(self.token)
            try:
                async with bot:
                    response = await bot.send_message(
                        chat_id=self.chat_id,
                        text=text,
                        parse_mode=parse_mode,
                    )
                    if response and response.message_id:
                        self.logging.debug("Successfully sent log.")
                    else:
                        raise TelegramError
            except TelegramError:
                self.logging.error("Telegram `log_text` failed. Process will continue.")

        asyncio.run(_log())

    def log_image(self, image: str | BinaryIO) -> None:
        """Sends image to Telegram.

        Args:
            image: The path as string or the image as Binary.
        """

        async def _log():
            bot = Bot(self.token)
            try:
                async with bot:
                    response = await bot.send_photo(chat_id=self.chat_id, photo=image)
                    if response and response.message_id:
                        self.logging.debug("Successfully sent log.")
                    else:
                        raise TelegramError
            except TelegramError:
                self.logging.error(
                    "Telegram `log_image` failed. Process will continue."
                )

        asyncio.run(_log())

    def log_dictionary(self, dictionary: dict[str, Any]) -> None:
        """Sends dictionary to Telegram.

        This methods use yaml to format the dictionary.
        This may result in errors if there are no available yaml handlers.

        Args:
            dictionary: The dictionary to send to Telegram.
        """
        msg = "```yaml\n" + yaml.dump(dictionary) + "\n```"
        return self.log_text(msg, parse_mode=ParseMode.MARKDOWN_V2)
