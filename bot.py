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
        message_from_admin = 'Админ отправил тебе сообщение:'

        if chat_id == ADMIN_ID:
            await context.bot.send_message(chat_id=CHAT_ID, text=message_from_admin)
            await context.bot.send_message(chat_id=CHAT_ID, text=message_text)
            await update.message.reply_text(text='Сообщение отправлено')
            await log_message(sender='User(admin)', message_type='TEXT', user_id=ADMIN_ID, message=message_text)
            await log_message(sender='Admin', user_id=CHAT_ID, message_type='TEXT', message=message_text)
        else:
            text_bot_message = f'Все говорят "{message_text}", а ты возьми и купи слоника'
            await update.message.reply_text(text=text_bot_message)
            await context.bot.send_message(chat_id=ADMIN_ID, text=f'{chat_id, username} отправил сообщение:')
            await context.bot.send_message(chat_id=ADMIN_ID, text=message_text)
            await log_message(sender='User', user_id=chat_id, message_type='TEXT', message=message_text)
            await log_message(sender=f'User {chat_id, username}', user_id=ADMIN_ID, message_type='TEXT', message=message_text)

    except Exception as e:
        print(f"Ошибка: {e}")


async def echo_elephant_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.effective_chat.id
        username = update.effective_user.username
        photo = update.message.photo[-1]
        message_caption = update.message.caption
        message_to_admin = f'{chat_id, username} отправил фото:'
        message_from_admin = f'Админ отправил тебе фото:'


        if chat_id == ADMIN_ID:
            await context.bot.send_message(chat_id=CHAT_ID, text=message_from_admin)
            await context.bot.send_photo(chat_id=CHAT_ID,
                                        photo=photo.file_id, 
                                        caption=message_caption)
            await update.message.reply_text(text='Фото отправлено')
            await log_message(sender='User(admin)', user_id=ADMIN_ID, message_type='IMAGE', image=photo.file_id, caption=message_caption)
            await log_message(sender='Admin', user_id=CHAT_ID, message_type='IMAGE', image=photo.file_id, caption=message_caption)

        else:
            text_bot_message1 = 'Все говорят'
            text_bot_message2 = 'А ты возьми и купи слоника'
            await context.bot.send_message(chat_id=ADMIN_ID, text=message_to_admin)
            await context.bot.send_photo(chat_id=ADMIN_ID,
                                        photo=photo.file_id, 
                                        caption=message_caption) 
            await update.message.reply_text(text=text_bot_message1)
            await update.message.reply_photo(photo=photo.file_id, 
                                             caption=message_caption)
            await update.message.reply_text(text=text_bot_message2)
            await log_message(sender=f'User', user_id=chat_id, message_type='IMAGE', image=photo.file_id, caption=message_caption)
            await log_message(sender=f'User {chat_id, username}', user_id=ADMIN_ID, message_type='IMAGE', image=photo.file_id, caption=message_caption)


    except Exception as e:
        print(f"Ошибка: {e}")


async def echo_elephant_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.effective_chat.id
        username = update.effective_user.username
        voice = update.message.voice
        message_to_admin = f'{chat_id, username} отправил аудио:'
        message_from_admin = f'Админ отправил тебе аудио:'


        if chat_id == ADMIN_ID:
            await context.bot.send_message(chat_id=CHAT_ID, text=message_from_admin)
            await context.bot.send_voice(chat_id=CHAT_ID, voice=voice)
            await log_message(sender='User(admin)', user_id=ADMIN_ID, message_type='VOICE', voice=voice.file_id)
            await log_message(sender='Admin', user_id=CHAT_ID, message_type='VOICE', voice=voice.file_id)

        else:
            text_bot_message1 = 'Все говорят'
            text_bot_message2 = 'А ты возьми и купи слоника'
            await context.bot.send_message(chat_id=ADMIN_ID, text=message_to_admin)
            await context.bot.send_voice(chat_id=ADMIN_ID, voice=voice)
            await update.message.reply_text(text=text_bot_message1)
            await update.message.reply_voice(voice=voice)
            await update.message.reply_text(text=text_bot_message2)
            await log_message(sender=f'User', user_id=chat_id, message_type='VOICE', voice=voice.file_id)
            await log_message(sender=f'User {chat_id, username}', user_id=ADMIN_ID, message_type='VOICE', voice=voice.file_id)

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
    app.add_handler(MessageHandler(filters.PHOTO, echo_elephant_image))
    app.add_handler(MessageHandler(filters.VOICE, echo_elephant_audio))
    app.run_polling()


if __name__ == '__main__':
    start_logging()
    main()