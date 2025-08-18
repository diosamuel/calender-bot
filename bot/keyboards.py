"""
Telegram Bot Keyboards
Custom keyboard layouts for bot interactions
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    """Get main menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("📅 Tambah Jadwal", callback_data='add_event'),
            InlineKeyboardButton("📋 Lihat Jadwal", callback_data='list_events')
        ],
        [
            InlineKeyboardButton("🗓️ Jadwal Minggu", callback_data='list_week'),
            InlineKeyboardButton("🗑️ Hapus Jadwal", callback_data='delete_event')
        ],
        [
            InlineKeyboardButton("🤖 AI Assistant", callback_data='ai_chat'),
            InlineKeyboardButton("⚙️ Settings", callback_data='settings')
        ],
        [
            InlineKeyboardButton("📚 Bantuan", callback_data='help')
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_calendar_menu():
    """Get calendar specific menu"""
    keyboard = [
        [
            InlineKeyboardButton("📅 Hari Ini", callback_data='today'),
            InlineKeyboardButton("📅 Besok", callback_data='tomorrow')
        ],
        [
            InlineKeyboardButton("🗓️ Minggu Ini", callback_data='this_week'),
            InlineKeyboardButton("🗓️ Bulan Ini", callback_data='this_month')
        ],
        [
            InlineKeyboardButton("🔍 Cari Jadwal", callback_data='search'),
            InlineKeyboardButton("📊 Analisis", callback_data='analyze')
        ],
        [
            InlineKeyboardButton("🔙 Menu Utama", callback_data='main_menu')
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_confirm_keyboard():
    """Get confirmation keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Ya", callback_data='confirm_yes'),
            InlineKeyboardButton("❌ Tidak", callback_data='confirm_no')
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_quick_reply_keyboard():
    """Get quick reply keyboard for common actions"""
    keyboard = [
        [
            KeyboardButton("📅 Tambah Jadwal"),
            KeyboardButton("📋 Lihat Hari Ini")
        ],
        [
            KeyboardButton("🗓️ Lihat Minggu"),
            KeyboardButton("🗑️ Hapus Jadwal")  # TAMBAHKAN INI
        ],
        [
            KeyboardButton("🤖 Chat AI"),
            KeyboardButton("📚 Bantuan")
        ]
    ]
    
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_time_selection_keyboard():
    """Get time selection keyboard"""
    keyboard = []
    
    # Morning times
    morning_row = []
    for hour in range(6, 12):
        morning_row.append(
            InlineKeyboardButton(f"{hour:02d}:00", callback_data=f"time_{hour:02d}:00")
        )
    keyboard.append(morning_row[:3])
    keyboard.append(morning_row[3:])
    
    # Afternoon times
    afternoon_row = []
    for hour in range(12, 18):
        afternoon_row.append(
            InlineKeyboardButton(f"{hour:02d}:00", callback_data=f"time_{hour:02d}:00")
        )
    keyboard.append(afternoon_row[:3])
    keyboard.append(afternoon_row[3:])
    
    # Evening times
    evening_row = []
    for hour in range(18, 22):
        evening_row.append(
            InlineKeyboardButton(f"{hour:02d}:00", callback_data=f"time_{hour:02d}:00")
        )
    keyboard.append(evening_row)
    
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data='back')])
    
    return InlineKeyboardMarkup(keyboard)

def get_duration_keyboard():
    """Get duration selection keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("30 menit", callback_data='duration_30'),
            InlineKeyboardButton("1 jam", callback_data='duration_60')
        ],
        [
            InlineKeyboardButton("1.5 jam", callback_data='duration_90'),
            InlineKeyboardButton("2 jam", callback_data='duration_120')
        ],
        [
            InlineKeyboardButton("3 jam", callback_data='duration_180'),
            InlineKeyboardButton("Seharian", callback_data='duration_all_day')
        ],
        [
            InlineKeyboardButton("🔙 Kembali", callback_data='back')
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_settings_keyboard():
    """Get settings menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("🔔 Notifikasi", callback_data='settings_notifications'),
            InlineKeyboardButton("🌍 Timezone", callback_data='settings_timezone')
        ],
        [
            InlineKeyboardButton("🔗 Reconnect Calendar", callback_data='settings_reconnect'),
            InlineKeyboardButton("🧹 Clear AI History", callback_data='settings_clear_ai')
        ],
        [
            InlineKeyboardButton("🔙 Menu Utama", callback_data='main_menu')
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)