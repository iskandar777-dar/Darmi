from Telegram.modules.disable import DisableAbleCommandHandler, DisableAbleMessageHandler
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler
from telegram.ext.filters import BaseFilter
from Telegram import dispatcher as d, log
from typing import Optional, Union, List


class AnieTelegramHandler:
    def __init__(self, d):
        self._dispatcher = d

    def command(
            self, command: str, filters: Optional[BaseFilter] = None, admin_ok: bool = False, pass_args: bool = False,
            pass_chat_data: bool = False, run_async: bool = True, can_disable: bool = True,
            group: Optional[int] = 40
    ):

        def _command(func):
            try:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleCommandHandler(command, func, filters=filters, run_async=run_async,
                                                    pass_args=pass_args, admin_ok=admin_ok), group
                    )
                else:
                    self._dispatcher.add_handler(
                        CommandHandler(command, func, filters=filters, run_async=run_async, pass_args=pass_args), group
                    )
                log.debug(f"[TELEGRAM] Penangan dimuat {command} untuk fungsi {func.__name__} dalam kelompok {group}")
            except TypeError:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleCommandHandler(command, func, filters=filters, run_async=run_async,
                                                pass_args=pass_args, admin_ok=admin_ok, pass_chat_data=pass_chat_data)
                    )
                else:
                    self._dispatcher.add_handler(
                        CommandHandler(command, func, filters=filters, run_async=run_async, pass_args=pass_args,
                                        pass_chat_data=pass_chat_data)
                    )
                log.debug(f"[TELEGRAM] Penangan dimuat {command} untuk fungsi {func.__name__}")

            return func

        return _command

    def message(self, pattern: Optional[BaseFilter] = None, can_disable: bool = True, run_async: bool = True,
                group: Optional[int] = 60, friendly=None):
        def _message(func):
            try:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleMessageHandler(pattern, func, friendly=friendly, run_async=run_async), group
                    )
                else:
                    self._dispatcher.add_handler(
                        MessageHandler(pattern, func, run_async=run_async), group
                    )
                log.debug(f"[TELEGRAM] Pola filter dimuat {pattern} untuk fungsi {func.__name__} dalam kelompok {group}")
            except TypeError:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleMessageHandler(pattern, func, friendly=friendly, run_async=run_async)
                    )
                else:
                    self._dispatcher.add_handler(
                        MessageHandler(pattern, func, run_async=run_async)
                    )
                log.debug(f"[TELEGRAM] Pola filter dimuat {pattern} untuk fungsi {func.__name__}")

            return func

        return _message

    def callbackquery(self, pattern: str = None, run_async: bool = True):
        def _callbackquery(func):
            self._dispatcher.add_handler(CallbackQueryHandler(pattern=pattern, callback=func, run_async=run_async))
            log.debug(f'[TELEGRAM] Penangan callbackquery yang dimuat dengan pola {pattern} untuk fungsi {func.__name__}')
            return func

        return _callbackquery

    def inlinequery(self, pattern: Optional[str] = None, run_async: bool = True, pass_user_data: bool = True,
                    pass_chat_data: bool = True, chat_types: List[str] = None):
        def _inlinequery(func):
            self._dispatcher.add_handler(
                InlineQueryHandler(pattern=pattern, callback=func, run_async=run_async, pass_user_data=pass_user_data,
                                    pass_chat_data=pass_chat_data, chat_types=chat_types))
            log.debug(
                f'[TELEGRAM] Handler inlinequery yang dimuat dengan pola {pattern} untuk fungsi {func.__name__} | LULUS '
                f'USER DATA: {pass_user_data} | MELEWATI DATA CHAT: {pass_chat_data} | JENIS CHAT: {chat_types}')
            return func

        return _inlinequery


zaidid = AnieTelegramHandler(d).command
zaidmsg = AnieTelegramHandler(d).message
zaidcallback = AnieTelegramHandler(d).callbackquery
zaidinline = AnieTelegramHandler(d).inlinequery
