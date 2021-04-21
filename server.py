from telegram.ext import (Updater,
                          Dispatcher,
                          Filters,
                          CommandHandler,
                          CallbackContext,
                          )

from telegram import (Bot,
                      KeyboardButton,
                      Update,
                      )

from config import TOKEN


def start(update: Update, context: CallbackContext):
    update.message.reply_text(f"Привет, {update.effective_user.first_name}!")


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()


if __name__ == '__main__':
    main()

# todo: сделать проверку на права доступа к командам, регистрацию пользоватей
