import requests
from Telegram import CASH_API_KEY
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from Telegram.modules.helper_funcs.decorators import zaid

@zaid(command='cash')
def convert(update: Update, context: CallbackContext):
    args = update.effective_message.text.split(" ")

    if len(args) == 4:
        try:
            orig_cur_amount = float(args[1])

        except ValueError:
            update.effective_message.reply_text("Jumlah Mata Uang Tidak Valid")
            return

        orig_cur = args[2].upper()

        new_cur = args[3].upper()

        request_url = (
            f"https://www.alphavantage.co/query"
            f"?function=CURRENCY_EXCHANGE_RATE"
            f"&from_currency={orig_cur}"
            f"&to_currency={new_cur}"
            f"&apikey={CASH_API_KEY}"
        )
        response = requests.get(request_url).json()
        try:
            current_rate = float(
                response["Nilai Tukar Mata Uang Realtime"]["5. Kurs"]
            )
        except KeyError:
            update.effective_message.reply_text("Mata Uang Tidak Didukung.")
            return
        new_cur_amount = round(orig_cur_amount * current_rate, 5)
        update.effective_message.reply_text(
            f"{orig_cur_amount} {orig_cur} = {new_cur_amount} {new_cur}"
        )

    elif len(args) == 1:
        update.effective_message.reply_text(__help__, parse_mode=ParseMode.MARKDOWN)

    else:
        update.effective_message.reply_text(
            f"*Argumen Tidak Valid!!:* Diperlukan 3 Tapi Lulus {len(args) -1}",
            parse_mode=ParseMode.MARKDOWN,
        )
        
__help__ = """
 - /konversi : pengubah mata uang
 contoh sintaks: /konversi 1 USD INR
"""
