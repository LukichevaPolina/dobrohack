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

    update.message.reply_text("Регистрация завершена! Мы будем использовать Ваши имя и фамилию, которые Вы определили "
                              "в профиле Telegram.",
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


def cancel_start(update: Update, _: CallbackContext):
    return ConversationHandler.END


# ======= choose spheres command ==========
CHOOSE_SPHERES_END = 1


def choose_spheres(update: Update, _: CallbackContext):
    """
    выводим список всех сфер, просим выбрать и ввести номера сфер через пробел
    """
    update.message.reply_text(f"Выберите сферы деятельности, в которых вы работаете. Введите номера сфер через пробел.")

    available_spheres(update, _)

    return CHOOSE_SPHERES_END


def choose_spheres_end(update: Update, _: CallbackContext):
    list_id_spheres = list(map(int, update.message.text.split()))

    bot_db.add_spheres2user(update.effective_user.username, list_id_spheres)

    my_spheres(update, _)

    return ConversationHandler.END


def cancel_choose_spheres(update: Update, _: CallbackContext):
    return ConversationHandler.END


# ======= show my spheres command ========
def my_spheres(update: Update, _: CallbackContext):
    spheres = bot_db.get_user_spheres(update.effective_user.username)
    list_spheres = ";\n".join([f"{ind}) {str(sphere)}" for ind, sphere in enumerate(spheres)])

    update.message.reply_text(f"Ваши сферы деятельности:\n"
                              f"{list_spheres}")


# ======= show available spheres command =========
def available_spheres(update: Update, _: CallbackContext):
    spheres = bot_db.get_spheres()
    list_spheres = ";\n".join([f"{ind}) {str(sphere)}" for ind, sphere in enumerate(spheres)])

    update.message.reply_text(f"Существующие сферы деятельности:\n"
                              f"{list_spheres}")


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # start command handler
    start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSE_ROLE: [MessageHandler(Filters.text & ~Filters.command, choose_role)]},

        fallbacks=[CommandHandler("cancel_start", cancel_start)]
    )
    dispatcher.add_handler(start_handler)

    # choose spheres command handler
    choose_spheres_handler = ConversationHandler(
        entry_points=[CommandHandler('choose_spheres', choose_spheres)],

        states={
            CHOOSE_SPHERES_END: [MessageHandler(Filters.text & ~Filters.command, choose_spheres_end)]},

        fallbacks=[CommandHandler("cancel_choose_spheres", cancel_choose_spheres)]
    )
    dispatcher.add_handler(choose_spheres_handler)

    # show available spheres command handler
    available_spheres_handler = CommandHandler('available_spheres', available_spheres)
    dispatcher.add_handler(available_spheres_handler)

    # show my spheres command handler
    my_spheres_handler = CommandHandler('my_spheres', my_spheres)
    dispatcher.add_handler(my_spheres_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()

# todo: делать проверку на право доступа к командам
