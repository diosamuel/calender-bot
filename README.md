# 🤖 Telegram Calendar Bot dengan AI Assistant

Bot Telegram yang terintegrasi dengan Google Calendar dan AI Assistant (Gemini) untuk membantu mengelola jadwal dan sebagai personal assistant.

## ✨ Fitur Utama

- 📅 **Manajemen Jadwal**: Tambah, hapus, edit jadwal di Google Calendar
- 🤖 **AI Assistant**: Chat dengan AI untuk bantuan scheduling dan produktivitas  
- ⏰ **Smart Scheduling**: Buat jadwal dari chat natural language
- 📊 **Analisis Jadwal**: AI menganalisis dan memberikan saran optimasi jadwal
- 🔍 **Natural Language Processing**: AI mengerti perintah dalam bahasa sehari-hari
- 🌍 **Timezone Support**: Dukungan multi-timezone

## 📸 Screenshots

<details>
<summary>Klik untuk melihat screenshots</summary>

### Menu Utama
```
Halo [Nama]! 👋

Saya adalah Calendar Assistant Bot Anda.

📅 Cara Menggunakan Bot:
• Gunakan tombol menu di bawah
• Atau ketik perintah langsung
• Atau chat langsung untuk membuat jadwal

💡 Contoh Chat untuk Jadwal:
'Meeting dengan tim besok jam 2 siang'
'Rapat di kantor hari Senin pukul 10:00'

[📅 Tambah Jadwal] [📋 Lihat Hari Ini]
[🗓️ Lihat Minggu] [🗑️ Hapus Jadwal]
[🤖 Chat AI] [📚 Bantuan]
```

</details>

## 📋 Prerequisites

Sebelum memulai, pastikan Anda memiliki:

- ✅ Python 3.8 atau lebih baru
- ✅ Akun Google dengan akses Google Calendar
- ✅ Bot Telegram (dari @BotFather)
- ✅ API Key Gemini (Google AI)
- ✅ Koneksi internet stabil

## 🚀 Setup Lengkap

### Langkah 1: Clone/Download Project

```bash
# Buat folder project
mkdir telegram-calendar-bot
cd telegram-calendar-bot

# Atau clone dari repository (jika ada)
git clone [URL_REPOSITORY]
```

### Langkah 2: Struktur Folder

Buat struktur folder seperti ini:

```
telegram-calendar-bot/
├── .env                    # Environment variables (buat sendiri)
├── credentials.json        # Google OAuth (download dari Google)
├── main.py                # Main application
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── bot/
│   ├── __init__.py
│   ├── handlers.py        # Command handlers
│   └── keyboards.py       # Keyboard layouts
├── services/
│   ├── __init__.py
│   ├── google_calendar.py # Calendar service
│   └── gemini_ai.py       # AI service
└── utils/
    ├── __init__.py
    └── helpers.py         # Helper functions
```

### Langkah 3: Install Dependencies

```bash
# Install menggunakan pip
pip install -r requirements.txt
```

Atau install manual:

```bash
pip install python-telegram-bot==20.3 \
            google-auth==2.25.2 \
            google-auth-oauthlib==1.2.0 \
            google-auth-httplib2==0.2.0 \
            google-api-python-client==2.111.0 \
            python-dotenv==1.0.0 \
            google-generativeai==0.3.2 \
            pytz==2023.3.post1
```

### Langkah 4: Setup Bot Telegram

1. **Buka Telegram** dan cari **@BotFather**

2. **Buat Bot Baru:**
   ```
   /newbot
   ```

3. **Ikuti instruksi BotFather:**
   - Nama bot: `My Calendar Assistant` (atau nama lain)
   - Username: `mycalendar_bot` (harus unik dan berakhiran 'bot')

4. **Simpan Token** yang diberikan:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

