import os
import sys
import time
from time import sleep
import asyncio

from telegram import Bot
import requests

chat_id = os.getenv('CHAT_ID', '')
bot_token = os.getenv('BOT_TOKEN', '')


async def send_message(message):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)


# defining key/request url
async def main(pair='HFTUSDT', dist=0.1, timeout=10):
    price_for_notification = 0
    while True:
        key = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"

        # requesting data from url
        data = requests.get(key)
        data = data.json()
        if value := float(data['price']):
            if (price_for_notification + float(dist)) < value:
                price_for_notification = value
                await send_message(f'UP {price_for_notification}')
            elif (price_for_notification - float(dist)) > value:
                price_for_notification = value
                await send_message(f'DOWN {price_for_notification}')
        sleep(int(timeout))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else 'HFTUSDT'))
    except KeyboardInterrupt:
        pass
    except requests.exceptions.ConnectionError:
        time.sleep(6000)
