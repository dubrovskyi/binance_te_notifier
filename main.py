import asyncio
import logging
import os
import sys
from time import sleep

from telegram import Bot
import requests

chat_id = os.getenv('CHAT_ID', '')
bot_token = os.getenv('BOT_TOKEN', '')
connection_error_timeout = int(os.getenv('ERROR_TIMEOUT', 600))
bot = Bot(token=bot_token)
logger = logging.getLogger(__name__)


async def send_message(message):
    await bot.send_message(chat_id=chat_id, text=message)


def check_symbol_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    data = requests.get(url)
    data = data.json()
    return float(data['price'])


async def main(pair='HFTUSDT') -> None:
    """
    Binance notifier with symbol pair to Telegram by dist and timeout
    :param pair: str symbol value by which pair need to check on Binance price
    # :param dist: float value when need to notify if previous value changed on
    # :param timeout: how frequently need to ping binance server
    :return: None
    """
    price_for_notification = 0
    while True:
        try:
            value = check_symbol_price(pair)
            if (price_for_notification + 0.01) <= value:
            # if value > 0.9:
                price_for_notification = value
                await send_message(f'{pair} \U0001F4B9 {value}')
            elif (price_for_notification - 0.01) >= value:
            # elif value < 0.7:
                price_for_notification = value
                await send_message(f'{pair} \U0001F53B {value}')
            sleep(60)

        except Exception as e:
            logger.info(f'Exception appeared {e}')
            sleep(connection_error_timeout)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else 'HFTUSDT'))

