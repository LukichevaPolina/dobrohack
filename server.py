from telegram.ext import (Updater,
                          Dispatcher,
                          Filters,
                          CommandHandler,
                          CallbackContext,
                          ConversationHandler,
                          MessageHandler
                          )

from telegram import (Bot,
                      ReplyKeyboardRemove, ReplyKeyboardMarkup,
                      KeyboardButton,
                      Update,
                      )

from config import TOKEN
from database import bot_db


from messages import (WELCOME_MESSAGE_IT,
                      WELCOME_MESSAGE_NKO,
                      WELCOME_MESSAGE_MODERATOR,
                      )

from constants import (IT,
                       NKO,
                       MODERATOR,
                       )

# ======== start command ========
CHOOSE_ROLE = 1


def start(update: Update, _: CallbackContext):

    keyboard = [[KeyboardButton(text=IT),
                 KeyboardButton(text=NKO)],
                [KeyboardButton(text=MODERATOR)]]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    update.message.reply_text(f"Здраствуйте, {update.effective_user.first_name}! Этот чат-бот создан для соединения "
                              f"НКО и IT-специалистов\n\n"
                              f"Кем вы являетесь?",
                              reply_markup=reply_markup)

    return CHOOSE_ROLE


def choose_role(update: Update, _: CallbackContext):
    text = {IT: WELCOME_MESSAGE_IT,
            NKO: WELCOME_MESSAGE_NKO,
            MODERATOR: WELCOME_MESSAGE_MODERATOR}

    role = update.message.text

    update.message.reply_text("Мы будем использовать Ваши имя и фамилию, которые Вы определили в профиле Telegram.",
                              reply_markup=ReplyKeyboardRemove())

    update.message.reply_text(text[role])

    # todo: добавления в БД, передавать нужные данные
    if role == IT:
        bot_db.create_it_person()

    elif role == NKO:
        bot_db.create_nko_person()

    elif role == MODERATOR:
        bot_db.create_moderator()

    return ConversationHandler.END


def cancel(update: Update, _: CallbackContext):
    pass


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSE_ROLE: [MessageHandler(Filters.text & ~Filters.command, choose_role)]},

        fallbacks=[CommandHandler("cancel", cancel)]
    )
    dispatcher.add_handler(start_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()

# todo: делать проверку на право доступа к командам
