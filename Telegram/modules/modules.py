import importlib

from Telegram import dispatcher
from Telegram.__main__ import (
    CHAT_SETTINGS,
    DATA_EXPORT,
    DATA_IMPORT,
    HELPABLE,
    IMPORTED,
    MIGRATEABLE,
    STATS,
    USER_INFO,
    USER_SETTINGS,
)
from Telegram.modules.helper_funcs.chat_status import dev_plus, sudo_plus
from telegram import ParseMode, Update
from telegram.ext import CallbackContext
from Telegram.modules.helper_funcs.decorators import zaid


@zaid(command='load')
@dev_plus
def load(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text.split(" ", 1)[1]
    load_messasge = message.reply_text(
        f"Mencoba memuat modul : <b>{text}</b>", parse_mode=ParseMode.HTML
    )

    try:
        imported_module = importlib.import_module("Telegram.modules." + text)
    except:
        load_messasge.edit_text("Apakah modul itu ada?")
        return

    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        load_messasge.edit_text("Modul sudah dimuat.")
        return
    if "__handlers__" in dir(imported_module):
        handlers = imported_module.__handlers__
        for handler in handlers:
            if type(handler) != tuple:
                dispatcher.add_handler(handler)
            else:
                handler_name, priority = handler
                dispatcher.add_handler(handler_name, priority)
    else:
        IMPORTED.pop(imported_module.__mod_name__.lower())
        load_messasge.edit_text("Modul tidak dapat dimuat.")
        return

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    load_messasge.edit_text(
        "Successfully loaded module : <b>{}</b>".format(text), parse_mode=ParseMode.HTML
    )

@zaid(command='unload')
@dev_plus
def unload(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text.split(" ", 1)[1]
    unload_messasge = message.reply_text(
        f"Mencoba membongkar modul : <b>{text}</b>", parse_mode=ParseMode.HTML
    )

    try:
        imported_module = importlib.import_module("Telegram.modules." + text)
    except:
        unload_messasge.edit_text("Apakah modul itu ada?")
        return

    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__
    if imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED.pop(imported_module.__mod_name__.lower())
    else:
        unload_messasge.edit_text("Tidak dapat membongkar sesuatu yang tidak dimuat.")
        return
    if "__handlers__" in dir(imported_module):
        handlers = imported_module.__handlers__
        for handler in handlers:
            if type(handler) == bool:
                unload_messasge.edit_text("This module can't be unloaded!")
                return
            elif type(handler) != tuple:
                dispatcher.remove_handler(handler)
            else:
                handler_name, priority = handler
                dispatcher.remove_handler(handler_name, priority)
    else:
        unload_messasge.edit_text("Modul tidak dapat dibongkar.")
        return

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE.pop(imported_module.__mod_name__.lower())

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.remove(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.remove(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.remove(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.remove(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.remove(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS.pop(imported_module.__mod_name__.lower())

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS.pop(imported_module.__mod_name__.lower())

    unload_messasge.edit_text(
        f"Berhasil membongkar modul : <b>{text}</b>", parse_mode=ParseMode.HTML
    )


@zaid(command='listmodules')
@sudo_plus
def listmodules(update: Update, context: CallbackContext):
    message = update.effective_message
    module_list = []

    for helpable_module in HELPABLE:
        helpable_module_info = IMPORTED[helpable_module]
        file_info = IMPORTED[helpable_module_info.__mod_name__.lower()]
        file_name = file_info.__name__.rsplit("Telegram.modules.", 1)[1]
        mod_name = file_info.__mod_name__
        module_list.append(f"- <code>{mod_name} ({file_name})</code>\n")
    module_list = "Modul berikut dimuat : \n\n" + "".join(module_list)
    message.reply_text(module_list, parse_mode=ParseMode.HTML)


__mod_name__ = "Modules"
