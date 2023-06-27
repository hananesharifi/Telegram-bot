import logging
from typing import Final

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

BOT_TOKEN: Final = "5849879483:AAGcpeqY9YV7CDrom-QZOURGKjHlzJfS9_o"
BOT_USERNAME: Final = "@RandomUsername1Bot"
DEV_IDS = ["6154789287"]

logging.basicConfig(format='%(levelname)s - (%(asctime)s) - %(message)s - (Line: %(lineno)d) - [%(filename)s]',
                    datefmt='%H:%M:%S',
                    encoding='utf-8',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# /start
# /dice
# /help
# /repeat <text>
# <text>

# Command Handlers
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("user %s started bot.", update.effective_user.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="سلام بر شما",
        reply_to_message_id=update.effective_message.id
    )


async def dice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("user %s wants dice", update.effective_user.id)
    message = await context.bot.send_dice(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.id,
    )
    print(message.dice.value)


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("user %s wants help", update.effective_user.id)
    await context.bot.send_message(
        text="""You can use my bot in following manner:
        /start -> start
        /dice -> bot sends you a dice
        /help -> this message
enjoy""",
        reply_to_message_id=update.effective_message.id,
    )


async def repeat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("user %s wants to say back", update.effective_user.id)
    text = " ".join(context.args)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.effective_message.id
    )


# Message Handlers
def generate_response(text: str) -> str:
    parsed_text = text.lower().strip()
    if "hello" in parsed_text:
        return "Hello to you"
    if "how are you" in parsed_text:
        return "I'm good how about you?"
    if "good" in parsed_text:
        return "Good to hear that"

    return "Sorry, I didn't understand you!"


async def response_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("user %s wants to talk to me", update.effective_user.id)
    chat_type = update.effective_chat.type
    if BOT_USERNAME not in update.effective_message.text and chat_type == "group":
        return
    answer_text = generate_response(update.effective_message.text)
    user_first_name = update.effective_user.first_name
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=answer_text + f"\n{user_first_name}",
        reply_to_message_id=update.effective_message.id
    )


async def echo_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("user %s repeat sticker", update.effective_user.id)
    await context.bot.send_sticker(
        chat_id=update.effective_chat.id,
        sticker=update.effective_message.sticker,
        reply_to_message_id=update.effective_message.id
    )


# Error Handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error("error: %s on update %s", context.error, update)
    for dev_id in DEV_IDS:
        await context.bot.send_message(
            chat_id=dev_id,
            text=f"error: {context.error} on update {update}"
        )


if __name__ == "__main__":
    logger.info("building bot ...")
    bot = ApplicationBuilder().token(BOT_TOKEN).build()

    # adding handlers
    bot.add_handler(CommandHandler("start", start_handler))
    bot.add_handler(CommandHandler("dice", dice_handler))
    bot.add_handler(CommandHandler("help", help_handler))
    bot.add_handler(CommandHandler("repeat", repeat_handler))
    bot.add_handler(MessageHandler(filters.TEXT, response_to_message))
    bot.add_handler(MessageHandler(filters.Sticker.ALL, echo_sticker))
    bot.add_error_handler(error_handler)

    # start bot
    logger.info("start polling ...")
    bot.run_polling()