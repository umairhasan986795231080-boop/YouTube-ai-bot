import os
import requests
import edge_tts
import tempfile
import shutil
from telegram import InputFile
import urllib.parse
from io import BytesIO
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
            timeout=120
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




async def scenepack(update, context):
    await generic(update, context, "Create a 20 scene cinematic breakdown for a YouTube video")

async def storyboard(update, context):
    await generic(update, context, "Create a complete storyboard with scene flow visuals and transitions")

async def shotlist(update, context):
    await generic(update, context, "Create a cinematic shot list with camera angles and b-roll")

async def videokit(update, context):
    topic = " ".join(context.args) or "History"
    result = ask_ai(f"""
Create a COMPLETE VIDEO KIT for: {topic}

Include:
1. Viral Title
2. Hook
3. Full Script
4. 20 Scenes
5. 20 Image Prompts
6. Shot List
7. Thumbnail Idea
8. Description
9. SEO Keywords
10. Hashtags
""")
    await send_long_message(update, result)


async def mastervideo(update, context):
    topic = " ".join(context.args) or "History"
    result = ask_ai(f"""
Create a COMPLETE MASTER VIDEO PACKAGE for: {topic}

Include:
1. Viral Title
2. Hook
3. Full Script
4. 20 Scene Breakdown
5. Storyboard
6. Shot List
7. 20 Image Prompts
8. Thumbnail Text
9. Description
10. SEO Keywords
11. Hashtags
12. Upload Strategy
""")
    await send_long_message(update, result)

async def contentcalendar(update, context):
    topic = " ".join(context.args) or "Faceless YouTube Channel"
    await generic(update, context, "Create a complete 30 day content calendar and posting schedule")

async def channelsystem(update, context):
    topic = " ".join(context.args) or "YouTube Channel"
    result = ask_ai(f"""
Create a COMPLETE CHANNEL SYSTEM for: {topic}

Include:
1. Niche Strategy
2. Content Plan
3. Shorts Strategy
4. Longform Strategy
5. SEO System
6. Monetization Plan
7. Growth Plan
8. Upload Workflow
9. Automation Workflow
10. 90 Day Roadmap
""")
    await send_long_message(update, result)


async def imagegen(update, context):
    topic = " ".join(context.args) or "Roman Empire"

    prompt = ask_ai(
        f"Create one detailed cinematic AI image prompt for: {topic}. Return only the prompt."
    )

    image_url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt[:500])

    await update.message.reply_text(
        f"🖼 Image generated for: {topic}\n\n{image_url}"
    )



async def factory(update, context):
    topic = " ".join(context.args) or "History"
    result = ask_ai(f"""
Create a COMPLETE FACTORY PACKAGE for: {topic}

Include:
1. Viral Title
2. Hook
3. Full Script
4. 20 Scene Breakdown
5. Storyboard
6. Shot List
7. 20 Image Prompts
8. Thumbnail Text
9. Description
10. SEO Keywords
11. Hashtags
12. Upload Strategy
13. 30 Day Content Calendar
14. Channel Growth System
""")
    await send_long_message(update, result)


async def imagebatch(update, context):
    topic = " ".join(context.args) or "History"

    await update.message.reply_text("🖼 Generating images...")

    for i in range(1, 6):
        try:
            prompt = ask_ai(
                f"Create cinematic image prompt #{i} for {topic}. Return only the prompt."
            )

            url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt[:300])

            response = requests.get(url, timeout=120)

            if response.status_code == 200:
                await update.message.reply_photo(
                    photo=BytesIO(response.content),
                    caption=f"{topic} - Image {i}"
                )
            else:
                await update.message.reply_text(url)

        except Exception as e:
            await update.message.reply_text(f"Image {i} failed: {e}")


async def uploadready(update, context):
    topic = " ".join(context.args) or "History"
    result = ask_ai(f"""
Create a COMPLETE UPLOAD PACKAGE for: {topic}

Include:
1. Viral Title
2. SEO Description
3. Keywords
4. Hashtags
5. Pinned Comment
6. Community Post
7. Upload Checklist
""")
    await send_long_message(update, result)



async def mediakit(update, context):
    topic = " ".join(context.args) or "History"
    result = ask_ai(f"""
Create a COMPLETE MEDIA KIT for: {topic}

Include:
1. Viral Title
2. Hook
3. Full Script
4. Storyboard
5. Shot List
6. Thumbnail Text
7. SEO Description
8. Keywords
9. Hashtags
10. Upload Package
""")
    await send_long_message(update, result)

async def videobuilder(update, context):
    topic = " ".join(context.args) or "History"
    result = ask_ai(f"""
Create a COMPLETE VIDEO BUILD PLAN for: {topic}

Include:
1. Scene by Scene Timeline
2. Narration for Each Scene
3. Image Placement Guide
4. Transition Suggestions
5. Background Music Style
6. Editing Instructions
7. CapCut Ready Workflow
8. Final Export Checklist
""")
    await send_long_message(update, result)



