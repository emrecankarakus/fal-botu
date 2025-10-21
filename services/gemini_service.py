import google.generativeai as genai
from PIL import Image
import io
import config

# Gemini API yapılandırması
logger = config.get_logger(__name__)
try:
    genai.configure(api_key=config.GEMINI_API_KEY)
    # Hem metin hem de görüntü için aynı, modern modeli kullanıyoruz.
    multimodal_model = genai.GenerativeModel(config.GEMINI_MODEL_NAME) 
    logger.info(f"Gemini servisi, '{config.GEMINI_MODEL_NAME}' modeli ile başarıyla başlatıldı.")
except Exception as e:
    logger.critical(f"GEMINI_API_KEY ortam değişkeni bulunamadı veya geçersiz! Hata: {e}")
    multimodal_model = None

async def get_gemini_response(prompt: str) -> str:
    """Metin istemine Gemini ile yanıt üretir."""
    if not multimodal_model:
        return "HATA: Gemini modeli yapılandırılamadı."
    try:
        response = await multimodal_model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Gemini metin yanıtı alınırken hata oluştu: {e}")
        return "Üzgünüm, şu an yıldızlarla bağlantı kuramıyorum."

async def get_coffee_fortune(image_bytes_list: list) -> str:
    """Verilen 3 fotoğrafı (byte listesi) kullanarak fal yorumu üretir."""
    if not multimodal_model:
        return "HATA: Gemini modeli yapılandırılamadı."
    try:
        images = [Image.open(io.BytesIO(img_bytes)) for img_bytes in image_bytes_list]
        prompt_parts = [
            "Sen usta bir kahve falcısısın. Sana gönderilen 3 farklı fincan fotoğrafını dikkatlice incele. Fincandaki sembolleri, yolları, figürleri birleştirerek anlamlı bir bütün oluştur. Kullanıcının AŞK, İŞ/PARA ve SAĞLIK/HANE durumu hakkında detaylı, uzun ve gizemli bir dille kahve falı yorumu yap. Yorumun en az 150 kelime olsun.",
        ]
        prompt_parts.extend(images)
        response = await multimodal_model.generate_content_async(prompt_parts)
        return response.text
    except Exception as e:
        logger.error(f"Gemini kahve falı yorumu alınırken hata oluştu: {e}")
        return "Üzgünüm, fincanındaki sembolleri şu an için okuyamıyorum. Lütfen daha sonra tekrar dene."

async def validate_coffee_cup_image(image_bytes: bytes) -> bool:
    """Verilen fotoğrafın bir kahve fincanı olup olmadığını doğrular."""
    if not multimodal_model:
        logger.error("HATA: Gemini modeli yapılandırılamadı.")
        return False
    try:
        image = Image.open(io.BytesIO(image_bytes))
        prompt = [
            "Bu fotoğrafta kahve falı için kullanılabilecek, içinde telve olan bir kahve fincanı veya tabağı var mı? Sadece 'EVET' veya 'HAYIR' diye cevap ver.",
            image,
        ]
        response = await multimodal_model.generate_content_async(prompt)
        return "EVET" in response.text.upper().strip()
    except Exception as e:
        logger.error(f"Gemini görüntü doğrulaması yapılırken hata oluştu: {e}")
        return False

