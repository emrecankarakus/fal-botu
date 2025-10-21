Telegram Fal Botu

Bu proje, Gemini API kullanarak kişiselleştirilmiş fal yorumları sunan bir Telegram botudur.

Proje Yapısı

Kodun daha sade, okunabilir ve yönetilebilir olması için proje birkaç modüle ayrılmıştır:

fal_botu/
├── handlers/
│   ├── general_handlers.py  # /start, /help gibi genel komutlar
│   └── fortune_handlers.py  # /gununfali gibi fal komutları
├── services/
│   └── gemini_service.py    # Gemini API ile iletişimi yöneten servis
├── config.py                # Tüm ayarlar, API anahtarları ve metinler
└── main.py                  # Botu başlatan ana dosya


main.py: Botun ana giriş noktasıdır. Sadece botu başlatır ve komutları ilgili handler'lara yönlendirir.

config.py: Tüm konfigürasyonları (API anahtarları, model adı, sabit metinler) içerir. Ayarları değiştirmek için sadece bu dosyayı düzenlemeniz yeterlidir.

services/: Dış servislerle (Gemini API gibi) olan tüm iletişimi yönetir. Botun "beyni" buradadır.

handlers/: Telegram'dan gelen komutları (/start, /gununfali vb.) işleyen fonksiyonları içerir.

Kurulum ve Çalıştırma

Gerekli Kütüphaneleri Yükleyin:

pip install python-telegram-bot google-generativeai


Ortam Değişkenlerini Ayarlayın:
Botun çalışması için API anahtarlarınızı terminal üzerinden "ortam değişkeni" olarak ayarlamanız gerekmektedir. Bu, anahtarlarınızı güvende tutar.

Linux veya macOS için:

export TELEGRAM_TOKEN="SENIN_TELEGRAM_TOKENIN"
export GEMINI_API_KEY="SENIN_GEMINI_API_KEYIN"


Windows (CMD) için:

set TELEGRAM_TOKEN="SENIN_TELEGRAM_TOKENIN"
set GEMINI_API_KEY="SENIN_GEMINI_API_KEYIN"


Botu Çalıştırın:
Yukarıdaki komutları girdikten sonra, aynı terminal penceresinden ana dosyayı çalıştırın:

python main.py


Botunuz artık çalışıyor olacak.