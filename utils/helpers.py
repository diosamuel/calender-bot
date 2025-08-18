"""
Helper functions for the bot
"""
from datetime import datetime, timedelta
import re
import config

def format_event(event):
    """Format a Google Calendar event for display"""
    summary = event.get('summary', 'Untitled Event')
    
    # Get start time
    start = event.get('start', {})
    if 'dateTime' in start:
        start_dt = datetime.fromisoformat(start['dateTime'].replace('Z', '+00:00'))
        start_str = start_dt.strftime('%H:%M')
    elif 'date' in start:
        start_str = 'All day'
    else:
        start_str = 'Unknown time'
    
    # Get end time
    end = event.get('end', {})
    if 'dateTime' in end:
        end_dt = datetime.fromisoformat(end['dateTime'].replace('Z', '+00:00'))
        end_str = end_dt.strftime('%H:%M')
    elif 'date' in end:
        end_str = ''
    else:
        end_str = 'Unknown time'
    
    # Build formatted string
    formatted = f"• *{start_str}"
    if end_str:
        formatted += f" - {end_str}"
    formatted += f"* {summary}"
    
    # Add location if available
    if event.get('location'):
        formatted += f"\n  📍 {event['location']}"
    
    # Add description snippet if available
    if event.get('description'):
        desc = event['description'][:50]
        if len(event['description']) > 50:
            desc += '...'
        formatted += f"\n  📝 {desc}"
    
    return formatted

def parse_datetime_input(text):
    """Parse various datetime input formats"""
    text = text.lower().strip()
    now = datetime.now(config.TIMEZONE)
    
    # Handle relative dates
    if text in ['hari ini', 'today']:
        return now
    elif text in ['besok', 'tomorrow']:
        return now + timedelta(days=1)
    elif text in ['lusa', 'day after tomorrow']:
        return now + timedelta(days=2)
    elif 'minggu depan' in text or 'next week' in text:
        return now + timedelta(weeks=1)
    elif 'bulan depan' in text or 'next month' in text:
        # Approximate - add 30 days
        return now + timedelta(days=30)
    
    # Try to parse DD/MM/YYYY format
    date_pattern = r'(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{2,4})'
    match = re.search(date_pattern, text)
    if match:
        day = int(match.group(1))
        month = int(match.group(2))
        year = int(match.group(3))
        
        # Handle 2-digit year
        if year < 100:
            year += 2000
        
        return config.TIMEZONE.localize(datetime(year, month, day))
    
    # Try to parse YYYY-MM-DD format
    date_pattern2 = r'(\d{4})[/\-.](\d{1,2})[/\-.](\d{1,2})'
    match = re.search(date_pattern2, text)
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        
        return config.TIMEZONE.localize(datetime(year, month, day))
    
    # Try to parse day names
    days = {
        'senin': 0, 'monday': 0,
        'selasa': 1, 'tuesday': 1,
        'rabu': 2, 'wednesday': 2,
        'kamis': 3, 'thursday': 3,
        'jumat': 4, 'friday': 4,
        'sabtu': 5, 'saturday': 5,
        'minggu': 6, 'sunday': 6
    }
    
    for day_name, day_num in days.items():
        if day_name in text:
            days_ahead = day_num - now.weekday()
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            return now + timedelta(days=days_ahead)
    
    raise ValueError(f"Could not parse date: {text}")

def parse_time_input(text):
    """Parse time input"""
    text = text.lower().strip()
    
    # Remove common words
    text = text.replace('jam', '').replace('pukul', '').replace('at', '').strip()
    
    # Handle format HH:MM
    time_pattern = r'(\d{1,2})[:\.](\d{2})'
    match = re.search(time_pattern, text)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        
        # Handle AM/PM
        if 'pm' in text and hour < 12:
            hour += 12
        elif 'am' in text and hour == 12:
            hour = 0
        
        return hour, minute
    
    # Handle single number (assume hour)
    single_num = re.search(r'(\d{1,2})', text)
    if single_num:
        hour = int(single_num.group(1))
        
        # Handle PM
        if 'malam' in text or 'sore' in text or 'pm' in text:
            if hour < 12:
                hour += 12
        elif 'pagi' in text or 'am' in text:
            if hour == 12:
                hour = 0
        
        return hour, 0
    
    raise ValueError(f"Could not parse time: {text}")

def get_greeting():
    """Get appropriate greeting based on time"""
    hour = datetime.now(config.TIMEZONE).hour
    
    if 5 <= hour < 12:
        return "Selamat pagi"
    elif 12 <= hour < 15:
        return "Selamat siang"
    elif 15 <= hour < 18:
        return "Selamat sore"
    else:
        return "Selamat malam"

def format_duration(minutes):
    """Format duration in minutes to readable string"""
    if minutes < 60:
        return f"{minutes} menit"
    
    hours = minutes // 60
    mins = minutes % 60
    
    if mins == 0:
        return f"{hours} jam"
    else:
        return f"{hours} jam {mins} menit"

def get_event_emoji(event_title):
    """Get appropriate emoji for event based on title"""
    title_lower = event_title.lower()
    
    emoji_map = {
        'meeting': '👥',
        'rapat': '👥',
        'birthday': '🎂',
        'ultah': '🎂',
        'lunch': '🍽️',
        'makan': '🍽️',
        'dinner': '🍽️',
        'breakfast': '🍳',
        'sarapan': '🍳',
        'gym': '🏋️',
        'workout': '🏋️',
        'olahraga': '🏃',
        'doctor': '👨‍⚕️',
        'dokter': '👨‍⚕️',
        'dentist': '🦷',
        'study': '📚',
        'belajar': '📚',
        'exam': '📝',
        'ujian': '📝',
        'flight': '✈️',
        'pesawat': '✈️',
        'travel': '🧳',
        'liburan': '🏖️',
        'vacation': '🏖️',
        'call': '📞',
        'telpon': '📞',
        'zoom': '💻',
        'online': '💻',
        'deadline': '⏰',
        'presentation': '📊',
        'presentasi': '📊',
        'interview': '🤝',
        'wawancara': '🤝',
        'date': '❤️',
        'kencan': '❤️',
        'party': '🎉',
        'pesta': '🎉',
        'wedding': '💒',
        'nikah': '💒',
        'shopping': '🛍️',
        'belanja': '🛍️',
        'coffee': '☕',
        'kopi': '☕',
        'movie': '🎬',
        'film': '🎬',
        'concert': '🎵',
        'konser': '🎵',
        'sport': '⚽',
        'game': '🎮',
        'church': '⛪',
        'gereja': '⛪',
        'mosque': '🕌',
        'masjid': '🕌',
        'pray': '🙏',
        'ibadah': '🙏'
    }
    
    for keyword, emoji in emoji_map.items():
        if keyword in title_lower:
            return emoji
    
    return '📅'  # Default calendar emoji

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def truncate_text(text, max_length=100):
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + '...'