"""
Telegram Calendar Bot with AI Assistant
Main application file - FIXED VERSION
"""
import logging
import sys
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

import config
from bot.handlers import (
    BotHandlers,
    WAITING_EVENT_TITLE,
    WAITING_EVENT_DATE,
    WAITING_EVENT_TIME,
    WAITING_EVENT_DURATION,
    WAITING_EVENT_LOCATION,
    WAITING_DELETE_SELECTION
)
from bot.keyboards import get_main_menu, get_quick_reply_keyboard

# Configure logging
logging.basicConfig(
    format=config.LOG_FORMAT,
    level=config.LOG_LEVEL
)
logger = logging.getLogger(__name__)

# Initialize handlers
bot_handlers = BotHandlers()

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks - SIMPLIFIED VERSION"""
    query = update.callback_query
    await query.answer()
    
    # Since inline buttons don't work well with conversation handlers,
    # we'll just send instructions to use commands
    
    if query.data == 'add_event':
        await query.message.reply_text(
            "📅 Untuk menambah jadwal, gunakan:\n"
            "• Ketik: /add_event\n"
            "• Atau klik tombol '📅 Tambah Jadwal' di keyboard\n"
            "• Atau langsung chat dengan format:\n"
            "  _'Meeting besok jam 2 siang di kantor'_",
            parse_mode='Markdown'
        )
    
    elif query.data == 'list_events':
        await query.message.reply_text(
            "📋 Untuk melihat jadwal hari ini:\n"
            "• Ketik: /list_events\n"
            "• Atau klik tombol '📋 Lihat Hari Ini' di keyboard"
        )
    
    elif query.data == 'list_week':
        await query.message.reply_text(
            "🗓️ Untuk melihat jadwal minggu ini:\n"
            "• Ketik: /list_week\n"
            "• Atau klik tombol '🗓️ Lihat Minggu' di keyboard"
        )
    
    elif query.data == 'delete_event':
        await query.message.reply_text(
            "🗑️ Untuk menghapus jadwal:\n"
            "• Ketik: /delete_event"
        )
    
    elif query.data == 'ai_chat':
        await query.message.reply_text(
            "🤖 *AI Assistant Mode*\n\n"
            "Cara menggunakan AI:\n"
            "• Langsung chat untuk buat jadwal otomatis\n"
            "• Atau ketik: /ai [pesan Anda]\n\n"
            "Contoh:\n"
            "_Meeting dengan client besok jam 3 sore_\n"
            "_/ai analisis jadwal saya_",
            parse_mode='Markdown'
        )
    
    elif query.data == 'help':
        # Call the help handler directly
        await bot_handlers.help(query, context)
    
    elif query.data == 'settings':
        from bot.keyboards import get_settings_keyboard
        await query.edit_message_text(
            "⚙️ *Settings*\n\nPilih pengaturan:",
            parse_mode='Markdown',
            reply_markup=get_settings_keyboard()
        )
    
    elif query.data == 'settings_reconnect':
        await query.message.reply_text("/connect_calendar untuk reconnect")
    
    elif query.data == 'settings_clear_ai':
        user_id = str(query.from_user.id)
        bot_handlers.ai_service.clear_chat_history(user_id)
        await query.message.reply_text("✅ AI chat history cleared!")
    
    elif query.data == 'main_menu':
        await query.edit_message_text(
            "📱 Menu Utama",
            reply_markup=get_main_menu()
        )

async def quick_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quick reply keyboard buttons"""
    text = update.message.text
    
    if text == "📅 Tambah Jadwal":
        return await bot_handlers.add_event_start(update, context)
    elif text == "📋 Lihat Hari Ini":
        await bot_handlers.list_events(update, context)
    elif text == "🗓️ Lihat Minggu":
        await bot_handlers.list_week_events(update, context)
    elif text == "🗑️ Hapus Jadwal":  # TAMBAHKAN INI
        return await bot_handlers.delete_event_start(update, context)
    elif text == "🤖 Chat AI":
        await update.message.reply_text(
            "🤖 *AI Assistant Mode*\n\n"
            "Silakan ketik pesan Anda.\n"
            "Contoh: Meeting besok jam 2 siang",
            parse_mode='Markdown'
        )
    elif text == "📚 Bantuan":
        await bot_handlers.help(update, context)
    else:
        # Treat as AI chat for schedule detection
        await bot_handlers.handle_message(update, context)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ Terjadi kesalahan. Silakan coba lagi atau gunakan /help"
            )
    except:
        pass

async def post_init(application: Application) -> None:
    """Post initialization"""
    bot_info = await application.bot.get_me()
    logger.info(f"Bot started: @{bot_info.username}")
    
    print("\n" + "="*50)
    print("🤖 TELEGRAM CALENDAR BOT WITH AI")
    print("="*50)
    print(f"✅ Bot: @{bot_info.username}")
    print(f"📍 Timezone: {config.TIMEZONE_STR}")
    print("="*50)
    print("Bot is running! Press Ctrl+C to stop.\n")

def main():
    """Start the bot"""
    if not config.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        sys.exit(1)
    
    if not config.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set")
    
    # Create application
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    # Conversation handlers
    add_event_conv = ConversationHandler(
        entry_points=[
            CommandHandler('add_event', bot_handlers.add_event_start),
            MessageHandler(filters.Regex('^📅 Tambah Jadwal$'), bot_handlers.add_event_start)
        ],
        states={
            WAITING_EVENT_TITLE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.receive_event_title)
            ],
            WAITING_EVENT_DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.receive_event_date)
            ],
            WAITING_EVENT_TIME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.receive_event_time)
            ],
            WAITING_EVENT_DURATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.receive_event_duration)
            ],
            WAITING_EVENT_LOCATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.receive_event_location)
            ],
        },
        fallbacks=[CommandHandler('cancel', bot_handlers.cancel)],
        per_message=False
    )
    
    delete_event_conv = ConversationHandler(
    entry_points=[
        CommandHandler('delete_event', bot_handlers.delete_event_start),
        MessageHandler(filters.Regex('^🗑️ Hapus Jadwal$'), bot_handlers.delete_event_start)  # TAMBAHKAN INI
    ],
    states={
        WAITING_DELETE_SELECTION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.receive_delete_selection)
        ],
    },
    fallbacks=[CommandHandler('cancel', bot_handlers.cancel)],
    per_message=False
    )
    
    # Register handlers
    application.add_handler(CommandHandler("start", bot_handlers.start))
    application.add_handler(CommandHandler("help", bot_handlers.help))
    application.add_handler(CommandHandler("connect_calendar", bot_handlers.connect_calendar))
    application.add_handler(CommandHandler("list_events", bot_handlers.list_events))
    application.add_handler(CommandHandler("list_week", bot_handlers.list_week_events))
    application.add_handler(CommandHandler("ai", bot_handlers.ai_chat))
    
    # Add conversation handlers FIRST
    application.add_handler(add_event_conv)
    application.add_handler(delete_event_conv)
    
    # Then callback handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Finally message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, quick_button_handler))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Post init
    application.post_init = post_init
    
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()