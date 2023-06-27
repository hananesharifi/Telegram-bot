from telegram import  InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler ,MessageHandler ,filters
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

provinces_info = {
        'آذربایجان شرقی': ['تبریز', 'هتل شمال', 'آفتابی'],
        'آذربایجان غربی': ['ارومیه', 'هتل آذربایجان', 'بارانی'],
        'اردبیل': ['اردبیل', 'هتل سپیده', 'آفتابی'],
        'اصفهان': ['اصفهان', 'هتل عباسی', 'بارانی'],
        'البرز': ['کرج', 'هتل البرز', 'آفتابی'],
        'ایلام': ['ایلام', 'هتل ایلام', 'بارانی'],
        'بوشهر': ['بوشهر', 'هتل بوشهر', 'آفتابی'],
        'تهران': ['تهران', 'هتل تهران', 'بارانی'],
        'چهارمحال و بختیاری': ['شهرکرد', 'هتل چهارمحال', 'آفتابی'],
        'خراسان جنوبی': ['بیرجند', 'هتل خراسان', 'بارانی'],
        'خراسان رضوی': ['مشهد', 'هتل رضوی', 'آفتابی'],
        'خراسان شمالی': ['بجنورد', 'هتل خراسان شمالی', 'بارانی'],
        'خوزستان': ['اهواز', 'هتل خوزستان', 'آفتابی'],
        'زنجان': ['زنجان', 'هتل زنجان', 'بارانی'],
        'سمنان': ['سمنان', 'هتل سمنان', 'آفتابی'],
        'سیستان و بلوچستان': ['زاهدان', 'هتل سیستان', 'بارانی'],
        'فارس': ['شیراز', 'هتل پارسیان', 'آفتابی'],
        'قزوین': ['قزوین', 'هتل قزوین', 'بارانی']
    }


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="سلام من ربات گردشگری هستم")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="من در ارتباط با جاذبه های گردگشگری ایران کمکت میکنم از city/ استفاده کنید")

async def city(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="نام شهر را وارد کنید:")


async def handle_message(update: Update,context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text in provinces_info.keys():
        keyboard = [
            [
                InlineKeyboardButton('مکان های دیدنی', callback_data='1'),
                InlineKeyboardButton('هتل ها', callback_data='2')

            ],
            [
                InlineKeyboardButton('وضیعت آب و هوا', callback_data='3')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text= text, reply_markup=reply_markup)

    else:
        reply_text = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text= 'ما همچین شهری نداریم در ایران دوباره تلاش کنین', reply_markup=reply_markup)


async def button(update: Update ,context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    element_key = query.data

    if element_key in provinces_info.keys():
        element_value = provinces_info[element_key]
        reply_text = '\n'.join(element_value)
        await query.answer()
        await query.edit_message_text(text=reply_text)
    else:
        await query.answer()
        await query.edit_message_text(text='not found')
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error("error %s happened to update %s", context.error, update)


if __name__ == '__main__':
    application = ApplicationBuilder().token('token').build()
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help' , help)
    city_handler = CommandHandler('city' ,city)
    message_handler = MessageHandler(filters.TEXT, handle_message)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(city_handler)
    application.add_handler(message_handler)
    application.add_handler(CallbackQueryHandler(button))
    application.add_error_handler(error_handler)
    application.run_polling()