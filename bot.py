import logging
import json
import sys
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from mcstatus import JavaServer

# --- Dosya İsimleri ---
CONFIG_FILE = "config.json"
MESSAGES_FILE = "messages.json"
DATA_FILE = "bot_data.json"

# --- Loglama Kurulumu ---
logging.basicConfig(
    format="%(asctime)s - BOT - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram.ext").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# --- Yükleyici Fonksiyonlar ---
def load_json_file(filename, template):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logger.warning(f"{filename} bulunamadı veya hatalı. Şablon oluşturuluyor.")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=4)
        if filename == CONFIG_FILE:
            logger.critical(f"{filename} oluşturuldu. Lütfen içini doldurup botu yeniden başlatın.")
            sys.exit(1)
        return template

# --- Ayarları ve Mesajları Yükle ---
config_template = {
    "TELEGRAM_TOKEN": "BURAYA_TOKENINIZI_GIRIN", "MINECRAFT_SERVER_IP": "sunucu.ip",
    "TARGET_CHAT_ID": 0, "SERVER_NAME": "Sunucum"
}
messages_template = {
    "status_online_header": "🌟 {server_name} 🌟", "status_offline_header": "🚫 SUNUCU ÇEVRİMDIŞI 🚫",
    "status_online_players": "👥 <b>Online Oyuncular:</b> {online}/{max}", "status_daily_record": "📈 <b>Günlük Rekor:</b> {daily_max}",
    "status_all_time_record": "🏆 <b>Tüm Zamanlar Rekoru:</b> {all_time_max}", "status_last_update": "🔄 <b>Son Güncelleme:</b> {update_time}",
    "status_last_check": "🔄 <b>Son Kontrol:</b> {update_time}", "status_offline_message": "Sunucu kapalı veya şu anda yanıt vermiyor.",
    "status_checking": "Sunucu durumu kontrol ediliyor...", "log_shutdown_title": "🗓️ Son 5 Sunucu Kapanma Zamanı",
    "log_startup_title": "🕒 Son 5 Sunucu Başlama Zamanı", "log_no_records": "Kayıt bulunmuyor.",
    "notification_server_up": "✅ Sunucu tekrar aktif!", "notification_server_down": "🚨 Sunucu kapandı veya ulaşılamıyor!",
    "command_start_greet": "Merhaba!", "command_start_desc": "Bu bot, Minecraft sunucu durumunu belirtilen grupta otomatik olarak takip eder.",
    "command_start_help": "<b>/durum</b> - Takip mesajlarını manuel olarak yeniden başlatır/günceller.\n<b>/durdur</b> - Takibi durdurur ve gönderilen mesajları silmeye çalışır.",
    "command_status_reply": "İzleme mesajları manuel olarak silinip yeniden oluşturuluyor...",
    "command_stop_reply_success": "Sunucu izleme durduruldu.", "command_stop_reply_fail": "Aktif bir izleme görevi bulunmuyor."
}

config = load_json_file(CONFIG_FILE, config_template)
MESSAGES = load_json_file(MESSAGES_FILE, messages_template)

TELEGRAM_TOKEN = config["TELEGRAM_TOKEN"]
MINECRAFT_SERVER_IP = config["MINECRAFT_SERVER_IP"]
TARGET_CHAT_ID = config["TARGET_CHAT_ID"]
SERVER_NAME = config["SERVER_NAME"]

# --- Veri Saklama Fonksiyonları ---
def load_data():
    try:
        with open(DATA_FILE, "r") as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): return {}
def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

# --- Bot Komutları ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    logger.info(f"Kullanıcı {user.username} ({user.id}) /start komutunu kullandı.")
    await update.message.reply_html(
        f"{MESSAGES['command_start_greet']}\n\n"
        f"{MESSAGES['command_start_desc']}\n"
        f"{MESSAGES['command_start_help']}"
    )

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    logger.info(f"Bir kullanıcı {chat_id} ID'li sohbette /idogren komutunu kullandı.")
    # HATA DÜZELTMESİ: Sondaki nokta karakteri escape edildi.
    await update.message.reply_text(
        f"Bu sohbetin ID'si: `{chat_id}`\n\n"
        f"Bu ID'yi kopyalayıp `config\\.json` dosyasındaki `TARGET_CHAT_ID` alanına yapıştırın\\.",
        parse_mode='MarkdownV2'
    )


