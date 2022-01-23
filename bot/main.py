import logging
import traceback

from telegram import ForceReply, TelegramError, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Dispatcher,
    Filters,
    MessageHandler,
    Updater,
)

import regru_api
import settings

logger = logging.getLogger()


def error_callback(update, context):
    try:
        raise context.error
    except TelegramError:
        logger.error(traceback.format_exc())
    except Exception:
        logger.error(traceback.format_exc())


def start(update: Update, _: CallbackContext):
    logger.info(f"Start by {update.effective_user.name}")
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr"Приветствую, {user.mention_markdown_v2()}\!",
        reply_markup=ForceReply(selective=True),
    )


def down(update: Update, _: CallbackContext):
    logger.info(f"Stop by {update.effective_user.name}")
    # regru_api.client.actions(regru_api.Action.STOP)
    info = regru_api.RegletInfo(regru_api.client.info())
    update.message.reply_markdown_v2(fr"Тушу сервер {info.ip()}, сэр")


def up(update: Update, _: CallbackContext):
    logger.info(f"Stop by {update.effective_user.name}")
    # regru_api.client.actions(regru_api.Action.START)
    info = regru_api.RegletInfo(regru_api.client.info())
    message = fr"""Сервер {info.ip()} запускается 🕓, сэр\. Проверьте статус через несколько минут"""
    update.message.reply_markdown_v2(message)


def status(update: Update, _: CallbackContext):
    logger.info(f"Status by {update.effective_user.name}")
    result = regru_api.client.info()
    info = regru_api.RegletInfo(result)
    ip = info.ip()
    status = info.status()
    message = fr"""Сервер {ip} {status.desc} {status.emoji}, сэр"""
    update.message.reply_markdown_v2(message, protect_content=True)


def access_denied(update: Update, _: CallbackContext):
    logger.info(
        f"Access denied by {update.effective_user.name} {update.effective_chat.full_name}"
    )
    message = fr"Я с Вами не играю"
    update.message.reply_markdown_v2(message, protect_content=True)


def up_bot() -> Dispatcher:
    if not settings.BOT_TOKEN:
        raise EnvironmentError("Empty bot token")

    base_filter = (
        ~Filters.command
        & Filters.text
        & Filters.chat_type.groups
        & Filters.chat(chat_id=int(settings.MASTER_GROUP_ID))
    )
    updater = Updater(token=settings.BOT_TOKEN, use_context=True)
    dispatcher: Dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(
        MessageHandler(
            base_filter & Filters.regex(r"Бриггс,.*статус.*"),
            status,
        )
    )
    dispatcher.add_handler(
        MessageHandler(base_filter & Filters.regex(r"Бриггс, запускайте сервер"), up)
    )
    dispatcher.add_handler(
        MessageHandler(
            base_filter & Filters.regex(r"Бриггс, тушите сервер"),
            down,
        )
    )
    dispatcher.add_handler(
        MessageHandler(
            ~Filters.command
            & Filters.text
            & Filters.chat_type.groups
            & ~Filters.chat(chat_id=int(settings.MASTER_GROUP_ID)),
            access_denied,
        )
    )
    dispatcher.add_error_handler(error_callback)

    logger.info("START POOLING")
    updater.start_polling(poll_interval=0.2)

    return dispatcher
