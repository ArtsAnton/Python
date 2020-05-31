import config
import language
import questions
import weather
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler


LANGUAGE_KEY = None
START_STICKER = 'CAACAgIAAxkBAALk117TcXfWHHfBS-Ol0XDI5JvENk91AAJuQAAC6VUFGBIFjkagvbdRGQQ'


def language_keyboard():
    keyboard = [[InlineKeyboardButton(language.Rus, callback_data=language.Rus),
                 InlineKeyboardButton(language.Eng, callback_data=language.Eng)]]
    return InlineKeyboardMarkup(keyboard)


def start(update: Update, context):
    context.bot.send_sticker(
        chat_id=update.effective_message.chat_id,
        sticker=START_STICKER
    )

    context.bot.send_message(
        chat_id=update.effective_message.chat_id,
        text=update.effective_message.text,
        reply_markup=language_keyboard()
    )


def lang(update: Update, context):
    context.bot.send_message(
        chat_id=update.effective_message.chat_id,
        text=update.effective_message.text,
        reply_markup=language_keyboard()
    )


def callback(update: Update, context):
    global LANGUAGE_KEY

    chat_id = update.effective_message.chat_id
    keyboard_answer = update.callback_query.data

    if keyboard_answer == language.Rus:
        LANGUAGE_KEY = language.Rus

        update.callback_query.edit_message_text(
            text=update.effective_message.text
        )

        context.bot.send_message(
            chat_id=chat_id,
            text='Вы выбрали русский язык!\nСменить язык - /language \n{}'.format(questions.WEATHER[LANGUAGE_KEY]),
            reply_markup=weather_keyboard()
        )
    elif keyboard_answer == language.Eng:
        LANGUAGE_KEY = language.Eng

        update.callback_query.edit_message_text(
            text=update.effective_message.text
        )

        context.bot.send_message(
            chat_id=chat_id,
            text='You chose English!\nChange language - /language \n{}'.format(questions.WEATHER[LANGUAGE_KEY]),
            reply_markup=weather_keyboard()
        )
    elif keyboard_answer == 'YES':

        update.callback_query.edit_message_text(
            text=update.effective_message.text
        )

        context.bot.send_message(
            chat_id=chat_id,
            text=questions.DATE[LANGUAGE_KEY],
            reply_markup=date_keyboard()
        )
    elif keyboard_answer == 'NO':

        update.callback_query.edit_message_text(
            text=update.effective_message.text
        )

        context.bot.send_message(
            chat_id=chat_id,
            text=questions.POWER[LANGUAGE_KEY]
        )
    elif keyboard_answer == '0':

        update.callback_query.edit_message_text(
            text=update.effective_message.text
        )

        context.bot.send_message(
            chat_id=chat_id,
            text=weather.obs(language.lang[LANGUAGE_KEY], keyboard_answer, config.OWM_API_KEY),
            reply_markup=date_keyboard()
        )
    elif keyboard_answer == '1':

        update.callback_query.edit_message_text(
            text=update.effective_message.text
        )

        context.bot.send_message(
            chat_id=chat_id,
            text=weather.obs(language.lang[LANGUAGE_KEY], keyboard_answer, config.OWM_API_KEY),
            reply_markup=date_keyboard()
        )
    elif keyboard_answer == '2':

        update.callback_query.edit_message_text(
            text=update.effective_message.text
        )

        context.bot.send_message(
            chat_id=chat_id,
            text=weather.obs(language.lang[LANGUAGE_KEY], keyboard_answer, config.OWM_API_KEY),
            reply_markup=date_keyboard()
        )
    elif keyboard_answer == '3':

        update.callback_query.edit_message_text(
            text=update.effective_message.text
        )

        context.bot.send_message(
            chat_id=chat_id,
            text=weather.obs(language.lang[LANGUAGE_KEY], keyboard_answer, config.OWM_API_KEY),
            reply_markup=date_keyboard()
        )


def weather_keyboard():
    global LANGUAGE_KEY
    if LANGUAGE_KEY == language.Rus:
        keyboard2 = [[InlineKeyboardButton('Да', callback_data='YES'),
                      InlineKeyboardButton('Нет', callback_data='NO')]]
    else:
        keyboard2 = [[InlineKeyboardButton('Yes', callback_data='YES'),
                      InlineKeyboardButton('No', callback_data='NO')]]
    return InlineKeyboardMarkup(keyboard2)


def date_keyboard():
    global LANGUAGE_KEY
    if LANGUAGE_KEY == language.Rus:
        keyboard = [[InlineKeyboardButton(questions.DATE_LIST[LANGUAGE_KEY][0], callback_data=0),
                     InlineKeyboardButton(questions.DATE_LIST[LANGUAGE_KEY][1], callback_data=1)],
                    [InlineKeyboardButton(questions.DATE_LIST[LANGUAGE_KEY][2], callback_data=2),
                    InlineKeyboardButton(questions.DATE_LIST[LANGUAGE_KEY][3], callback_data=3)]]
    else:
        keyboard = [[InlineKeyboardButton(questions.DATE_LIST[LANGUAGE_KEY][0], callback_data=0),
                     InlineKeyboardButton(questions.DATE_LIST[LANGUAGE_KEY][1], callback_data=1)],
                    [InlineKeyboardButton(questions.DATE_LIST[LANGUAGE_KEY][2], callback_data=2),
                    InlineKeyboardButton(questions.DATE_LIST[LANGUAGE_KEY][3], callback_data=3)]]
    return InlineKeyboardMarkup(keyboard)


def main():
    print('Bot is running')

    updater = Updater(
        token=config.TOKEN,
        base_url=config.PROXI,
        use_context=True
    )

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("language", lang))
    dp.add_handler(CallbackQueryHandler(callback=callback, pass_chat_data=True))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
