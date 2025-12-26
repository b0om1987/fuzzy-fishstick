from telethon import TelegramClient, events
import os

client = TelegramClient(
    'Edge Sesh', os.getenv('API_ID'), os.getenv('API_HASH'),
    system_version = os.getenv('SYSTEM_VERSION'),
    device_model = os.getenv('DEVICE_MODEL'),
    app_version = os.getenv('APP_VERSION'),
    local_addr = [f'0.0.0.0:{os.getenv('PORT')}']).start(bot_token=os.getenv('TOKEN'))

@client.on(events.NewMessage)
async def my_event_handler(event):
    if 'hello' in event.raw_text:
        await event.reply('hi!')

client.start()
client.run_until_disconnected()
