"""
Gemini AI Service
Handles AI interactions using Google's Gemini API
"""
import google.generativeai as genai
from typing import Dict, List, Optional
from datetime import datetime
import config
import json

class GeminiAIService:
    def __init__(self):
        """Initialize Gemini AI service"""
        genai.configure(api_key=config.GEMINI_API_KEY)
        
        # Configure the model
        self.model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            generation_config={
                'temperature': 0.7,
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 2048,
            }
        )
        
        # System prompt for calendar assistant
        self.system_prompt = """
        Kamu adalah asisten pribadi yang membantu mengelola jadwal dan calendar.
        Tugasmu adalah:
        1. Membantu menganalisis jadwal dari teks user
        2. Memberikan saran waktu yang tepat untuk kegiatan
        3. Mengingatkan hal-hal penting
        4. Menjawab pertanyaan seputar manajemen waktu
        5. Membantu mengekstrak informasi jadwal dari pesan user
        
        Ketika user memberikan informasi jadwal, ekstrak:
        - Judul kegiatan
        - Tanggal dan waktu mulai
        - Tanggal dan waktu selesai
        - Lokasi (jika ada)
        - Deskripsi (jika ada)
        
        Format output untuk jadwal baru dalam JSON:
        {
            "action": "create_event",
            "title": "...",
            "start_date": "YYYY-MM-DD",
            "start_time": "HH:MM",
            "end_date": "YYYY-MM-DD",
            "end_time": "HH:MM",
            "location": "...",
            "description": "..."
        }
        
        Jika tidak ada informasi jadwal, berikan response normal sebagai asisten.
        """
        
        # Chat history storage (per user)
        self.chat_histories = {}
    
    def parse_schedule_from_text(self, text: str, user_id: str = None) -> Dict:
        """
        Parse schedule information from natural language text
        """
        prompt = f"""
        {self.system_prompt}
        
        Pesan dari user: "{text}"
        
        Analisis pesan di atas. Jika ada informasi jadwal, ekstrak dalam format JSON.
        Jika tidak ada informasi jadwal, berikan response sebagai asisten biasa.
        Gunakan timezone {config.TIMEZONE_STR}.
        Tanggal hari ini: {datetime.now(config.TIMEZONE).strftime('%Y-%m-%d %H:%M')}
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Try to extract JSON if present
            if '{' in response_text and '}' in response_text:
                # Find JSON in response
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                json_str = response_text[start_idx:end_idx]
                
                try:
                    parsed_data = json.loads(json_str)
                    return {
                        'type': 'schedule',
                        'data': parsed_data,
                        'message': response_text
                    }
                except json.JSONDecodeError:
                    pass
            
            # Return as regular chat if no schedule found
            return {
                'type': 'chat',
                'message': response_text
            }
            
        except Exception as e:
            return {
                'type': 'error',
                'message': f'Error processing request: {str(e)}'
            }
    
    def chat(self, message: str, user_id: str = None, context: List[Dict] = None) -> str:
        """
        General chat with AI assistant
        """
        # Initialize chat history for user if not exists
        if user_id and user_id not in self.chat_histories:
            self.chat_histories[user_id] = []
        
        # Build conversation context
        conversation = []
        
        # Add system prompt
        conversation.append(f"System: {self.system_prompt}")
        
        # Add context if provided
        if context:
            for ctx in context[-5:]:  # Last 5 messages for context
                role = ctx.get('role', 'user')
                content = ctx.get('content', '')
                conversation.append(f"{role}: {content}")
        
        # Add user history if available
        if user_id and self.chat_histories.get(user_id):
            for hist in self.chat_histories[user_id][-5:]:  # Last 5 exchanges
                conversation.append(hist)
        
        # Add current message
        conversation.append(f"User: {message}")
        
        # Generate response
        full_prompt = "\n".join(conversation)
        
        try:
            response = self.model.generate_content(full_prompt)
            response_text = response.text
            
            # Store in history
            if user_id:
                self.chat_histories[user_id].append(f"User: {message}")
                self.chat_histories[user_id].append(f"Assistant: {response_text}")
                
                # Keep only last 20 messages
                if len(self.chat_histories[user_id]) > 20:
                    self.chat_histories[user_id] = self.chat_histories[user_id][-20:]
            
            return response_text
            
        except Exception as e:
            return f"Maaf, terjadi kesalahan: {str(e)}"
    
    def generate_reminder_message(self, event: Dict) -> str:
        """
        Generate a reminder message for an event
        """
        prompt = f"""
        Buat pesan reminder yang friendly dan helpful untuk jadwal berikut:
        
        Judul: {event.get('summary', 'Acara')}
        Waktu: {event.get('start', {}).get('dateTime', '')}
        Lokasi: {event.get('location', 'Tidak ada lokasi')}
        Deskripsi: {event.get('description', 'Tidak ada deskripsi')}
        
        Buat pesan reminder yang:
        1. Singkat dan jelas
        2. Friendly dan motivating
        3. Include waktu yang tersisa
        4. Saran persiapan jika perlu
        
        Gunakan bahasa Indonesia yang casual.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"⏰ Reminder: {event.get('summary', 'Acara Anda')} akan segera dimulai!"
    
    def suggest_schedule_optimization(self, events: List[Dict]) -> str:
        """
        Analyze schedule and suggest optimizations
        """
        events_summary = []
        for event in events:
            events_summary.append({
                'title': event.get('summary', ''),
                'start': event.get('start', {}).get('dateTime', ''),
                'end': event.get('end', {}).get('dateTime', '')
            })
        
        prompt = f"""
        Analisis jadwal berikut dan berikan saran optimasi:
        
        {json.dumps(events_summary, indent=2)}
        
        Berikan saran untuk:
        1. Efisiensi waktu
        2. Work-life balance
        3. Waktu istirahat yang cukup
        4. Prioritas kegiatan
        5. Potensi konflik jadwal
        
        Gunakan bahasa Indonesia yang friendly dan actionable.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return "Tidak dapat menganalisis jadwal saat ini."
    
    def clear_chat_history(self, user_id: str):
        """Clear chat history for a specific user"""
        if user_id in self.chat_histories:
            self.chat_histories[user_id] = []
            return True
        return False