import logging
import os
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# === Логирование ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === Список ID тем, в которых бот удаляет сообщения от не-админов ===
BLOCKED_THREAD_IDS = [
    14,  # замените на реальные ID тем
    9876543210
]

# === Приветствие новых участников ===
def welcome(update: Update, context: CallbackContext):
    for member in update.message.new_chat_members:
        update.message.reply_text(
            f"👋 Добро пожаловать, {member.full_name}!\n\n"
            "📜 Правила чата:\n"
            "1. Не спамить\n"
            "2. Уважать участников\n"
            "3. Соблюдать тему общения\n"
        )

# === Блокировка сообщений в выбранных темах ===
def block_topics(update: Update, context: CallbackContext):
    msg = update.message
    if not msg:
        return

    thread_id = getattr(msg, "message_thread_id", None)
    if not thread_id:
        return  # это обычное сообщение, не тема форума

    user_id = update.effective_user.id
    admins = [admin.user.id for admin in context.bot.get_chat_administrators(update.effective_chat.id)]

    if user_id not in admins and thread_id in BLOCKED_THREAD_IDS:
        try:
            msg.delete()
            logger.info(f"Сообщение удалено от пользователя {user_id} в теме {thread_id}.")
        except Exception as e:
            logger.error(f"Ошибка при удалении сообщения: {e}")

# === Временный хэндлер для отладки ID темы ===
def debug_thread_id(update: Update, context: CallbackContext):
    msg = update.message
    if not msg:
        return

    thread_id = getattr(msg, "message_thread_id", None)
    if thread_id:
        msg.reply_text(f"ID этой темы: {thread_id}")
    else:
        msg.reply_text("Это не тема форума.")

# === Основной запуск бота ===
def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("❌ Переменная окружения TELEGRAM_TOKEN не установлена!")

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # Хэндлеры
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    dp.add_handler(MessageHandler(Filters.all, block_topics))

    # Временный хэндлер для получения ID темы
    dp.add_handler(MessageHandler(Filters.all, debug_thread_id))

    # Запуск
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
