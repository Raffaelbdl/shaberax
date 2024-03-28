import argparse

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext


def parse_args() -> tuple[str, str]:
    parser = argparse.ArgumentParser()

    parser.add_argument("token", help="The token of your bot.")
    parser.add_argument(
        "--password", help="A `secret` password to make sure no one uses your bot."
    )

    args = parser.parse_args()
    return args.token, args.password


if __name__ == "__main__":
    token, password = parse_args()
    app = ApplicationBuilder().token(token).build()

    async def start(update: Update, context: CallbackContext) -> int:
        if len(context.args) > 0 and context.args[0] == password:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Success! Check the chat_id on the Python console.",
            )
            print(update.effective_chat.id)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Failed! Provide the correct password.",
        )
        print("Failed attempt to connect.")

    app.add_handler(CommandHandler("start", start))
    app.run_polling()
