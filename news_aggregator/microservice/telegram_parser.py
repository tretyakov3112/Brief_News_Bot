from collections import deque
from telethon import TelegramClient, events

from config import api_id, api_hash


def telegram_parser(session, api_id, api_hash, telegram_channels, posted_q,
                    n_test_chars=50, check_pattern_func=None,
                    send_message_func=None, logger=None, loop=None):
    '''Телеграм парсер'''

    # Ссылки на телеграмм каналы
    telegram_channels_links = list(telegram_channels.values())

    client = TelegramClient(session, api_id, api_hash,
                            base_logger=logger, loop=loop, use_ipv6=False)
   
    @client.on(events.NewMessage(chats=telegram_channels_links))
    async def handler(event):
        '''Забирает посты из телеграмм каналов и посылает их в наш канал'''
        if event.raw_text == '':
            return

        # news_text = ' '.join(event.raw_text.split('\n')[:2])
        news_text = event.raw_text
        from llm_integration import handle_news        # local import (avoids cycle)
        impact = handle_news(news_text, event.chat_id)

        if not (check_pattern_func is None):
            if not check_pattern_func(news_text):
                return

        head = news_text[:n_test_chars].strip()

        if head in posted_q:
            return

        source = telegram_channels[event.message.peer_id.channel_id]

        link = f'{source}/{event.message.id}'

        channel = '@' + source.split('/')[-1]

        post = f'<b>{channel}</b>\n{link}\n{news_text}'

        if send_message_func is None:
            print(post, '\n')
        else:
            await send_message_func(post)

        posted_q.appendleft(head)
    client.start() 
    return client
    

if __name__ == "__main__":

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

    # Очередь из уже опубликованных постов, чтобы их не дублировать
    posted_q = deque(maxlen=20)

    client = telegram_parser('gazp', api_id, api_hash, telegram_channels, posted_q)

    client.run_until_disconnected()