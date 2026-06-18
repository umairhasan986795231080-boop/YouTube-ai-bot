import os
import requests

from fastapi import FastAPI
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

app = FastAPI()

@app.get("/")
async def home():
    return {"status": "YT Incognite AI Bot Running"}

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

telegram_app = None

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
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=60
        )

        data = response.json()

        if "choices" not in data:
            return f"OpenRouter Error:\\n{data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 YT Incognite AI Bot Active\\n\\n"
        "Commands:\\n"
        "/viral\\n/title topic\\n/hashtags topic\\n/script topic\\n"
        "/shorts topic\\n/thumbnail topic\\n/description topic\\n"
        "/seo topic\\n/contentplan niche\\n/channelidea niche"
    )

async def viral(update, context):
    await update.message.reply_text(
        ask_ai("Give me 10 viral YouTube video ideas.")[:4000]
    )

async def title(update, context):
    topic = " ".join(context.args)
    if not topic:
        return await update.message.reply_text("Example:\\n/title AI Agents")
    await update.message.reply_text(
        ask_ai(f"Create 10 viral YouTube titles about: {topic}")[:4000]
    )

async def hashtags(update, context):
    topic = " ".join(context.args)
    if not topic:
        return await update.message.reply_text("Example:\\n/hashtags AI")
    await update.message.reply_text(
        ask_ai(f"Generate 30 viral hashtags for: {topic}")[:4000]
    )

async def script(update, context):
    topic = " ".join(context.args)
    if not topic:
        return await update.message.reply_text("Example:\\n/script AI Agents")
    await update.message.reply_text(
        ask_ai(f"Write a highly engaging viral YouTube video script about: {topic}")[:4000]
    )

async def shorts(update, context):
    topic = " ".join(context.args)
    if not topic:
        return await update.message.reply_text("Example:\\n/shorts AI Agents")
    await update.message.reply_text(
        ask_ai(f"Create a viral YouTube Shorts script about {topic} with HOOK, MAIN CONTENT and CTA under 60 seconds.")[:4000]
    )

async def thumbnail(update, context):
    topic = " ".join(context.args)
    if not topic:
        return await update.message.reply_text("Example:\\n/thumbnail AI Agents")
    await update.message.reply_text(
        ask_ai(f"Create 5 viral YouTube thumbnail ideas for {topic}. Include text, visual concept, emotion, colors and CTR tip.")[:4000]
    )

async def description(update, context):
    topic = " ".join(context.args)
    if not topic:
        return await update.message.reply_text("Example:\\n/description AI Agents")
    await update.message.reply_text(
        ask_ai(f"Write a SEO optimized YouTube description for: {topic}")[:4000]
    )

async def seo(update, context):
    topic = " ".join(context.args)
    if not topic:
        return await update.message.reply_text("Example:\\n/seo AI Agents")
    await update.message.reply_text(
        ask_ai(f"Generate complete YouTube SEO package for {topic}: keywords, tags, hashtags and ranking tips.")[:4000]
    )

async def contentplan(update, context):
    topic = " ".join(context.args)
    if not topic:
        return await update.message.reply_text("Example:\\n/contentplan AI")
    await update.message.reply_text(
        ask_ai(f"Create a 30 day YouTube content plan for niche: {topic}")[:4000]
    )

async def channelidea(update, context):
    topic = " ".join(context.args)
    if not topic:
        return await update.message.reply_text("Example:\\n/channelidea AI")
    await update.message.reply_text(
        ask_ai(f"Give 20 faceless YouTube channel ideas for niche: {topic}")[:4000]
    )

@app.on_event("startup")
async def startup():
    global telegram_app

    telegram_app = Application.builder().token(BOT_TOKEN).build()

    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("viral", viral))
    telegram_app.add_handler(CommandHandler("title", title))
    telegram_app.add_handler(CommandHandler("hashtags", hashtags))
    telegram_app.add_handler(CommandHandler("script", script))
    telegram_app.add_handler(CommandHandler("shorts", shorts))
    telegram_app.add_handler(CommandHandler("thumbnail", thumbnail))
    telegram_app.add_handler(CommandHandler("description", description))
    telegram_app.add_handler(CommandHandler("seo", seo))
    telegram_app.add_handler(CommandHandler("contentplan", contentplan))
    telegram_app.add_handler(CommandHandler("channelidea", channelidea))

    await telegram_app.initialize()
    await telegram_app.start()

    if telegram_app.updater:
        await telegram_app.updater.start_polling(drop_pending_updates=True)

@app.on_event("shutdown")
async def shutdown():
    global telegram_app

    if telegram_app:
        if telegram_app.updater:
            await telegram_app.updater.stop()

        await telegram_app.stop()
        await telegram_app.shutdown()
    
