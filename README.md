https://habr.com/ru/post/689520/

# Агрегатор новостей

### Для работы необходимо:

1. Добавить свои значения переменных в файл `config.py`:

> 1.1 Параметры из [my.telegram.org](https://my.telegram.org)
- `api_id = <Твой api_id int>`
- `api_hash = <Твой api_hash str>`

> 1.2 id канала, куда будут сливаться все новости(нужно создать канал и добавить в него бота из предыдущего пункта как администратора)
- `gazp_chat_id = <Id твоего канала c минусом в начале int>`

2. Добавить свои значения переменных в файл `.env`:

> 2.1 API ключ [platform.openai.com](https://platform.openai.com/settings/organization/billing/overview) (тут нужно зарегистрироваться пополнить баланс, 5$ предварительно должно хватить на месяц)
- `OPENAI_API_KEY=<Твой api_key str>`

> 2.2 Бот из @BotFather
- `BOT_TOKEN= <Токен твоего бота str>`

3. Получить файлы `bot.session` и `gazp.session`:

> 3.1 Запустить `make_session.py`, чтобы пройти аутентификацию в [telethon](https://docs.telethon.dev/en/stable/) и получить свой файл сессии `bot.session`(нужно будет ввести токен бота)

> 3.2 Запустить `make_user_session.py`, чтобы пройти аутентификацию и получить свой файл сессии `gazp.session`(нужно будет ввести свой телефон и пароль от telegram)


### Агрегатор парсит новости из:
> телеграм каналы ([@rbc_news](https://t.me/rbc_news) и т.п.)

> RSS каналы ([www.rbc.ru](https://.rbc.ru))

> новостные сайты ([www.bcs-express.ru](https://bcs-express.ru))

### Настройка и запуск
Фильтр закомментирован (есть пример настройки на газпром, газ и всё с этим связанное).

Добавить/убавить свои каналы или поменять фильтры для новостей можно в файлах `main.py`, `telegram_parser.py`.
На основе ваших предпочтений можете изменить системный промпт в `llm_integration.py`.
Также можете выбрать любую модель gpt и поменять ее в `llm_integration.py` и `docker-compose.yml`.
Каждый парсер написан таким образом, чтобы его можно было запустить отдельно от остальных. 
Это значительно упрощает процесс добавления новых источников, их лучше проверять отдельно, чтобы убедиться в работоспособности. 
Например, feedparser может не прочитать RSS канал и тогда его придется парсить вручную.
- `telegram_parser.py` - парсер телеграм каналов
- `rss_parser.py` - парсер RSS каналов
- `bcs_parser.py` - кастомный парсер сайта [www.bcs-express.ru](https://bcs-express.ru/)
- `main.py` - запускает все парсеры сразу, либо можно запустить в докере через `docker-compose.yml`

Из папки news_aggregator:

Чтобы собрать докер:
```bash
docker compose build --no-cache
```
Чтобы поднять докер:
```bash
docker compose up -d
```
Чтобы посмотреть статус(должен быть Up):
```bash
docker compose ps
```
Чтобы получить логи:
```bash
docker compose logs -f microservice
```
Чтобы завершить сессию:
```bash
docker compose down
```