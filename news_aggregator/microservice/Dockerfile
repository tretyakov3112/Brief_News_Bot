FROM python:3.10

RUN pip install --no-cache-dir \
        openai==1.78.0 \
        tiktoken==0.7.0 \
        feedparser==6.0.10 \
        Scrapy==2.6.2 \
        telethon>=1.40 \
        telethon-cryptg==0.0.4 \
        httpx==0.23.0

WORKDIR /app

ADD main.py main.py
ADD utils.py utils.py
ADD config.py config.py
ADD user_agents.py user_agents.py
ADD telegram_parser.py telegram_parser.py
ADD llm_integration.py llm_integration.py
ADD rss_parser.py rss_parser.py
# ADD bcs_parser.py bcs_parser.py

ADD bot.session bot.session
ADD gazp.session gazp.session