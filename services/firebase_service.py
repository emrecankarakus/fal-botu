import firebase_admin
from firebase_admin import credentials, storage
import uuid  # Dosyalara benzersiz isimler vermek için
import config

# Firebase'i başlatmak için bir kerelik kurulum
try:
    # İndirdiğimiz anahtar dosyasının yolunu belirtiyoruz
    cred = credentials.Certificate("firebase_key.json")
    
    # Firebase projemizin Storage bucket URL'sini bulmamız gerekiyor.
    # Bu URL'yi Firebase konsolundaki Storage sayfasının "Files" sekmesinde bulabilirsin.
    # Genellikle `proje-id.appspot.com` şeklinde olur.
    # Lütfen aşağıdaki satırdaki URL'yi kendininkiyle değiştir.
    FIREBASE_BUCKET_URL = 'SENIN-PROJE-IDN.appspot.com' 
    
    firebase_admin.initialize_app(cred, {
        'storageBucket': FIREBASE_BUCKET_URL
    })
    logger = config.get_logger(__name__)
    logger.info("Firebase servisi başarıyla başlatıldı.")
except Exception as e:
    logger = config.get_logger(__name__)
    logger.critical(f"Firebase başlatılırken ciddi bir hata oluştu: {e}")
    logger.critical("Lütfen 'firebase_key.json' dosyasının doğru yerde olduğundan ve bucket URL'sinin doğru olduğundan emin olun.")


async def upload_image_to_storage(image_bytes: bytes, user_id: int) -> str:
    """
    Verilen bir resmi (byte olarak) Firebase Storage'a yükler ve URL'sini döndürür.
    """
    try:
        # Firebase Storage'daki ana depolama alanını (bucket) al
        bucket = storage.bucket()
        
        # Her resim için benzersiz bir dosya adı oluşturuyoruz.
        # Örnek: user_photos/12345678/abc-123-def-456.jpg
        unique_filename = f"user_photos/{user_id}/{uuid.uuid4()}.jpg"
        
        # Dosyayı yüklemek için bir "blob" (nesne) oluştur
        blob = bucket.blob(unique_filename)
        
        # Resmi byte olarak yükle
        # content_type, dosyanın bir resim olduğunu belirtir
        blob.upload_from_string(
            data=image_bytes,
            content_type='image/jpeg'
        )
        
        # Yüklenen resmin herkes tarafından görülebilir URL'sini oluştur ve döndür
        # Bu URL kalıcıdır ve veritabanına kaydedilebilir.
        blob.make_public()
        
        logger.info(f"Resim başarıyla Firebase Storage'a yüklendi: {blob.public_url}")
        return blob.public_url
        
    except Exception as e:
        logger.error(f"Firebase'e resim yüklenirken hata oluştu: {e}")
        return None
