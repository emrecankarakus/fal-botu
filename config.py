from dotenv import load_dotenv
import os
import logging

# .env dosyasındaki tüm değişkenleri yükle
load_dotenv()

# --- GİZLİ BİLGİLER ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- YENİ: SUPABASE AYARLARI ---
# Bu satırlar, .env dosyasındaki Supabase bilgilerini okur.
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# --- MODEL AYARLARI ---
GEMINI_MODEL_NAME = 'gemini-2.5-flash'

# --- LOGLAMA AYARLARI ---
def get_logger(name):
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    return logging.getLogger(name)

# --- BOT MESAJLARI ---
START_MESSAGE = "Merhaba {user_mention}! Ben senin fal botunum. 🤖\n\nKullanılabilir komutlar için /help yazabilirsin."

HELP_MESSAGE = """
🔮 *İşte kullanabileceğin komutlar:*

`/gununfali <burç> <cinsiyet>`
_Örnek: /gununfali yengeç kadın_
Günlük kişisel burç yorumunu alırsın\.

`/kahvefali`
Fincanının 3 farklı açıdan fotoğrafını göndererek sana özel kahve falı yorumu alabilirsin\.

`/iptal`
Devam eden bir kahve falı işlemini iptal eder\.
"""

GUNUN_FALI_USAGE_ERROR = "Lütfen komutu doğru formatta kullan: `/gununfali <burç> <cinsiyet>`\n\n*Örnek: /gununfali aslan erkek*"

# --- KAHVE FALI MESAJLARI ---
COFFEE_FORTUNE_START = "Harika! Kahve falı için fincanının **3 farklı açıdan** fotoğrafını göndermeye başlayabilirsin. (0/3)"
COFFEE_FORTUNE_PROGRESS = "{count}/3 fotoğraf tamamlandı. Lütfen sıradaki fotoğrafı gönder."
COFFEE_FORTUNE_COMPLETE = "✅ 3/3 fotoğraf tamamlandı! Fincanını inceliyorum, sembolleri bir araya getiriyorum... Bu işlem biraz zaman alabilir, lütfen bekle."
COFFEE_FORTUNE_CANCEL = "Kahve falı isteğin iptal edildi."
COFFEE_FORTUNE_INVALID_STATE = "Lütfen sadece fotoğraf göndererek devam et veya işlemi `/iptal` komutuyla sonlandır."
COFFEE_FORTUNE_TIMEOUT = "Uzun süre fotoğraf göndermediğin için kahve falı isteğin zaman aşımına uğradı ve iptal edildi."

# --- FOTOĞRAF KONTROLÜ İÇİN MESAJLAR ---
COFFEE_VALIDATION_MESSAGE = "✔️ Fotoğraf alındı, fincan olup olmadığını kontrol ediyorum..."
COFFEE_INVALID_PHOTO_ERROR = "❌ Üzgünüm, bu bir kahve fincanı fotoğrafına benzemiyor. Lütfen fincanının net bir fotoğrafını gönder."

