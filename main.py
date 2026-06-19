import os
import requests
import edge_tts
import tempfile
from telegram import InputFile
from fastapi import FastAPI
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

app = FastAPI()

@app.get("/")
async def home():
    return {"status": "YT Incognite AI Bot Phase 5 Running"}

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

telegram_app = None

# -------------------------
# OpenRouter
# -------------------------

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

# -------------------------
# Long Message Splitter
# -------------------------

async def send_long_message(update, text):

    if not text:
        return

    for i in range(0, len(text), 4000):
        await update.message.reply_text(text[i:i+4000])

# -------------------------
# Start
# -------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
🚀 YT Incognite AI Bot

CONTENT
/title
/script
/shorts
/series

SEO
/hashtags
/seo
/description
/keyword

RESEARCH
/trend
/competitor
/niche

GROWTH
/hook
/cta
/contentplan
/uploadplan

CHANNEL
/channelidea
/monetize

PACKAGING
/thumbnail
/uploadpackage

AI SYSTEM
/viral
/contentmachine

FACELESS
/faceless
/voiceover
/imageprompt
/videoprompt
"""
    )

# -------------------------
# Generic Handler
# -------------------------

async def generic(update, context, prompt_prefix):

    topic = " ".join(context.args)

    if not topic:
        topic = "AI"

    result = ask_ai(
        f"{prompt_prefix}: {topic}"
    )

    await send_long_message(update, result)

# -------------------------
# Commands
# -------------------------

async def viral(update, context):
    await send_long_message(
        update,
        ask_ai("Give me 20 viral YouTube video ideas.")
    )

async def title(update, context):
    await generic(update, context, "Create 20 viral YouTube titles")

async def hashtags(update, context):
    await generic(update, context, "Generate 50 viral hashtags")

async def script(update, context):
    await generic(update, context, "Write a viral YouTube script")

async def shorts(update, context):
    await generic(update, context, "Create a viral YouTube Shorts script")

async def thumbnail(update, context):
    await generic(update, context, "Create 10 viral thumbnail ideas")

async def description(update, context):
    await generic(update, context, "Write SEO YouTube description")

async def seo(update, context):
    await generic(update, context, "Generate complete YouTube SEO package")

async def contentplan(update, context):
    await generic(update, context, "Create 30 day content plan")

async def channelidea(update, context):
    await generic(update, context, "Generate 20 faceless channel ideas")

async def hook(update, context):
    await generic(update, context, "Generate 20 viral hooks")

async def cta(update, context):
    await generic(update, context, "Generate 20 CTA lines")

async def trend(update, context):
    await generic(update, context, "Find trending content ideas")

async def series(update, context):
    await generic(update, context, "Create a 30 episode YouTube series")

async def competitor(update, context):
    await generic(update, context, "Competitor analysis for niche")

async def uploadpackage(update, context):
    await generic(update, context, "Create complete upload package")

async def keyword(update, context):
    await generic(update, context, "Generate SEO keywords")

async def niche(update, context):
    await generic(update, context, "Find profitable YouTube niches")

async def uploadplan(update, context):
    await generic(update, context, "Create weekly upload plan")

async def monetize(update, context):
    await generic(update, context, "Create monetization strategy")

async def faceless(update, context):
    await generic(update, context, "Create faceless YouTube strategy")

async def voiceover(update, context):
    await generic(update, context, "Create voiceover script")

async def imageprompt(update, context):
    await generic(update, context, "Generate AI image prompts")

async def videoprompt(update, context):
    await generic(update, context, "Generate AI video prompts")

async def contentmachine(update, context):

    niche_name = " ".join(context.args)

    if not niche_name:
        niche_name = "AI"

    result = ask_ai(f"""
Create a COMPLETE YouTube Content Machine for:

{niche_name}

Include:

1. 10 Channel Names
2. Channel Description
3. 30 Video Ideas
4. 20 Shorts Ideas
5. 20 SEO Keywords
6. 30 Hashtags
7. Competitor Strategy
8. Monetization Plan
9. Affiliate Ideas
10. Upload Plan
11. Growth Strategy
12. Thumbnail Strategy

