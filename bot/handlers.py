"""
Telegram Bot Handlers
Handles all bot commands and interactions
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from datetime import datetime, timedelta
import re
import config
from services.google_calendar import GoogleCalendarService
from services.gemini_ai import GeminiAIService
from bot.keyboards import get_main_menu, get_calendar_menu, get_confirm_keyboard
from utils.helpers import format_event, parse_datetime_input

# Conversation states
WAITING_EVENT_TITLE = 1
WAITING_EVENT_DATE = 2
WAITING_EVENT_TIME = 3
WAITING_EVENT_DURATION = 4
WAITING_EVENT_LOCATION = 5
WAITING_EVENT_CONFIRM = 6
WAITING_DELETE_SELECTION = 7
WAITING_AI_CHAT = 8

class BotHandlers:
    def __init__(self):
        self.calendar_service = None
        self.ai_service = GeminiAIService()
        self.user_data = {}
    
    def init_calendar_service(self):
        """Initialize calendar service when needed"""
        if not self.calendar_service:
            try:
                self.calendar_service = GoogleCalendarService()
                return True
            except Exception as e:
                print(f"Error initializing calendar service: {e}")
                return False
        return True
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        welcome_message = (
            f"Halo {user.first_name}! 👋\n\n"
            "Saya adalah Calendar Assistant Bot Anda. "
            "Saya bisa membantu Anda:\n\n"
            "📅 Mengelola jadwal Google Calendar\n"
            "🤖 Chat dengan AI Assistant\n"
            "⏰ Set reminder untuk acara\n"
            "📝 Analisis dan optimasi jadwal\n\n"
            "Silakan pilih menu di bawah atau gunakan /help untuk bantuan."
        )
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=get_main_menu()
        )
    
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = (
            "📚 *PANDUAN PENGGUNAAN BOT*\n\n"
            "*Perintah Tersedia:*\n"
            "/start - Menu utama\n"
            "/help - Bantuan ini\n"
            "/add_event - Tambah jadwal baru\n"
            "/list_events - Lihat jadwal hari ini\n"
            "/list_week - Lihat jadwal minggu ini\n"
            "/delete_event - Hapus jadwal\n"
            "/ai - Chat dengan AI Assistant\n"
            "/connect_calendar - Hubungkan Google Calendar\n\n"
            "*Tips Penggunaan:*\n"
            "• Anda bisa chat langsung dengan AI untuk menambah jadwal\n"
            "• Contoh: 'Meeting dengan tim besok jam 2 siang'\n"
            "• AI akan otomatis mengekstrak informasi jadwal\n\n"
            "*Fitur AI:*\n"
            "• Analisis jadwal\n"
            "• Saran optimasi waktu\n"
            "• Personal assistant untuk reminder\n"
            "• Menjawab pertanyaan seputar produktivitas"
        )
        
        await update.message.reply_text(
            help_text,
            parse_mode='Markdown'
        )
    
    async def connect_calendar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle calendar connection"""
        await update.message.reply_text("🔄 Menghubungkan dengan Google Calendar...")
        
        if self.init_calendar_service():
            await update.message.reply_text(
                "✅ Berhasil terhubung dengan Google Calendar!\n"
                "Anda sekarang bisa mulai mengelola jadwal."
            )
        else:
            await update.message.reply_text(
                "❌ Gagal terhubung dengan Google Calendar.\n"
                "Pastikan file credentials.json sudah ada dan benar.\n"
                "Silakan ikuti panduan setup di README."
            )
    
    async def add_event_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start adding new event conversation"""
        if not self.init_calendar_service():
            await update.message.reply_text(
                "❌ Calendar belum terhubung. Gunakan /connect_calendar terlebih dahulu."
            )
            return ConversationHandler.END
        
        await update.message.reply_text(
            "📝 Mari tambahkan jadwal baru!\n\n"
            "Masukkan *judul acara*:",
            parse_mode='Markdown'
        )
        
        return WAITING_EVENT_TITLE
    
    async def receive_event_title(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive event title"""
        user_id = update.effective_user.id
        title = update.message.text
        
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        
        self.user_data[user_id]['event_title'] = title
        
        await update.message.reply_text(
            "📅 Masukkan *tanggal* acara\n"
            "Format: DD/MM/YYYY atau 'besok', 'lusa', dll:",
            parse_mode='Markdown'
        )
        
        return WAITING_EVENT_DATE
    
    async def receive_event_date(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive event date"""
        user_id = update.effective_user.id
        date_input = update.message.text
        
        try:
            event_date = parse_datetime_input(date_input)
            self.user_data[user_id]['event_date'] = event_date
            
            await update.message.reply_text(
                "⏰ Masukkan *waktu mulai*\n"
                "Format: HH:MM (contoh: 14:30 atau 2:30 PM):",
                parse_mode='Markdown'
            )
            
            return WAITING_EVENT_TIME
        except Exception as e:
            await update.message.reply_text(
                "❌ Format tanggal tidak valid. Coba lagi.\n"
                "Contoh: 25/12/2024 atau 'besok'"
            )
            return WAITING_EVENT_DATE
    
    async def receive_event_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive event time"""
        user_id = update.effective_user.id
        time_input = update.message.text
        
        try:
            # Parse time
            time_parts = re.findall(r'\d+', time_input)
            if len(time_parts) >= 2:
                hour = int(time_parts[0])
                minute = int(time_parts[1])
                
                # Handle PM
                if 'pm' in time_input.lower() and hour < 12:
                    hour += 12
                
                self.user_data[user_id]['event_hour'] = hour
                self.user_data[user_id]['event_minute'] = minute
                
                await update.message.reply_text(
                    "⏱️ Berapa lama durasi acara?\n"
                    "Contoh: '1 jam', '90 menit', '2 jam 30 menit':"
                )
                
                return WAITING_EVENT_DURATION
            else:
                raise ValueError("Invalid time format")
        except Exception as e:
            await update.message.reply_text(
                "❌ Format waktu tidak valid.\n"
                "Contoh: 14:30 atau 2:30 PM"
            )
            return WAITING_EVENT_TIME
    
    async def receive_event_duration(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive event duration"""
        user_id = update.effective_user.id
        duration_input = update.message.text.lower()
        
        try:
            # Parse duration
            hours = 0
            minutes = 0
            
            if 'jam' in duration_input:
                hours_match = re.search(r'(\d+)\s*jam', duration_input)
                if hours_match:
                    hours = int(hours_match.group(1))
            
            if 'menit' in duration_input:
                minutes_match = re.search(r'(\d+)\s*menit', duration_input)
                if minutes_match:
                    minutes = int(minutes_match.group(1))
            
            if hours == 0 and minutes == 0:
                # Default 1 hour
                hours = 1
            
            self.user_data[user_id]['duration_hours'] = hours
            self.user_data[user_id]['duration_minutes'] = minutes
            
            await update.message.reply_text(
                "📍 Masukkan *lokasi* (opsional, ketik 'skip' untuk lewati):",
                parse_mode='Markdown'
            )
            
            return WAITING_EVENT_LOCATION
        except Exception as e:
            await update.message.reply_text(
                "❌ Format durasi tidak valid.\n"
                "Contoh: '1 jam' atau '90 menit'"
            )
            return WAITING_EVENT_DURATION
    
    async def receive_event_location(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive event location and create event"""
        user_id = update.effective_user.id
        location = update.message.text
        
        if location.lower() != 'skip':
            self.user_data[user_id]['event_location'] = location
        
        # Create the event
        try:
            data = self.user_data[user_id]
            
            # Build start and end datetime
            start_datetime = data['event_date'].replace(
                hour=data['event_hour'],
                minute=data['event_minute']
            )
            
            end_datetime = start_datetime + timedelta(
                hours=data['duration_hours'],
                minutes=data['duration_minutes']
            )
            
            # Create event in Google Calendar
            event = self.calendar_service.create_event(
                summary=data['event_title'],
                start_time=start_datetime,
                end_time=end_datetime,
                location=data.get('event_location', ''),
                description=f"Created via Telegram Bot by {update.effective_user.first_name}"
            )
            
            # Send confirmation
            confirmation = (
                "✅ *Jadwal berhasil ditambahkan!*\n\n"
                f"📅 *Judul:* {data['event_title']}\n"
                f"📆 *Tanggal:* {start_datetime.strftime('%d/%m/%Y')}\n"
                f"⏰ *Waktu:* {start_datetime.strftime('%H:%M')} - {end_datetime.strftime('%H:%M')}\n"
            )
            
            if data.get('event_location'):
                confirmation += f"📍 *Lokasi:* {data['event_location']}\n"
            
            confirmation += f"\n🔗 [Lihat di Google Calendar]({event.get('htmlLink', '#')})"
            
            await update.message.reply_text(
                confirmation,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
            
            # Clear user data
            del self.user_data[user_id]
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ Gagal membuat jadwal: {str(e)}"
            )
        
        return ConversationHandler.END
    
    async def list_events(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """List today's events"""
        if not self.init_calendar_service():
            await update.message.reply_text(
                "❌ Calendar belum terhubung. Gunakan /connect_calendar terlebih dahulu."
            )
            return
        
        try:
            events = self.calendar_service.get_todays_events()
            
            if not events:
                await update.message.reply_text(
                    "📅 Tidak ada jadwal untuk hari ini.\n"
                    "Santai dan nikmati hari Anda! 😊"
                )
            else:
                message = "📅 *Jadwal Hari Ini:*\n\n"
                for event in events:
                    message += format_event(event) + "\n"
                
                await update.message.reply_text(
                    message,
                    parse_mode='Markdown',
                    disable_web_page_preview=True
                )
        except Exception as e:
            await update.message.reply_text(
                f"❌ Error mengambil jadwal: {str(e)}"
            )
    
    async def list_week_events(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """List this week's events"""
        if not self.init_calendar_service():
            await update.message.reply_text(
                "❌ Calendar belum terhubung. Gunakan /connect_calendar terlebih dahulu."
            )
            return
        
        try:
            events = self.calendar_service.get_week_events()
            
            if not events:
                await update.message.reply_text(
                    "📅 Tidak ada jadwal untuk minggu ini."
                )
            else:
                message = "📅 *Jadwal Minggu Ini:*\n\n"
                current_date = None
                
                for event in events:
                    event_date = event.get('start', {}).get('dateTime', '')[:10]
                    
                    if event_date != current_date:
                        current_date = event_date
                        date_obj = datetime.strptime(event_date, '%Y-%m-%d')
                        message += f"\n*{date_obj.strftime('%A, %d %B %Y')}*\n"
                    
                    message += format_event(event) + "\n"
                
                # Split message if too long
                if len(message) > 4000:
                    messages = [message[i:i+4000] for i in range(0, len(message), 4000)]
                    for msg in messages:
                        await update.message.reply_text(
                            msg,
                            parse_mode='Markdown',
                            disable_web_page_preview=True
                        )
                else:
                    await update.message.reply_text(
                        message,
                        parse_mode='Markdown',
                        disable_web_page_preview=True
                    )
        except Exception as e:
            await update.message.reply_text(
                f"❌ Error mengambil jadwal: {str(e)}"
            )
    
    async def delete_event_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start delete event conversation"""
        if not self.init_calendar_service():
            await update.message.reply_text(
                "❌ Calendar belum terhubung. Gunakan /connect_calendar terlebih dahulu."
            )
            return ConversationHandler.END
        
        try:
            # Get upcoming events
            events = self.calendar_service.list_events(max_results=10)
            
            if not events:
                await update.message.reply_text(
                    "📅 Tidak ada jadwal yang bisa dihapus."
                )
                return ConversationHandler.END
            
            # Store events in context
            user_id = update.effective_user.id
            if user_id not in self.user_data:
                self.user_data[user_id] = {}
            self.user_data[user_id]['events_to_delete'] = events
            
            # Create selection menu
            message = "🗑️ *Pilih jadwal yang akan dihapus:*\n\n"
            for i, event in enumerate(events, 1):
                message += f"{i}. {format_event(event)}\n"
            
            message += "\nKetik nomor jadwal atau 'cancel' untuk batal:"
            
            await update.message.reply_text(
                message,
                parse_mode='Markdown'
            )
            
            return WAITING_DELETE_SELECTION
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ Error: {str(e)}"
            )
            return ConversationHandler.END
    
    async def receive_delete_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle delete selection"""
        user_id = update.effective_user.id
        selection = update.message.text
        
        if selection.lower() == 'cancel':
            await update.message.reply_text("❌ Penghapusan dibatalkan.")
            return ConversationHandler.END
        
        try:
            index = int(selection) - 1
            events = self.user_data[user_id]['events_to_delete']
            
            if 0 <= index < len(events):
                event = events[index]
                event_id = event['id']
                
                # Delete the event
                self.calendar_service.delete_event(event_id)
                
                await update.message.reply_text(
                    f"✅ Jadwal '{event.get('summary', 'Untitled')}' berhasil dihapus!"
                )
            else:
                await update.message.reply_text("❌ Nomor tidak valid.")
            
        except ValueError:
            await update.message.reply_text("❌ Masukkan nomor yang valid.")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
        
        # Clean up
        if user_id in self.user_data:
            del self.user_data[user_id]
        
        return ConversationHandler.END
    
    async def ai_chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle AI chat"""
        message = update.message.text
        user_id = str(update.effective_user.id)
        
        # Remove /ai command if present
        if message.startswith('/ai'):
            message = message[3:].strip()
        
        if not message:
            await update.message.reply_text(
                "💬 Silakan ketik pesan Anda setelah /ai\n"
                "Contoh: /ai bantu saya mengatur jadwal minggu ini"
            )
            return
        
        # Send typing action
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action='typing'
        )
        
        # Check if message contains schedule information
        result = self.ai_service.parse_schedule_from_text(message, user_id)
        
        if result['type'] == 'schedule' and self.init_calendar_service():
            # Extract schedule data
            data = result.get('data', {})
            
            if data.get('action') == 'create_event':
                try:
                    # Parse dates and times
                    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
                    start_time = datetime.strptime(data['start_time'], '%H:%M').time()
                    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
                    end_time = datetime.strptime(data['end_time'], '%H:%M').time()
                    
                    start_datetime = datetime.combine(start_date, start_time)
                    start_datetime = config.TIMEZONE.localize(start_datetime)
                    end_datetime = datetime.combine(end_date, end_time)
                    end_datetime = config.TIMEZONE.localize(end_datetime)
                    
                    # Create event
                    event = self.calendar_service.create_event(
                        summary=data['title'],
                        start_time=start_datetime,
                        end_time=end_datetime,
                        location=data.get('location', ''),
                        description=data.get('description', '')
                    )
                    
                    response = (
                        "✅ Jadwal berhasil ditambahkan!\n\n"
                        f"📅 {data['title']}\n"
                        f"📆 {start_datetime.strftime('%d/%m/%Y %H:%M')}\n"
                        f"📍 {data.get('location', 'No location')}"
                    )
                    
                    await update.message.reply_text(response)
                except Exception as e:
                    await update.message.reply_text(
                        f"AI mendeteksi jadwal, tapi gagal membuat: {str(e)}\n\n"
                        f"Response AI: {result.get('message', '')}"
                    )
        else:
            # Regular chat response
            response = result.get('message', 'Maaf, tidak bisa memproses permintaan Anda.')
            await update.message.reply_text(response)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages (AI chat)"""
        await self.ai_chat(update, context)
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel current operation"""
        await update.message.reply_text(
            "❌ Operasi dibatalkan.",
            reply_markup=get_main_menu()
        )
        return ConversationHandler.END