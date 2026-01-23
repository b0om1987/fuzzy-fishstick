from telethon import TelegramClient, events
import os
import asyncio
import random
from random import randint, choice
from datetime import datetime, timedelta, timezone
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from telethon.tl.types import InputPhoto

global database

uri = f"mongodb+srv://autobot:{os.getenv('DB_ACCESS')}@clustermain.0qpaogm.mongodb.net/?appName=ClusterMain"
mongo_client = MongoClient(uri, server_api=ServerApi('1'))
db = mongo_client[os.getenv('DB_NAME')]
database = db[os.getenv('COLLECTION_NAME')]

global prefix
global adressing
global oskprefix
global oskmain
global postfix

TltFlood = -1003481332457
TestingChat = -5121472948
PMs = 1272926086
GreenFucker = -1002097505858

prefix = ['Блять', 'Сука', 'Ёб твою мать', 'Пиздец', 'Ёбаный свет блять',
          'Как меня это заебло уже', 'Да я мать твою ебал', 'Мудило гороховое',
          'Ой не щекочи мою залупу', 'Я ору с тебя', 'Мать моя женщина',
          'Ну сука, блять', 'Ой блять', 'Ой сука', 'Да ебучий случай',
          'Ебать мой рот наковальней блять', 'Ох пиздец', 'Да ты меня заебёшь']
adressing = ['ты,', 'да ты же', 'какое ты', 'ты нахуй', 'ты сука',
             'ты вообще не стесняешься даже что ты', 'ебало вальни,',
             'ебать ты', 'какое же ты', 'я дурею, какое ты']
oskprefix = ['прогнившее', 'тупое', 'уёбищное', 'ебанутое', 'безмозглое',
             'бесполезное', 'ебаное', 'блядское', 'дегенератское', 'позорное',
             'богатое', 'ёбнутое', 'тупорылое', 'безмамное', 'отвратительное',
             'пиздоблядское, охуевшее', 'ничтожное',
             'ебануто трахнутое божественными силами', 'хуёвое, обесцененное просто',
             'не нужное никому нахуй в мире', 'припизднутое', 'бредящее', 'ублюдошное',
             'залупососное', 'гомеопатическое']
oskmain = ['чмо', 'животное', 'хуйло', 'ебланище', 'трепло', 'быдло', 'говно', 'фуфло',
           'чучело', 'подобие человека', 'уёбище', 'говнорождающее предприятие',
           'чудище', 'чудовище', 'ничтожество', 'ублюдище', 'хранилище членов в заднице',
           'позорище', 'долбаёбище', 'мудило', 'пидорасище']
postfix = ['у тебя вообще нету алиби', 'и твоя мать давно уже не жива',
           'я с тебя одуреваю блять', 'батю найди потом пизди',
           'выйди из чата и не возвращайся блять', 'ливай с позором блять',
           'уходи нахуй и еблище закрыть не забудь за собой',
           'пойди маму свою обними покуда мозг совсем не сгнил',
           'понюхай яйца мне нахуй', 'купи себе презерватив и не размножайся',
           'прекращай бредить нахуй пока я тебе рот членом не заткнул',
           'заткни просто еблет и всё нахуй', 'закрой ебало своё и не еби мозги',
           'снимись в видосе брайн мапса хахаха']