Format clearly.
""")

    await send_long_message(update, result)


# -------------------------
# Automation Pack
# -------------------------

async def autoshorts(update, context):
    topic = " ".join(context.args) or "History Fact"
    result = ask_ai(f"""Create a COMPLETE viral YouTube Shorts package for {topic}.
Include title, hook, 60 sec script, voiceover, 10 image prompts, thumbnail text, description and hashtags.""")
    await send_long_message(update, result)

async def longformmachine(update, context):
    topic = " ".join(context.args) or "History"
    result = ask_ai(f"""Create a COMPLETE 10 minute YouTube package for {topic}.
Include title, chapters, script, narration, b-roll ideas, SEO, description and CTA.""")
    await send_long_message(update, result)

async def imagepack(update, context):
    topic = " ".join(context.args) or "History"
    result = ask_ai(f"Generate 20 cinematic AI image prompts for: {topic}")
    await send_long_message(update, result)

async def voicepack(update, context):
    topic = " ".join(context.args) or "History"
    result = ask_ai(f"Create a professional narration package for: {topic}")
    await send_long_message(update, result)


# -------------------------
# Voice Automation
# -------------------------

async def autoepisode(update, context):
    topic = " ".join(context.args) or "History"

    result = ask_ai(f"""
Create a COMPLETE YouTube episode package for:

{topic}

Include:

1. Viral Title
2. Hook
3. Full Narration Script
4. Thumbnail Text
5. 20 Image Prompts
6. Description
7. SEO Keywords
8. Hashtags

Format clearly.
""")

    await send_long_message(update, result)


async def generatevoice(update, context):
    topic = " ".join(context.args) or "History"

    script = ask_ai(
        f"Write a professional YouTube narration script about: {topic}"
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        mp3_file = tmp.name

    communicate = edge_tts.Communicate(
        script[:4000],
        "en-US-GuyNeural"
    )

    await communicate.save(mp3_file)

    with open(mp3_file, "rb") as audio:
        await update.message.reply_audio(
            audio=audio,
            filename=f"{topic}.mp3"
        )

# -------------------------
# Startup
# -------------------------

@app.on_event("startup")
async def startup():

    global telegram_app

    telegram_app = Application.builder().token(BOT_TOKEN).build()

    commands = {
        "start": start,
        "viral": viral,
        "title": title,
        "hashtags": hashtags,
        "script": script,
        "shorts": shorts,
        "thumbnail": thumbnail,
        "description": description,
        "seo": seo,
        "contentplan": contentplan,
        "channelidea": channelidea,
        "hook": hook,
        "cta": cta,
        "trend": trend,
        "series": series,
        "competitor": competitor,
        "uploadpackage": uploadpackage,
        "keyword": keyword,
        "niche": niche,
        "uploadplan": uploadplan,
        "monetize": monetize,
        "faceless": faceless,
        "voiceover": voiceover,
        "imageprompt": imageprompt,
        "videoprompt": videoprompt,
        "contentmachine": contentmachine,
        "autoshorts": autoshorts,
        "longformmachine": longformmachine,
        "imagepack": imagepack,
        "voicepack": voicepack,
        "autoepisode": autoepisode,
        "generatevoice": generatevoice
    }

    for name, func in commands.items():
        telegram_app.add_handler(
            CommandHandler(name, func)
        )

    await telegram_app.initialize()
    await telegram_app.start()

    if telegram_app.updater:
        await telegram_app.updater.start_polling(
            drop_pending_updates=True
        )

    print("✅ Telegram Bot Started")

# -------------------------
# Shutdown
# -------------------------

@app.on_event("shutdown")
async def shutdown():

    global telegram_app

    if telegram_app:

        if telegram_app.updater:
            await telegram_app.updater.stop()

        await telegram_app.stop()
        await telegram_app.shutdown()

                     
