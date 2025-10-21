from supabase import create_client, Client
import config
import uuid

# Supabase istemcisini (client) .env dosyasındaki bilgilerle başlat
try:
    url: str = config.SUPABASE_URL
    key: str = config.SUPABASE_KEY
    supabase: Client = create_client(url, key)
    logger = config.get_logger(__name__)
    logger.info("Supabase servisi başarıyla başlatıldı.")
except Exception as e:
    logger = config.get_logger(__name__)
    logger.critical(f"Supabase başlatılırken ciddi bir hata oluştu: {e}")
    logger.critical("Lütfen .env dosyasındaki SUPABASE_URL ve SUPABASE_KEY bilgilerini kontrol edin.")
    supabase = None

async def upload_image(image_bytes: bytearray, user_id: int) -> str | None:
    """
    Verilen bir resmi (bytearray olarak) Supabase Storage'a yükler ve URL'sini döndürür.
    """
    if not supabase:
        return None
    try:
        # Her resim için benzersiz bir dosya yolu oluşturuyoruz.
        file_path = f"{user_id}/{uuid.uuid4()}.jpg"
        
        # --- DÜZELTME BURADA ---
        # Supabase kütüphanesi 'bytearray' yerine 'bytes' beklediği için
        # veriyi doğru tipe dönüştürüyoruz.
        image_data_as_bytes = bytes(image_bytes)
        
        # Resmi 'fincan-resimleri' kovasına yüklüyoruz.
        supabase.storage.from_("fincan-resimleri").upload(
            file=image_data_as_bytes,
            path=file_path,
            file_options={"content-type": "image/jpeg"}
        )
        
        # Yüklenen resmin kalıcı ve herkese açık URL'sini alıyoruz.
        res = supabase.storage.from_("fincan-resimleri").get_public_url(file_path)
        
        logger.info(f"Resim başarıyla Supabase'e yüklendi: {res}")
        return res
        
    except Exception as e:
        logger.error(f"Supabase'e resim yüklenirken hata oluştu: {e}")
        return None

async def save_fortune_to_db(user_id: int, fortune_text: str, image_urls: list) -> bool:
    """
    Fal yorumunu ve ilgili resim URL'lerini Supabase veritabanına kaydeder.
    """
    if not supabase:
        return False
    try:
        data_to_insert = {
            'user_id': user_id,
            'fortune_text': fortune_text,
            'image_urls': image_urls
        }
        
        supabase.table('fortunes').insert(data_to_insert).execute()
        
        logger.info(f"{user_id} kullanıcısı için fal başarıyla veritabanına kaydedildi.")
        return True
        
    except Exception as e:
        logger.error(f"Supabase'e fal kaydedilirken hata oluştu: {e}")
        return False