5. **Setup Commands** (opsional):
   ```
   /setcommands
   ```
   Lalu paste:
   ```
   start - Menu utama
   help - Bantuan penggunaan
   add_event - Tambah jadwal baru
   list_events - Lihat jadwal hari ini
   list_week - Lihat jadwal minggu ini
   delete_event - Hapus jadwal
   ai - Chat dengan AI Assistant
   connect_calendar - Hubungkan Google Calendar
   ```

### Langkah 5: Setup Google Calendar API

#### A. Buat Project di Google Cloud Console

1. Buka [Google Cloud Console](https://console.cloud.google.com/)
2. Klik **"Create Project"** atau **"Select Project"** > **"New Project"**
3. Beri nama project (contoh: "Telegram Calendar Bot")
4. Klik **"Create"**

#### B. Enable Google Calendar API

1. Di dashboard, klik **"+ ENABLE APIS AND SERVICES"**
2. Cari **"Google Calendar API"**
3. Klik API tersebut, lalu klik **"ENABLE"**

#### C. Buat OAuth 2.0 Credentials

1. Pergi ke **"APIs & Services"** > **"Credentials"**
2. Klik **"+ CREATE CREDENTIALS"** > **"OAuth client ID"**

3. **Jika diminta Configure Consent Screen:**
   - Pilih **"External"**
   - Isi informasi dasar:
     - App name: `Telegram Calendar Bot`
     - User support email: (email Anda)
     - Developer contact: (email Anda)
   - Klik **"Save and Continue"**
   - Di Scopes, klik **"Save and Continue"**
   - Di Test users, klik **"+ ADD USERS"**
   - Tambahkan email Anda
   - Klik **"Save and Continue"**

4. **Kembali ke Create OAuth client ID:**
   - Application type: **"Desktop app"**
   - Name: `Telegram Bot Client`
   - Klik **"Create"**

5. **Download JSON:**
   - Klik tombol download
   - Rename file menjadi `credentials.json`
   - Pindahkan ke folder project

### Langkah 6: Setup Gemini API

1. Buka [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Klik **"Create API Key"**
3. Pilih project atau buat baru
4. Copy API key yang diberikan

### Langkah 7: Konfigurasi Environment Variables

Buat file `.env` di folder project:

```bash
# Bot Telegram Token dari BotFather
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE

# API Key Gemini
GEMINI_API_KEY=YOUR_GEMINI_KEY_HERE

# Timezone (sesuaikan dengan lokasi)
TIMEZONE=Asia/Jakarta

# Telegram ID Anda (optional, untuk fitur admin)
ADMIN_ID=YOUR_TELEGRAM_ID
```

**Cara mendapatkan Telegram ID:**
1. Start bot [@userinfobot](https://t.me/userinfobot) di Telegram
2. Bot akan mengirim ID Anda

### Langkah 8: First Run & Authorization

```bash
python main.py
```

**Pada run pertama:**
1. Browser akan terbuka otomatis
2. Login dengan akun Google Anda
3. Jika muncul warning "This app isn't verified":
   - Klik **"Advanced"**
   - Klik **"Go to [App Name] (unsafe)"**
4. Allow permissions untuk Calendar
5. Setelah sukses, window browser bisa ditutup
6. File `token.json` akan dibuat otomatis

### Langkah 9: Test Bot

1. **Buka Telegram**
2. **Cari bot Anda** dengan username yang dibuat
3. **Klik Start** atau kirim `/start`
4. **Test fitur:**
   - Klik tombol "📚 Bantuan" untuk panduan
   - Coba buat jadwal dengan chat: "Meeting besok jam 2 siang"

## 📱 Cara Penggunaan

### 🎯 Quick Start

```
1. Kirim: /start
2. Pilih menu yang diinginkan
3. Atau langsung chat untuk buat jadwal
```

### 📝 Perintah Tersedia

| Command | Deskripsi |
|---------|-----------|
| `/start` | Menu utama dan welcome message |
| `/help` | Panduan lengkap penggunaan |
| `/add_event` | Tambah jadwal (step by step) |
| `/list_events` | Lihat jadwal hari ini |
| `/list_week` | Lihat jadwal minggu ini |
| `/delete_event` | Hapus jadwal |
| `/ai [pesan]` | Chat dengan AI Assistant |
| `/connect_calendar` | Hubungkan/reconnect Google Calendar |

### 💬 Contoh Penggunaan

#### 1. Buat Jadwal dengan Chat Natural:
```
"Meeting dengan tim besok jam 2 siang di Zoom"
"Dinner dengan client Jumat jam 7 malam di Hotel X"
"Olahraga setiap Senin jam 6 pagi"
```

#### 2. Gunakan AI Assistant:
```
/ai analisis jadwal saya minggu ini
/ai beri tips untuk meningkatkan produktivitas
/ai kapan waktu terbaik untuk meeting minggu depan?
```

#### 3. Step by Step (Gunakan /add_event):
```
Bot: Masukkan judul acara
You: Meeting Project ABC

Bot: Masukkan tanggal
You: besok

Bot: Masukkan waktu mulai
You: 14:30

Bot: Berapa lama durasi?
You: 2 jam

Bot: Masukkan lokasi
You: Zoom Meeting Room
```

### 📅 Format Input yang Diterima

#### Tanggal:
- `25/12/2024` atau `25-12-2024`
- `hari ini`, `besok`, `lusa`
- `Senin`, `Selasa`, dst (minggu ini)
- `minggu depan`, `bulan depan`

#### Waktu:
- `14:30` atau `2:30 PM`
- `jam 2 siang`, `pukul 10 pagi`
- `10:00`, `10.00`

#### Durasi:
- `1 jam`, `2 jam`
- `30 menit`, `90 menit`
- `2 jam 30 menit`

## 🔧 Troubleshooting

### ❌ Error: "Calendar belum terhubung"

**Solusi:**
1. Jalankan `/connect_calendar`
2. Pastikan file `credentials.json` ada di folder project
3. Check apakah Google Calendar API sudah enabled

### ❌ Error saat authorization Google

**Solusi:**
1. Pastikan menggunakan browser default
2. Delete file `token.json` jika ada
3. Jalankan ulang bot
4. Ulangi proses authorization

### ❌ Bot tidak merespon

**Solusi:**
1. Check token bot di file `.env`
2. Pastikan format token benar
3. Check koneksi internet
4. Restart bot dengan `Ctrl+C` lalu `python main.py`

### ❌ AI tidak berfungsi

**Solusi:**
1. Check Gemini API key di `.env`
2. Pastikan API key valid dan aktif
3. Check quota API di Google AI Studio

### ❌ Error "Can't parse entities"

**Solusi:**
1. Biasanya karena markdown formatting
2. Bot akan tetap berfungsi normal
3. Abaikan error ini

### ❌ Error "ExtBot is not properly initialized"

**Solusi:**
1. Downgrade python-telegram-bot ke versi 20.3
```bash
pip uninstall python-telegram-bot
pip install python-telegram-bot==20.3
```

## 🛡️ Security Best Practices

### ⚠️ File Sensitif

**JANGAN PERNAH** share atau upload file berikut:
- `.env` - Berisi API keys dan tokens
- `credentials.json` - OAuth credentials Google
- `token.json` - Token akses Google Calendar

### 📝 Gunakan .gitignore

Jika menggunakan Git, buat file `.gitignore`:

```gitignore
# Environment variables
.env

# Google credentials
credentials.json
token.json

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

## 🚀 Deployment (Optional)

### Deploy ke VPS/Server

1. **Setup VPS (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

2. **Clone project:**
```bash
cd /home/user
git clone [repository]
cd telegram-calendar-bot
```

3. **Install dependencies:**
```bash
pip3 install -r requirements.txt
```

4. **Setup environment:**
```bash
nano .env
# Paste configuration
```

5. **Gunakan systemd service:**

Buat file `/etc/systemd/system/telegram-bot.service`:

```ini
[Unit]
Description=Telegram Calendar Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/user/telegram-calendar-bot
ExecStart=/usr/bin/python3 /home/user/telegram-calendar-bot/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

6. **Start service:**
```bash
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

### Deploy ke Heroku (Free Alternative)

1. **Install Heroku CLI**
2. **Buat `Procfile`:**
```
worker: python main.py
```

3. **Deploy:**
```bash
heroku create your-bot-name
heroku config:set TELEGRAM_BOT_TOKEN=xxx
heroku config:set GEMINI_API_KEY=xxx
git push heroku main
heroku ps:scale worker=1
```

## 📊 Monitoring

### Check Logs:
```bash
# Systemd
sudo journalctl -u telegram-bot -f

# Heroku
heroku logs --tail
```

### Bot Status:
```bash
# Systemd
sudo systemctl status telegram-bot

# Manual check
ps aux | grep main.py
```

## 🗂️ File Structure Lengkap

```
telegram-calendar-bot/
├── .env                        # Environment variables
├── .gitignore                  # Git ignore file
├── README.md                   # Documentation
├── requirements.txt            # Python dependencies
├── credentials.json            # Google OAuth credentials
├── token.json                  # Google access token (auto-generated)
├── main.py                     # Main application entry point
├── config.py                   # Configuration settings
│
├── bot/                        # Bot related modules
│   ├── __init__.py
│   ├── handlers.py            # Command and message handlers
│   └── keyboards.py           # Keyboard layouts
│
├── services/                   # External service integrations
│   ├── __init__.py
│   ├── google_calendar.py    # Google Calendar API service
│   └── gemini_ai.py          # Gemini AI service
│
└── utils/                      # Utility functions
    ├── __init__.py
    └── helpers.py             # Helper functions
```

## 📦 Dependencies

```txt
python-telegram-bot==20.3
google-auth==2.25.2
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0
google-api-python-client==2.111.0
python-dotenv==1.0.0
google-generativeai==0.3.2
pytz==2023.3.post1
```

## 🎯 Fitur Mendatang (Roadmap)

- [ ] 🔔 Reminder otomatis sebelum event
- [ ] 📧 Integrasi dengan Gmail
- [ ] 📊 Dashboard analytics
- [ ] 🌐 Multi-language support
- [ ] 👥 Group calendar management
- [ ] 📱 Mobile app companion
- [ ] 🔄 Sync dengan calendar lain (Outlook, Apple)
- [ ] 🎨 Custom themes
- [ ] 📈 Productivity insights
- [ ] 🤝 Meeting scheduler dengan multiple participants

## 🐛 Known Issues

1. **Markdown parsing error** - Tidak mempengaruhi fungsi bot
2. **Inline keyboard limitations** - Gunakan reply keyboard untuk conversation
3. **Timezone handling** - Pastikan timezone di .env sesuai lokasi

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

### How to Contribute:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

Created with ❤️ for personal productivity

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [Google Calendar API](https://developers.google.com/calendar) - Calendar integration
- [Google Gemini AI](https://ai.google.dev/) - AI Assistant
- [pytz](https://pythonhosted.org/pytz/) - Timezone handling

## 📞 Support

Jika ada pertanyaan atau masalah:
1. Check dokumentasi ini
2. Lihat [Troubleshooting](#-troubleshooting)
3. Buat issue di repository
4. Contact: [your-email@example.com]

## 📈 Version History

- **v1.0.0** (Current)
  - Initial release
  - Basic calendar management
  - AI integration
  - Natural language processing

---

**Happy Scheduling! 🎉**

*Bot ini dibuat untuk memudahkan manajemen jadwal Anda. Gunakan dengan bijak!*

<div align="center">
Made with ❤️ and ☕
</div>