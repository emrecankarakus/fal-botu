import config
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Handlers klasöründeki modüllerden gerekli fonksiyonları ve handler'ları içe aktar
from handlers.general_handlers import start, help_command, error_handler, unknown_command
from handlers.fortune_handlers import gunun_fali, coffee_conv_handler # YENİ: coffee_conv_handler eklendi

def main() -> None:
    """
    Ana bot fonksiyonu. Botu başlatır ve komutları dinler.
    """
    # Bot'un Application nesnesini oluştur
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()
    
    # --- Komutları ve Handler'ları Bot'a Tanıt ---

    # 1. Genel komutlar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # 2. Günlük fal komutu
    application.add_handler(CommandHandler("gununfali", gunun_fali))

    # 3. YENİ: Kahve falı sohbet handler'ı
    # Bu, tek bir komut değil, bütün bir sohbet akışını yönetir.
    application.add_handler(coffee_conv_handler)
    
    # 4. Bilinmeyen komut/metin handler'ı (diğerlerinden sonra gelmeli)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_command))
    
    # 5. Hata yakalayıcı (her zaman en sona eklenmeli)
    application.add_error_handler(error_handler)

    # Bot'u çalıştırmaya başla
    logger = config.get_logger(__name__)
    logger.info("Bot çalışıyor... Durdurmak için CTRL+C")
    application.run_polling()

if __name__ == "__main__":
    main()