mat = ['блять', 'сука', 'нахуй']
workwords = ['Так уж и быть, {user.first_name}, ради тебя - сгоняю.',
            'не',
            'We work to earn the right to work to earn the right to work to earn the right to work to earn the right to work to earn the right to give ourselves the right to buy ourselves the right to live to earn the right to die',
            'Я не так много придумал новых строчек для работы, {user.first_name}, так что иди нахуй блять!',
            'Ну хорошо, пойду рефакторить код второй раз после того как ушёл спать и забыл сохраниться',
            'ЭЭЭЭЭ ВСМЫСЛЕ РАБОТАТЬ а если я не хочу...\nсука меня ержаном сделали это пиздец господа!',
            'ну неее( ну мне лень( я не хочу((( ну лааадно, {user.first_name}(',
            'Опять на работу... Опять яндекс... Опять склад... Опять 24 часа смены... Баляяя...',
            'Оке, без вопросов хули',
            'да не, ну нахуй, какая работа, ебану чтоль бл\nойду лучше у бомжа пару копеек спизжу',
            'Вжжжж Вжжжж Бум Бум Бум чача чача чача КРРРРК\nРОБОТ БОТИС ИДЁТ НА РАБОТУ',
            'с тебя бутылка пива - с меня зарплата, идёт?',
            'Пойдём в макдак, мне там уютней\nВозьмём картошку на двоих\nА крошки скормим голубям\nИ в парке уткам...\n\nБлять так я же работать в макдаке буду( Ну ёбаный в рот того всего нахуй',
            'на работу говоришь?\nsome time\nyou gotta believe me\nit\'s not my fault that there\'s so much on tv\n\n> Вы нихуя не заработали! Ботис обленился!\n\nшутка',
            'Иду работать ладно сука блять\n{user.first_name} ты в 1% стремишься попасть, да? Свинья капиталистическая блять...\nладно, уважаю)',
            'БАБКИ БАБКИ СУКА БАБКИ',
            'я мишка гуми бэр вкуснейший гуми бэр\nзаходите в пивнуху по адресу московская 33 дробь 2\nвот такая нынче работа хули людей в пивнуху зазывать',
            'да иди нахуй, я лучше пентагон взломаю и файлы эпштейна солью за бабки чем работать буду']
  
client = TelegramClient(
    'Edge Sesh', os.getenv('API_ID'), os.getenv('API_HASH'),
    system_version = os.getenv('SYSTEM_VERSION'),
    device_model = os.getenv('DEVICE_MODEL'),
    app_version = os.getenv('APP_VERSION'),
    local_addr = ('0.0.0.0', 19133)).start(bot_token=os.getenv('TOKEN'))