async def productionpack(update, context):
    topic = " ".join(context.args) or "History"

    result = ask_ai(f"""
Create a COMPLETE PRODUCTION PACK for: {topic}

Include:
1. Viral Title
2. Hook
3. Full Script
4. Scene Breakdown
5. Storyboard
6. Shot List
7. 5 Image Prompts
8. Narration Blocks
9. Video Timeline
10. Editing Instructions
11. Thumbnail Text
12. SEO Description
13. Keywords
14. Hashtags
15. Upload Checklist

Format clearly.
""")

    await send_long_message(update, result)



async def mp4builder(update, context):
    topic = " ".join(context.args) or "History"

    result = ask_ai(f"""
Create a COMPLETE MP4 BUILD PACKAGE for: {topic}

Include:
1. Full Narration
2. Scene Timeline
3. Image Sequence
4. Voice Placement Guide
5. Transition Guide
6. Background Music Style
7. CapCut Workflow
8. Export Settings
9. Final MP4 Checklist

Format clearly.
""")

    await send_long_message(update, result)


async def youtubepackage(update, context):
    topic = " ".join(context.args) or "History"

    result = ask_ai(f"""
Create a COMPLETE YOUTUBE UPLOAD PACKAGE for: {topic}

Include:
1. Viral Title
2. SEO Description
3. Keywords
4. Hashtags
5. Thumbnail Text
6. Pinned Comment
7. Community Post
8. Upload Checklist

Format clearly.
""")

    await send_long_message(update, result)



async def autovideopack(update, context):
    topic = " ".join(context.args) or "History"
    result = ask_ai(f"""
Create a COMPLETE AUTO VIDEO PACK for: {topic}

Include:
1. Viral Title
2. Full Script
3. Narration
4. Scene Timeline
5. Image Prompts
6. MP4 Build Plan
7. Thumbnail Text
8. SEO Description
9. Keywords
10. Hashtags
11. Upload Checklist
""")
    await send_long_message(update, result)


async def automp4(update, context):
    topic = " ".join(context.args) or "History"
    result = ask_ai(f"""
Create an AUTOMATED MP4 PRODUCTION PLAN for: {topic}

Include:
1. Voice Generation Steps
2. Image Generation Steps
3. FFmpeg Workflow
4. Video Assembly Steps
5. Export Settings
6. Final MP4 Checklist
""")
    await send_long_message(update, result)


async def autoupload(update, context):
    topic = " ".join(context.args) or "History"
    result = ask_ai(f"""
Create a COMPLETE YOUTUBE AUTO UPLOAD PACKAGE for: {topic}

Include:
1. Title
2. Description
3. Tags
4. Hashtags
5. Thumbnail Text
6. Pinned Comment
7. Upload Steps
8. Publishing Checklist
""")
    await send_long_message(update, result)



async def fullauto(update, context):
    topic = " ".join(context.args) or "History"

    result = ask_ai(f"""
Create a COMPLETE FULL AUTO VIDEO SYSTEM for: {topic}

Include:

1. Viral Title
2. Full Script
3. Narration Script
4. 10 Scene Timeline
5. 10 Image Prompts
6. Voice Generation Workflow
7. FFmpeg MP4 Workflow
8. Thumbnail Text
9. SEO Description
10. Keywords
11. Hashtags
12. YouTube Upload Steps
13. Publishing Checklist

Format clearly and production-ready.
""")

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

    try:
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

    except Exception as e:
        await update.message.reply_text(
            f"⚠️ Voice generation unavailable on Render right now.\nError: {e}"
        )



async def checkffmpeg(update, context):
    if shutil.which("ffmpeg"):
        await update.message.reply_text("✅ FFmpeg Installed")
    else:
        await update.message.reply_text("❌ FFmpeg Not Found")
        

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
        "generatevoice": generatevoice,
        "scenepack": scenepack,
        "storyboard": storyboard,
        "shotlist": shotlist,
        "videokit": videokit,
        "mastervideo": mastervideo,
        "contentcalendar": contentcalendar,
        "channelsystem": channelsystem,
        "imagegen": imagegen,
        "factory": factory,
        "imagebatch": imagebatch,
        "uploadready": uploadready,
        "mediakit": mediakit,
        "videobuilder": videobuilder,
        "productionpack": productionpack,
        "mp4builder": mp4builder,
        "youtubepackage": youtubepackage,
        "autovideopack": autovideopack,
        "automp4": automp4,
        "autoupload": autoupload,
        "fullauto": fullauto,
        "checkffmpeg": checkffmpeg
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



      
