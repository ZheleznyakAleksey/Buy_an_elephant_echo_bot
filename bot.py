import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
from log import start_logging, log_message


async def echo_elephant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.effective_chat.id
        username = update.effective_user.username
        message_text = update.message.text

        if chat_id == ADMIN_ID:
            await context.bot.send_message(CHAT_ID, message_text)
            await log_message('User(admin)', ADMIN_ID, message_text)
            await log_message('Admin', CHAT_ID, message_text)

        else:
            text_bot_message = f'Все говорят "{message_text}", а ты возьми и купи слоника'
            await log_message('User', chat_id, message_text)
            await log_message('Bot', chat_id, text_bot_message)
            await log_message(f'User {chat_id, username}', ADMIN_ID, message_text)
            await update.message.reply_text(text_bot_message)
            await context.bot.send_message(ADMIN_ID, f'Новое сообщение от {chat_id, username}: {message_text}')

    except Exception as e:
        print(f"Ошибка: {e}")


def load_config():
    load_dotenv()
    return (
        os.getenv('TOKEN'),
        int(os.getenv('ADMIN_ID')),
        int(os.getenv('CHAT_ID'))
    )


def main():
    global TOKEN, ADMIN_ID, CHAT_ID
    TOKEN, ADMIN_ID, CHAT_ID = load_config()
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, echo_elephant))
    app.run_polling()


if __name__ == '__main__':
    start_logging()
    main()