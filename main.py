import os
import requests
import asyncio
import threading
import edge_tts

from fastapi import FastAPI
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from moviepy.editor import *

# -------------------------
# FASTAPI
# -------------------------
app = FastAPI()

@app.get("/")
async def home():
    return {"status": "YT Automation Bot Running"}

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

telegram_app = None

# -------------------------
# OPENROUTER AI
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
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=60
        )

        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return str(e)

# -------------------------
# VOICE (TTS)
# -------------------------
async def tts_async(text):
    tts = edge_tts.Communicate(text, "en-US-AriaNeural")
    await tts.save("voice.mp3")

def generate_voice(text):
    asyncio.run(tts_async(text))

# -------------------------
# SCRIPT
# -------------------------
def generate_script(topic):
    return ask_ai(f"""
Write a viral YouTube script on {topic}

Include:
- Hook
- Story
- Emotional engagement
- CTA
""")

# -------------------------
# VIDEO CREATION
# -------------------------
def create_video():
    audio = AudioFileClip("voice.mp3")

    img = ImageClip("image.jpg").set_duration(audio.duration)
    video = img.set_audio(audio)

    video.write_videofile("final.mp4", fps=24)

# -------------------------
# UPLOAD (placeholder)
# -------------------------
def upload_video():
    return "https://youtube.com/watch?v=demo_video"

# -------------------------
# START COMMAND
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🚀 YT Automation Bot Ready

Commands:
/generatevideo <topic>

Example:
/generatevideo history of rome
""")

# -------------------------
# MAIN VIDEO COMMAND
# -------------------------
async def generatevideo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    topic = " ".join(context.args)

    if not topic:
        await update.message.reply_text("❌ Send a topic")
        return

    await update.message.reply_text("🎬 Creating video...")

    # 1. Script
    script = generate_script(topic)

    # 2. Voice
    generate_voice(script)

    # 3. Image (simple safe placeholder)
    img_url = "https://images.pexels.com/photos/414171/pexels-photo-414171.jpeg"
    img_data = requests.get(img_url).content

    with open("image.jpg", "wb") as f:
        f.write(img_data)

    # 4. Video
    create_video()

    # 5. Upload
    link = upload_video()

    await update.message.reply_text(f"✅ Video Ready!\n{link}")

# -------------------------
# TELEGRAM BOT RUNNER (FIXED FOR RENDER)
# -------------------------
def run_bot():
    global telegram_app

    telegram_app = Application.builder().token(BOT_TOKEN).build()

    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("generatevideo", generatevideo))

    telegram_app.run_polling(drop_pending_updates=True)

# -------------------------
# FASTAPI STARTUP
# -------------------------
@app.on_event("startup")
def startup():
    thread = threading.Thread(target=run_bot)
    thread.start()
    print("✅ Telegram Bot Running in Background")

# -------------------------
# OPTIONAL SHUTDOWN
# -------------------------
@app.on_event("shutdown")
def shutdown():
    print("❌ Bot stopping")
