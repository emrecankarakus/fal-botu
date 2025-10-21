from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters
)
import config
from services import gemini_service, supabase_service # YENİ: supabase_service eklendi

# Sohbet durumları için sabit tanımlıyoruz.
AWAITING_PHOTOS = range(1)

async def start_coffee_fortune(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """/kahvefali komutu ile sohbeti başlatır ve fotoğraf bekler."""
    context.user_data['coffee_photos'] = []
    await update.message.reply_text(config.COFFEE_FORTUNE_START)
    return AWAITING_PHOTOS

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Gelen fotoğrafları doğrular, sayar, 3'e ulaştığında Supabase'e yükler,
    malı yorumlar ve sonucu veritabanına kaydeder.
    """
    user = update.effective_user
    photo_file = await update.message.photo[-1].get_file()
    photo_bytes = await photo_file.download_as_bytearray()

    await update.message.reply_text(config.COFFEE_VALIDATION_MESSAGE)
    is_valid_cup = await gemini_service.validate_coffee_cup_image(photo_bytes)

    if not is_valid_cup:
        await update.message.reply_text(config.COFFEE_INVALID_PHOTO_ERROR)
        return AWAITING_PHOTOS

    if 'coffee_photos' not in context.user_data:
        context.user_data['coffee_photos'] = []

    context.user_data['coffee_photos'].append(photo_bytes)
    photo_count = len(context.user_data['coffee_photos'])

    if photo_count < 3:
        await update.message.reply_text(config.COFFEE_FORTUNE_PROGRESS.format(count=photo_count))
        return AWAITING_PHOTOS
    else:
        # 3 fotoğraf tamamlandığında, kullanıcıya beklemesini söyle
        await update.message.reply_text(config.COFFEE_FORTUNE_COMPLETE)

        # --- YENİ ADIMLAR ---
        # 1. Fotoğrafları Supabase'e yükle ve URL'lerini topla
        image_urls = []
        for photo_byte_data in context.user_data['coffee_photos']:
            url = await supabase_service.upload_image(photo_byte_data, user.id)
            if url:
                image_urls.append(url)
        
        # Yükleme başarısız olursa kullanıcıyı bilgilendir
        if len(image_urls) != 3:
            await update.message.reply_text("Resimleri depolarken bir sorun oluştu, lütfen daha sonra tekrar dene.")
            del context.user_data['coffee_photos']
            return ConversationHandler.END

        # 2. Gemini'dan fal yorumunu al
        fortune_text = await gemini_service.get_coffee_fortune(context.user_data['coffee_photos'])

        # 3. Falı ve resim URL'lerini veritabanına kaydet
        await supabase_service.save_fortune_to_db(
            user_id=user.id,
            fortune_text=fortune_text,
            image_urls=image_urls
        )
        # --- YENİ ADIMLAR BİTTİ ---

        # Kullanıcıya fal sonucunu gönder
        await update.message.reply_text(fortune_text)

        # Geçici verileri temizle ve sohbeti sonlandır
        del context.user_data['coffee_photos']
        return ConversationHandler.END

async def invalid_photo_state(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Fotoğraf beklenirken metin gönderilirse kullanıcıyı uyarır."""
    await update.message.reply_text(config.COFFEE_FORTUNE_INVALID_STATE)
    return AWAITING_PHOTOS

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sohbeti iptal eder."""
    if 'coffee_photos' in context.user_data:
        del context.user_data['coffee_photos']
    await update.message.reply_text(config.COFFEE_FORTUNE_CANCEL)
    return ConversationHandler.END

async def timeout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sohbet zaman aşımına uğradığında çalışır."""
    if 'coffee_photos' in context.user_data:
        del context.user_data['coffee_photos']
    await context.bot.send_message(chat_id=update.effective_chat.id, text=config.COFFEE_FORTUNE_TIMEOUT)

async def gunun_fali(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Günlük burç yorumu yapar."""
    if len(context.args) != 2:
        await update.message.reply_markdown_v2(config.GUNUN_FALI_USAGE_ERROR)
        return
    burc, cinsiyet = context.args[0].lower(), context.args[1].lower()
    prompt = f"Sen çok yetenekli, gizemli ve bilge bir falcısın. Burcu '{burc}' olan '{cinsiyet}' bir kullanıcı için, bugüne özel detaylı bir fal yorumu yap. Yorumunda aşk, para ve sağlık konularına değin. Yaklaşık 70-90 kelime uzunluğunda olsun."
    await update.message.reply_text("🔮 Falın yıldızlarda aranıyor, lütfen bekle...")
    fortune_text = await gemini_service.get_gemini_response(prompt)
    await update.message.reply_text(fortune_text)


# Kahve falı sohbet handler'ı
coffee_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("kahvefali", start_coffee_fortune)],
    states={
        AWAITING_PHOTOS: [
            MessageHandler(filters.PHOTO, handle_photo),
            MessageHandler(filters.TEXT & ~filters.COMMAND, invalid_photo_state)
        ]
    },
    fallbacks=[CommandHandler("iptal", cancel)],
    conversation_timeout=600,
    per_user=True,
    per_chat=True
)

