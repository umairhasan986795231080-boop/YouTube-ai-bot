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
            return f"OpenRouter Error: {data}"
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("YT Incognite AI Bot Active")

async def generic(update, context, prompt_prefix):
    topic = " ".join(context.args)
    if not topic:
        topic = "AI"
    await update.message.reply_text(ask_ai(f"{prompt_prefix}: {topic}")[:4000])

async def viral(update, context): await update.message.reply_text(ask_ai("Give me 10 viral YouTube video ideas.")[:4000])
async def title(update, context): await generic(update, context, "Create 10 viral YouTube titles")
async def hashtags(update, context): await generic(update, context, "Generate 30 viral hashtags")
async def script(update, context): await generic(update, context, "Write a viral YouTube script")
async def shorts(update, context): await generic(update, context, "Create a viral YouTube Shorts script")
async def thumbnail(update, context): await generic(update, context, "Create 5 viral YouTube thumbnail ideas")
async def description(update, context): await generic(update, context, "Write a SEO YouTube description")
async def seo(update, context): await generic(update, context, "Generate complete YouTube SEO package")
async def contentplan(update, context): await generic(update, context, "Create a 30 day content plan")
async def channelidea(update, context): await generic(update, context, "Give 20 faceless channel ideas")
async def hook(update, context): await generic(update, context, "Generate 20 viral hooks")
async def cta(update, context): await generic(update, context, "Generate 20 CTA lines")
async def trend(update, context): await generic(update, context, "Give trending content ideas")
async def series(update, context): await generic(update, context, "Create a 30 episode YouTube series")
async def competitor(update, context): await generic(update, context, "Competitor analysis for niche")
async def uploadpackage(update, context): await generic(update, context, "Create full YouTube upload package")

@app.on_event("startup")
async def startup():
    global telegram_app
    telegram_app = Application.builder().token(BOT_TOKEN).build()
    commands = {
        "start": start, "viral": viral, "title": title, "hashtags": hashtags,
        "script": script, "shorts": shorts, "thumbnail": thumbnail,
        "description": description, "seo": seo, "contentplan": contentplan,
        "channelidea": channelidea, "hook": hook, "cta": cta,
        "trend": trend, "series": series, "competitor": competitor,
        "uploadpackage": uploadpackage
    }
    for name, func in commands.items():
        telegram_app.add_handler(CommandHandler(name, func))
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
        