# --- Yardımcı Fonksiyonlar ---
async def delete_message_callback(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    try:
        await context.bot.delete_message(chat_id=job.data['chat_id'], message_id=job.data['message_id'])
        logger.info(f"Geçici bildirim mesajı ({job.data['message_id']}) silindi.")
    except Exception as e:
        logger.warning(f"Geçici mesaj silinemedi: {e}")

def format_log_message(title_key, times_list):
    message = f"<b>{MESSAGES[title_key]}</b>\n\n"
    if not times_list:
        message += MESSAGES['log_no_records']
    else:
        for i, time_str in enumerate(times_list, 1):
            message += f"{i}. {time_str}\n"
    return message

# --- Ana Fonksiyonlar ---
async def check_server_status(context: ContextTypes.DEFAULT_TYPE) -> None:
    bot_data = context.application.bot_data
    if 'status_msg_id' not in bot_data: return
    previous_state = bot_data.get('server_state', 'unknown')
    update_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    try:
        server = JavaServer.lookup(MINECRAFT_SERVER_IP)
        status = await server.async_status()
        online_players = status.players.online
        max_players = status.players.max
        data_updated = False
        today_str = datetime.now().strftime("%Y-%m-%d")

        all_time_max = bot_data.get('all_time_max_players', 0)
        if online_players > all_time_max:
            bot_data['all_time_max_players'] = online_players
            all_time_max = online_players
            data_updated = True
            logger.info(f"Yeni tüm zamanlar rekoru: {all_time_max}")

        daily_max_date = bot_data.get('daily_max_date', '')
        daily_max = bot_data.get('daily_max_players', 0)
        if daily_max_date != today_str:
            bot_data['daily_max_date'] = today_str
            bot_data['daily_max_players'] = online_players
            daily_max = online_players
            data_updated = True
            logger.info(f"Yeni gün ({today_str}), günlük rekor sıfırlandı: {daily_max}")
        elif online_players > daily_max:
            bot_data['daily_max_players'] = online_players
            daily_max = online_players
            data_updated = True
            logger.info(f"Yeni günlük rekor: {daily_max}")
        
        if data_updated:
            save_data(bot_data)

        new_status_text = (
            f"<b>{MESSAGES['status_online_header'].format(server_name=SERVER_NAME)}</b>\n\n"
            f"{MESSAGES['status_online_players'].format(online=online_players, max=max_players)}\n"
            f"{MESSAGES['status_daily_record'].format(daily_max=daily_max)}\n"
            f"{MESSAGES['status_all_time_record'].format(all_time_max=all_time_max)}\n\n"
            f"{MESSAGES['status_last_update'].format(update_time=update_time)}"
        )
        current_state = "online"
    except Exception:
        all_time_max = bot_data.get('all_time_max_players', 0)
        daily_max = bot_data.get('daily_max_players', 0)
        new_status_text = (
            f"<b>{MESSAGES['status_offline_header']}</b>\n\n"
            f"{MESSAGES['status_offline_message']}\n\n"
            f"{MESSAGES['status_daily_record'].format(daily_max=daily_max)}\n"
            f"{MESSAGES['status_all_time_record'].format(all_time_max=all_time_max)}\n\n"
            f"{MESSAGES['status_last_check'].format(update_time=update_time)}"
        )
        current_state = "offline"

    now_str_log = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if current_state != previous_state:
        if current_state == 'online':
            if 'shutdown_notification_msg_id' in bot_data:
                try:
                    await context.bot.delete_message(chat_id=TARGET_CHAT_ID, message_id=bot_data['shutdown_notification_msg_id'])
                    logger.info(f"Eski 'sunucu kapalı' bildirimi silindi.")
                except Exception as e:
                    logger.warning(f"'Sunucu kapalı' bildirimi silinemedi: {e}")
                del bot_data['shutdown_notification_msg_id']

            sent_msg = await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=MESSAGES['notification_server_up'])
            context.job_queue.run_once(delete_message_callback, 30, data={'chat_id': TARGET_CHAT_ID, 'message_id': sent_msg.message_id})

            start_times = bot_data.get('startup_times', [])
            start_times.insert(0, now_str_log)
            bot_data['startup_times'] = start_times[:5]
            await context.bot.edit_message_text(format_log_message("log_startup_title", bot_data['startup_times']), chat_id=TARGET_CHAT_ID, message_id=bot_data['startup_log_msg_id'], parse_mode='HTML')
            logger.info("Sunucu tekrar aktif, bildirim gönderildi ve başlangıç logu güncellendi.")
        elif current_state == 'offline':
            sent_shutdown_msg = await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=MESSAGES['notification_server_down'])
            bot_data['shutdown_notification_msg_id'] = sent_shutdown_msg.message_id

            shut_times = bot_data.get('shutdown_times', [])
            shut_times.insert(0, now_str_log)
            bot_data['shutdown_times'] = shut_times[:5]
            await context.bot.edit_message_text(format_log_message("log_shutdown_title", bot_data['shutdown_times']), chat_id=TARGET_CHAT_ID, message_id=bot_data['shutdown_log_msg_id'], parse_mode='HTML')
            logger.info("Sunucu kapandı, bildirim gönderildi ve kapanma logu güncellendi.")

        bot_data['server_state'] = current_state
        save_data(bot_data)

    if bot_data.get('last_status_text') != new_status_text:
        try:
            await context.bot.edit_message_text(new_status_text, chat_id=TARGET_CHAT_ID, message_id=bot_data['status_msg_id'], parse_mode='HTML')
            bot_data['last_status_text'] = new_status_text
        except Exception as e:
            logger.error(f"Durum mesajı güncellenemedi: {e}")

