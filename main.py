import os
import asyncio
import threading

from fastapi import FastAPI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

import google.generativeai as genai

# --------------------
# FastAPI
# --------------------

app = FastAPI()

@app.get("/")
def home():
    return {"status": "YT Incognite AI Bot Running"}

# --------------------
# ENV
# --------------------

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# --------------------
# Gemini Helper
# --------------------

def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# --------------------
# Telegram Commands
# --------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 YT Incognite AI Bot Active\n\n"
        "Commands:\n"
        "/viral\n"
        "/title topic\n"
        "/hashtags topic\n"
        "/script topic"
    )

async def viral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = """
    Give me 10 viral YouTube video ideas
    for 2025.
    """

    result = ask_gemini(prompt)
    await update.message.reply_text(result[:4000])

async def title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args)

    if not topic:
        await update.message.reply_text(
            "Example:\n/title AI Agents"
        )
        return

    prompt = f"""
    Create 10 viral YouTube titles about:
    {topic}
    """

    result = ask_gemini(prompt)
    await update.message.reply_text(result[:4000])

async def hashtags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args)

    if not topic:
        await update.message.reply_text(
            "Example:\n/hashtags AI"
        )
        return

    prompt = f"""
    Generate 30 viral hashtags for:
    {topic}
    """

    result = ask_gemini(prompt)
    await update.message.reply_text(result[:4000])

async def script(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args)

    if not topic:
        await update.message.reply_text(
            "Example:\n/script AI Agents"
        )
        return

    prompt = f"""
    Write a YouTube script on:
    {topic}

    Make it engaging and viral.
    """

    result = ask_gemini(prompt)
    await update.message.reply_text(result[:4000])

# --------------------
# Telegram Runner
# --------------------

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if not BOT_TOKEN:
        print("No TELEGRAM_BOT_TOKEN found")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("viral", viral))
    application.add_handler(CommandHandler("title", title))
    application.add_handler(CommandHandler("hashtags", hashtags))
    application.add_handler(CommandHandler("script", script))

    application.run_polling()

# --------------------
# Startup
# --------------------

@app.on_event("startup")
async def startup():
    threading.Thread(
        target=run_bot,
        daemon=True
    ).start()
