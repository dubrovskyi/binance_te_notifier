import logging
import os
import sys
import time
from time import sleep
import asyncio

from telegram import Bot
import requests

chat_id = os.getenv('CHAT_ID', '')
bot_token = os.getenv('BOT_TOKEN', '')
connection_error_timeout = int(os.getenv('ERROR_TIMEOUT', 600))
logger = logging.getLogger(__name__)


async def send_message(message):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)


# defining key/request url
async def main(pair='HFTUSDT', dist=0.1, timeout=10) -> None:
    """
    Binance notifier with symbol pair to Telegram by dist and timeout
    :param pair: str symbol value by which pair need to check on Binance price
    :param dist: float value when need to notify if previous value changed on
    :param timeout: how frequently need to ping binance server
    :return: None
    """
    price_for_notification = 0
    while True:
        key = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"

        # requesting data from url
        data = requests.get(key)
        data = data.json()
        if value := float(data['price']):
            if (price_for_notification + float(dist)) < value:
                price_for_notification = value
                await send_message(f'{pair} \U0001F53B {price_for_notification}')
            elif (price_for_notification - float(dist)) > value:
                price_for_notification = value
                await send_message(f'{pair} \U0001F53B {price_for_notification}')
        sleep(int(timeout))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else 'HFTUSDT'))
    except KeyboardInterrupt:
        pass
    except requests.exceptions.ConnectionError:
        logger.info('ConnectionError appeared')
        time.sleep(connection_error_timeout)
