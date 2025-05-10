import httpx
import asyncio
import logging
from collections import deque
from telethon import TelegramClient

from telegram_parser import telegram_parser
from rss_parser import rss_parser
# from bcs_parser import bcs_parser
from utils import create_logger, get_history, send_error_message
from config import api_id, api_hash, gazp_chat_id, bot_token


###########################
# Можно добавить телеграм канал, rss ссылку или изменить фильтр новостей

telegram_channels = {
    2608899059: 'https://t.me/quantum_test_channel',
    1099860397: 'https://t.me/rbc_news',
    1428717522: 'https://t.me/gazprom',
    1101170442: 'https://t.me/rian_ru',
    1133408457: 'https://t.me/prime1',
    1149896996: 'https://t.me/interfaxonline',
    # 1001029560: 'https://t.me/bcs_express',
    1203560567: 'https://t.me/markettwits',
    1889761402: 'https://t.me/cryptogoodreads',
    1848837618: 'https://t.me/cryptonarratives1',
    1225126001: 'https://t.me/Paradigm_research',
    1448623236: 'https://t.me/defiprime',
    1876860459: 'https://t.me/defi_eth2',
    1277938806: 'https://t.me/lobsters_daily',
    1974163155: 'https://t.me/dlnewsinfo',
    1249177227: 'https://t.me/crab_notes',
    1598301326: 'https://t.me/mirror_curator_dao',
    1852228340: 'https://t.me/thanefieldresearch',
    1560620044: 'https://t.me/nftTTC',
    1237707529: 'https://t.me/cozytradecrypto',
    1462219382: 'https://t.me/crypto_hd',
    1686223985: 'https://t.me/iliyachain',
    1975585080: 'https://t.me/Vladimir_Tikhonov_Channel',
    1262962760: 'https://t.me/sokolovcrypt',
    1971870226: 'https://t.me/Traidng_Lemon',
    1153542953: 'https://t.me/trade_soul',
    1349257027: 'https://t.me/michaelchobanian',
    1360370332: 'https://t.me/teamtrade618',
    1432348769: 'https://t.me/slezisatoshi',
    1570859949: 'https://t.me/crypto_Iemon',
    1571240278: 'https://t.me/wellfedhamster',
    1287067034: 'https://t.me/gen_m',
    1290061428: 'https://t.me/mr_mozart',
    1773288261: 'https://t.me/CryptoFamilyPublic',
    1623079030: 'https://t.me/SiriusTradingCompany',
    1950002070: 'https://t.me/BITRAF777',

}

rss_channels = {
    # 'www.rbc.ru': 'https://rssexport.rbc.ru/rbcnews/news/20/full.rss',
    # 'www.ria.ru': 'https://ria.ru/export/rss2/archive/index.xml',
    # 'www.1prime.ru': 'https://1prime.ru/export/rss2/index.xml',
    # 'www.interfax.ru': 'https://www.interfax.ru/rss.asp',
}


def check_pattern_func(text):
    '''Вибирай только посты или статьи про газпром или газ'''
    # words = text.lower().split()

    # key_words = [
    #     'газп',     # газпром
    #     'газо',     # газопровод, газофикация...
    #     'поток',    # сервеный поток, северный поток 2, южный поток
    #     'спг',      # спг - сжиженный природный газ
    #     'gazp',
    # ]

    # for word in words:
    #     if 'газ' in word and len(word) < 6:  # газ, газу, газом, газа
    #         return True

    #     for key in key_words:
    #         if key in word:
    #             return True

    return True


###########################
# Если у парсеров много ошибок или появляются повторные новости

# 50 первых символов от поста - это ключ для поиска повторных постов
n_test_chars = 50

# Количество уже опубликованных постов, чтобы их не повторять
amount_messages = 50

# Очередь уже опубликованных постов
posted_q = deque(maxlen=amount_messages)

# +/- интервал между запросами у rss и кастомного парсеров в секундах
timeout = 2

###########################


logger = create_logger('gazp')
logger.info('Start...')

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

tele_logger = create_logger('telethon', level=logging.ERROR)

bot = TelegramClient('bot', api_id, api_hash,
                     base_logger=tele_logger, loop=loop)
bot.start(bot_token=bot_token)


async def send_message_func(text):
    '''Отправляет посты в канал через бот'''
    await bot.send_message(entity=gazp_chat_id,
                           parse_mode='html', link_preview=False, message=text)

    logger.info(text)


# Телеграм парсер
client = telegram_parser('gazp', api_id, api_hash, telegram_channels, posted_q,
                         n_test_chars, check_pattern_func, send_message_func,
                         tele_logger, loop)


# Список из уже опубликованных постов, чтобы их не дублировать
history = loop.run_until_complete(get_history(client, gazp_chat_id,
                                              n_test_chars, amount_messages))

posted_q.extend(history)

httpx_client = httpx.AsyncClient()

# Добавляй в текущий event_loop rss парсеры
for source, rss_link in rss_channels.items():

    # https://docs.python-guide.org/writing/gotchas/#late-binding-closures
    async def wrapper(source, rss_link):
        try:
            await rss_parser(httpx_client, source, rss_link, posted_q,
                             n_test_chars, timeout, check_pattern_func, send_message_func,
                         tele_logger)
        except Exception as e:
            message = f'&#9888; ERROR: {source} parser is down! \n{e}'
            await send_error_message(message, bot_token, gazp_chat_id, logger)

    loop.create_task(wrapper(source, rss_link))


# Добавляй в текущий event_loop кастомный парсер
# async def bcs_wrapper():
#     try:
#         await bcs_parser(httpx_client, posted_q, n_test_chars, timeout,
#                          check_pattern_func, send_message_func,
#                          tele_logger)
#     except Exception as e:
#         message = f'&#9888; ERROR: bcs-express.ru parser is down! \n{e}'
#         await send_error_message(message, bot_token, gazp_chat_id, logger)

# loop.create_task(bcs_wrapper())


try:
    # Запускает все парсеры
    client.run_until_disconnected()

except Exception as e:
    message = f'&#9888; ERROR: telegram parser (all parsers) is down! \n{e}'
    loop.run_until_complete(send_error_message(message, bot_token,
                                               gazp_chat_id, logger))
finally:
    loop.run_until_complete(httpx_client.aclose())
    loop.close()