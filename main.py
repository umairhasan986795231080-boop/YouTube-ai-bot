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