@client.on(events.NewMessage(pattern='Ботис (.+)'))
async def _mainline(event):
    
    global database
    
    #if event.chat_id == TltFlood or event.chat_id == GreenFucker or event.chat_id == PMs or event.chat_id == TestingChat:
    if True:
        
        if 'оскорби' in event.raw_text:
            post_id = await event.get_reply_message()
            
            # Неповторяющиеся оски
            osk1 = choice(oskmain)
            osk2 = choice(oskmain)
            while osk2 == osk1:
                osk2 = choice(oskmain)
            # Неповторяющиеся прилагательные
            pref1 = choice(oskprefix)
            pref2 = choice(oskprefix)
            while pref2 == pref1:
                pref2 = choice(oskprefix)
                
            if post_id != None:
                await post_id.reply(f'{choice(prefix)}, {choice(adressing)} {pref1}, {pref2} {osk1}, {choice(postfix)}, {osk2} {choice(mat)}')
            else:
                await event.respond(f'{choice(prefix)}, {choice(adressing)} {pref1}, {pref2} {osk1}, {choice(postfix)}, {osk2} {choice(mat)}')
            print('Done!')
            
    #if event.chat_id == TltFlood or event.chat_id == TestingChat:
    if True:
            
        if 'иди на работу' in event.raw_text:
            if randint(1, 100) != 42:
                payout = randint(44, 228)
                user = await event.get_sender()
                account = database.find_one({'userId': str(event.sender_id)})
                if account:
                    if event.date - datetime.strptime(f'{account["lastWork"]}+00:00', '%Y-%m-%d %H:%M:%S%z') >= timedelta(minutes = 10):
                        await event.respond(choice(workwords).replace("{user.first_name}", user.first_name) + f"\n> Вы заработали {payout} скамкоинов!", parse_mode='markdown')
                        database.update_one(account, {'$inc': {'scamCoins': payout}, '$set': {'lastWork': event.date}})
                        
                    else:
                        await event.respond(f'{user.first_name}, ну ты {choice(oskmain)} {choice(oskprefix)}, дай отдохнуть {choice(mat)}... Заебался я в край {choice(mat)}')
                else:
                    database.insert_one({
                        'userId': str(event.sender_id),
                        'scamCoins': payout,
                        'lastWork': event.date
                        })
                    await event.respond(f'Так уж и быть, {user.first_name}, ради тебя - сгоняю.\n> Вы заработали {payout} скамкоинов!', parse_mode='markdown')
                
                
            # Пасхалка
            else:
                # Неповторяющиеся оски
                osk1 = choice(oskmain)
                osk2 = choice(oskmain)
                while osk2 == osk1:
                    osk2 = choice(oskmain)
                osk3 = choice(oskmain)
                while osk3 == osk2 or osk3 == osk1:
                    osk3 = choice(oskmain)
                    
                # Неповторяющиеся прилагательные
                pref1 = choice(oskprefix)
                pref2 = choice(oskprefix)
                while pref2 == pref1:
                    pref2 = choice(oskprefix)
                pref3 = choice(oskprefix)
                while pref3 == pref2 or pref3 == pref1:
                    pref3 = choice(oskprefix)
                    
                await event.reply(f'{choice(prefix)}, ты мне ещё командовать будешь, {osk1} {pref1}, {pref2} {osk2} {choice(mat)}? Рыло вальни, {choice(postfix)}, {pref3} {osk3} {choice(mat)}')

    if True:
        if 'баланс' in event.raw_text or 'балик' in event.raw_text:
            account = database.find_one({'userId': str(event.sender_id)})
            if account:
                await event.reply(f'Ваш баланс: {account["scamCoins"]} скамкоинов!')
            else:
                database.insert_one({
                    'userId': str(event.sender_id),
                    'scamCoins': 0,
                    'lastWork': datetime.strptime('2024-07-03 22:34:09+00:00', '%Y-%m-%d %H:%M:%S%z')
                })
                await event.reply('Ваш баланс: 0 скамкоинов!')
                
    if False:
        if 'крутка' in event.raw_text or 'гача' in event.raw_text:
            account = database.find_one({'userId': str(event.sender_id)})
            if account:
                if account["scamCoins"] < 500:
                    await event.reply(f'У вас недостаточно скамкоинов для крутки!\nНеобходимо 500 скамкоинов, а у вас всего лишь {account["scamCoins"]}\n\nНищета ебаная {choice(mat)}...')
                else:
                    char_id = random.choices([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], weights = [25, 25, 20, 10, 5, 10, 10, 10, 10, 10, 40, 40, 40, 40, 40, 35], k = 1)[0]
                    char_data = database.find_one({'chID': char_id})
                    database.update_one(account, {'$addToSet': {'characters': char_id}, '$set': {'scamCoins': account['scamCoins'] - 500}})
                    await event.reply(f'Вы получили...\n\nПерсонажа по имени {char_data["chName"]}!', file = InputPhoto(char_data["chImageID"], char_data["chAccessHash"], char_data["fileRef"]))
            else:
                database.insert_one({
                    'userId': str(event.sender_id),
                    'scamCoins': 0,
                    'lastWork': datetime.strptime('2024-07-03 22:34:09+00:00', '%Y-%m-%d %H:%M:%S%z')
                })
                await event.reply(f'У вас недостаточно скамкоинов для крутки!\nНеобходимо 500 скамкоинов, а у вас всего лишь 0\n\nНищета ебаная {choice(mat)}...')
                
    if True:
        if 'добавить персонажа 1133' in event.raw_text:
            chID = event.raw_text.split('\n')
            database.insert_one({
                'chID': int(chID[1]),
                'chName': chID[2],
                'chImageID': event.message.photo.id,
                'chAccessHash': event.message.photo.access_hash,
                'fileRef': event.message.photo.file_reference
                })

    if 'порно' in event.raw_text:
        await event.reply(f'весело задорно хули я ещё могу сказать {choice(mat)}')
            

client.start()
client.run_until_disconnected()











