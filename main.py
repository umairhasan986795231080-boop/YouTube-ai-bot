import os
import requests

from fastapi import FastAPI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# --------------------
# FastAPI
# --------------------

app = FastAPI()

@app.get("/")
async def home():
    return {"status": "YT Incognite AI Bot Running"}

# --------------------
# ENV
# --------------------

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

telegram_app = None

# --------------------
# OpenRouter Helper
# --------------------

def ask_ai(prompt):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openai/gpt-oss-20b:free",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=60
        )

        data = response.json()

        if "choices" not in data:
            return f"OpenRouter Error:\n{data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {e}"

# --------------------
# Commands
# --------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 YT Incognite AI Bot Active\n\n"
        "Commands:\n"
        "/viral\n"
        "/title topic\n"
        "/hashtags topic\n"
        "/script topic\n"
        "/shorts topic"
    )

async def viral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = ask_ai(
        "Give me 10 viral YouTube video ideas."
    )
    await update.message.reply_text(result[:4000])

async def title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args)

    if not topic:
        await update.message.reply_text(
            "Example:\n/title AI Agents"
        )
        return

    result = ask_ai(
        f"Create 10 viral YouTube titles about: {topic}"
    )

    await update.message.reply_text(result[:4000])

async def hashtags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args)

    if not topic:
        await update.message.reply_text(
            "Example:\n/hashtags AI"
        )
        return

    result = ask_ai(
        f"Generate 30 viral hashtags for: {topic}"
    )

    await update.message.reply_text(result[:4000])

async def script(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args)

    if not topic:
        await update.message.reply_text(
            "Example:\n/script AI Agents"
        )
        return

    result = ask_ai(
        f"Write a YouTube script on: {topic}. Make it engaging and viral."
    )

    await update.message.reply_text(result[:4000])

async def shorts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args)

    if not topic:
        await update.message.reply_text(
            "Example:\n/shorts AI Agents"
        )
        return

    result = ask_ai(
        f"""
Create a viral YouTube Shorts script about: {topic}

Format:
HOOK:
MAIN CONTENT:
CTA:

Keep it under 60 seconds.
"""
    )

    await update.message.reply_text(result[:4000])

# --------------------
# Startup
# --------------------

@app.on_event("startup")
async def startup():

    global telegram_app

    if not BOT_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN missing")
        return

    telegram_app = Application.builder().token(BOT_TOKEN).build()

    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("viral", viral))
    telegram_app.add_handler(CommandHandler("title", title))
    telegram_app.add_handler(CommandHandler("hashtags", hashtags))
    telegram_app.add_handler(CommandHandler("script", script))
    telegram_app.add_handler(CommandHandler("shorts", shorts))

    await telegram_app.initialize()
    await telegram_app.start()

    if telegram_app.updater:
        await telegram_app.updater.start_polling(
            drop_pending_updates=True
        )

    print("✅ Telegram Bot Started")

# --------------------
# Shutdown
# --------------------

@app.on_event("shutdown")
async def shutdown():

    global telegram_app

    if telegram_app:

        if telegram_app.updater:
            await telegram_app.updater.stop()

        await telegram_app.stop()
        await telegram_app.shutdown()