async def start_monitoring_routine(context: ContextTypes.DEFAULT_TYPE) -> None:
    bot_data = context.application.bot_data
    logger.info("Otomatik izleme rutini kontrol ediliyor...")

    messages_ok = False
    if 'status_msg_id' in bot_data:
        try:
            await context.bot.edit_message_text(MESSAGES['status_checking'], chat_id=TARGET_CHAT_ID, message_id=bot_data['status_msg_id'])
            logger.info("Mevcut takip mesajları doğrulandı.")
            messages_ok = True
        except Exception as e:
            logger.warning(f"Mevcut takip mesajları doğrulanamadı (muhtemelen silinmişler): {e}")
            messages_ok = False
    
    if not messages_ok:
        logger.info("Takip mesajları oluşturuluyor...")
        for key in ['shutdown_log_msg_id', 'startup_log_msg_id', 'status_msg_id']:
            if key in bot_data: del bot_data[key]
        
        try:
            msg = await context.bot.send_message(TARGET_CHAT_ID, format_log_message("log_shutdown_title", bot_data.get('shutdown_times', [])), parse_mode='HTML')
            bot_data['shutdown_log_msg_id'] = msg.message_id
        except Exception as e: logger.error(f"Kapanma log mesajı gönderilemedi: {e}")

        try:
            msg = await context.bot.send_message(TARGET_CHAT_ID, format_log_message("log_startup_title", bot_data.get('startup_times', [])), parse_mode='HTML')
            bot_data['startup_log_msg_id'] = msg.message_id
        except Exception as e: logger.error(f"Başlama log mesajı gönderilemedi: {e}")

        try:
            msg = await context.bot.send_message(TARGET_CHAT_ID, MESSAGES['status_checking'], parse_mode='HTML')
            bot_data['status_msg_id'] = msg.message_id
        except Exception as e: logger.error(f"Durum mesajı gönderilemedi: {e}")
    
    save_data(bot_data)
    remove_job_if_exists(str(TARGET_CHAT_ID), context)
    context.job_queue.run_repeating(check_server_status, interval=20, first=1, name=str(TARGET_CHAT_ID))
    logger.info(f"Sunucu izleme görevi {TARGET_CHAT_ID} için başlatıldı/yenilendi.")

async def manual_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot_data = context.application.bot_data
    await update.message.reply_text(MESSAGES['command_status_reply'])
    
    for key in ['shutdown_log_msg_id', 'startup_log_msg_id', 'status_msg_id']:
        if key in bot_data:
            try: await context.bot.delete_message(chat_id=TARGET_CHAT_ID, message_id=bot_data[key])
            except Exception: pass
            del bot_data[key]
    
    await start_monitoring_routine(context)

def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs: return False
    for job in current_jobs: job.schedule_removal()
    return True

async def stop_monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    job_removed = remove_job_if_exists(str(TARGET_CHAT_ID), context)
    text = MESSAGES['command_stop_reply_success'] if job_removed else MESSAGES['command_stop_reply_fail']

    if job_removed:
        bot_data = context.application.bot_data
        for key in ['shutdown_log_msg_id', 'startup_log_msg_id', 'status_msg_id', 'shutdown_notification_msg_id']:
            if key in bot_data:
                try: await context.bot.delete_message(chat_id=TARGET_CHAT_ID, message_id=bot_data[key])
                except Exception: pass
        save_data({})
        context.application.bot_data.clear()
        logger.info("İzleme durduruldu ve tüm veriler temizlendi.")
    await update.message.reply_text(text)

def main() -> None:
    loaded_data = load_data()
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.bot_data.update(loaded_data)
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("durum", manual_start_command))
    application.add_handler(CommandHandler("durdur", stop_monitoring))
    application.add_handler(CommandHandler("idogren", get_chat_id))
    
    application.job_queue.run_once(start_monitoring_routine, 5)
    
    logger.info("Bot başlatılıyor...")
    application.run_polling()

if __name__ == "__main__":
    main()

