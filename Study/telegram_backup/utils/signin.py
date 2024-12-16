from telethon import TelegramClient
from configuration import config_extractor

# Use your own values from my.telegram.org

api_id, api_hash = config_extractor.fetchIDandHash()

# The first parameter is the .session file name (absolute paths allowed)
with TelegramClient('saarang', api_id, api_hash) as client:
    # client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))
    pass