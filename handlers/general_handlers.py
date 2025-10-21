import traceback
import html
import json
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
# config.py'den gerekli değişkenleri ve fonksiyonları alıyoruz.
# Eğer config dosyanızda bu değişkenler yoksa, eklemeniz gerekebilir.
import config 

logger = config.get_logger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start komutuna başlangıç mesajıyla yanıt verir."""
    
    # --- DÜZELTME BURADA ---
    # .mention_html() yerine kullanıcının sadece adını (.first_name) alıyoruz.
    user_mention = update.effective_user.first_name
    
    # Mesaj artık düz metin olduğu için parse_mode'a gerek kalmadı.
    # config.START_MESSAGE'ın "{user_mention}" içerdiğinden emin olun.
    await update.message.reply_text(
        config.START_MESSAGE.format(user_mention=user_mention)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/help komutuna yardım mesajıyla yanıt verir."""
    # parse_mode'u config dosyanızdaki metne göre ayarlayabilirsiniz.
    await update.message.reply_text(config.HELP_MESSAGE, parse_mode='MarkdownV2')

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tanınmayan komutlara veya metinlere yardım mesajıyla yanıt verir."""
    await update.message.reply_text(config.HELP_MESSAGE, parse_mode='MarkdownV2')

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tüm hataları yakalar ve terminale detaylı bir şekilde yazar."""
    logger.error("Bir güncelleme işlenirken istisna oluştu:", exc_info=context.error)
    
    # Hata detaylarını formatla
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Geliştiriciye gönderilecek mesajı hazırla (isteğe bağlı)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        "Botta bir hata oluştu:\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    
    # Geliştiriciye (sana) hata mesajı göndermek istersen burayı aktif edebilirsin.
    # developer_chat_id = 123456789 # Kendi Telegram ID'ni yaz
    # await context.bot.send_message(chat_id=developer_chat_id, text=message, parse_mode=ParseMode.HTML)

