"""
LLM wrapper for Brief_News_Bot
• Calls OpenAI ChatCompletion with NO dialog context
• Returns a summary of the news
"""

import os
from functools import lru_cache
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL  = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")

SYSTEM_MSG = (
    "You are Oskar Hartmann.\n"
    "Summarize the following single news paragraph in 1–3 sentences.\n"
    "Focus on key information.\n"
    "No introduction or fluff. Just the concise summary."
)

def _prompt(news: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_MSG},
        {"role": "user",   "content": news.strip()[:512]}
    ]

@lru_cache(maxsize=10_000)
def get_news_summary(news_text: str) -> str:
    """Return summary of the news (cached by news_text)."""
    try:
        rsp = client.chat.completions.create(
            model=MODEL,
            messages=_prompt(news_text),
            temperature=0.6,
            max_tokens=1000     # enough for “0.42”
        )
        summary = rsp.choices[0].message.content.strip()
        print(f"[OpenAI] tokens={rsp.usage.total_tokens}, summary={summary}")
        return summary
    except Exception as e:
        print(f"[OpenAI] fail: {e}")
        return 0.0