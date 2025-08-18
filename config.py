"""
Configuration file for Telegram Calendar Bot
"""
import os
from dotenv import load_dotenv
import pytz

# Load environment variables
load_dotenv()

# Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')  # Optional admin ID

# Gemini Configuration  
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Timezone Configuration
TIMEZONE_STR = os.getenv('TIMEZONE', 'Asia/Jakarta')
TIMEZONE = pytz.timezone(TIMEZONE_STR)

# Google Calendar Configuration
GOOGLE_CREDENTIALS_FILE = 'credentials.json'
GOOGLE_TOKEN_FILE = 'token.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Bot Commands
COMMANDS = {
    'start': 'Mulai bot dan lihat menu utama',
    'help': 'Lihat bantuan penggunaan bot',
    'add_event': 'Tambah jadwal baru',
    'list_events': 'Lihat jadwal hari ini',
    'list_week': 'Lihat jadwal minggu ini',
    'delete_event': 'Hapus jadwal',
    'ai': 'Chat dengan AI Assistant',
    'reminder': 'Set reminder',
    'connect_calendar': 'Hubungkan dengan Google Calendar'
}

# Logging Configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# Debug (untuk testing)
if __name__ == "__main__":
    print(f"Token: {TELEGRAM_BOT_TOKEN}")
    print(f"Admin ID: {ADMIN_ID}")
    print(f"Gemini API: {GEMINI_API_KEY}")