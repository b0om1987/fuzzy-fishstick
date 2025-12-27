from telethon import TelegramClient, events
from flask import Flask
import os

app = Flask(__name__)
@app.route('/')
def hello_world():
  return 'Hello, World!'

client = TelegramClient(
    'Edge Sesh', os.getenv('API_ID'), os.getenv('API_HASH'),
    system_version = os.getenv('SYSTEM_VERSION'),
    device_model = os.getenv('DEVICE_MODEL'),
    app_version = os.getenv('APP_VERSION'),
    local_addr = ('0.0.0.0', os.getenv('PORT'))).start(bot_token=os.getenv('TOKEN'))

@client.on(events.NewMessage)
async def my_event_handler(event):
    if 'hello' in event.raw_text:
        await event.reply('hi!')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'), debug=False)
client.start()
client.run_until_disconnected()
