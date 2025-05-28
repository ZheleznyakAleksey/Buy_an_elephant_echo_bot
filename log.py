import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime, time


logger = logging.getLogger()
logger.setLevel(logging.WARNING)


def start_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    handler = TimedRotatingFileHandler(
    filename='logs/log',
    when='H',
    interval=1,
    atTime=time(1, 0),
    backupCount=5,
    encoding='utf-8'
    )
    handler.suffix = '%Y-%m-%d.log'
    handler.setLevel(logging.WARNING)

    formatter = logging.Formatter('%(asctime)s — %(levelname)s — %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)


async def log_message(sender: str, user_id: int, message_type: str = None, message: str = None,
                      image: str = None, caption: str = None, voice: str = None):
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    
    log_entry = f'{formatted_time} | {sender} | {message_type} | '
    if message_type == 'IMAGE':
        log_entry += f'{image} | {caption}'
    elif message_type == 'VOICE':
        log_entry += voice
    else:
        log_entry += message


    log_folder = 'message_history'
    os.makedirs(log_folder, exist_ok=True)

    log_file_path = os.path.join(log_folder, f'chat_{user_id}_log.txt')
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(log_entry + '\n')