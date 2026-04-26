from telethon import TelegramClient, events, Button
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
characterDatabase = db['characters']
userDatabase = db['user_data']
storyDatabase = db['stories']

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
                account = userDatabase.find_one({'userId': str(event.sender_id)})
                if account:
                    if event.date - datetime.strptime(f'{account["lastWork"]}+00:00', '%Y-%m-%d %H:%M:%S%z') >= timedelta(minutes = 10):
                        await event.respond(choice(workwords).replace("{user.first_name}", user.first_name) + f"\n> Вы заработали {payout} скамкоинов!", parse_mode='markdown')
                        userDatabase.update_one(account, {
                            '$inc': {'scamCoins': payout},
                            '$set': {'lastWork': event.date}
                        })
                        
                    else:
                        await event.respond(f'{user.first_name}, ну ты {choice(oskmain)} {choice(oskprefix)}, дай отдохнуть {choice(mat)}... Заебался я в край {choice(mat)}')
                else:
                    userDatabase.insert_one({
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
            account = userDatabase.find_one({'userId': str(event.sender_id)})
            if account:
                await event.reply(f'Ваш баланс: {account["scamCoins"]} скамкоинов!')
            else:
                userDatabase.insert_one({
                    'userId': str(event.sender_id),
                    'scamCoins': 0,
                    'lastWork': datetime.strptime('2024-07-03 22:34:09+00:00', '%Y-%m-%d %H:%M:%S%z')
                })
                await event.reply('Ваш баланс: 0 скамкоинов!')

    if 'кто канон пейринг с Растом?' in event.raw_text:
        await event.reply('Очевидно, что это @VeraKorneplod')
                
    if False:
        if 'крутка' in event.raw_text or 'гача' in event.raw_text:
            account = userDatabase.find_one({'userId': str(event.sender_id)})
            if account:
                if account["scamCoins"] < 500:
                    await event.reply(f'У вас недостаточно скамкоинов для крутки!\nНеобходимо 500 скамкоинов, а у вас всего лишь {account["scamCoins"]}\n\nНищета ебаная {choice(mat)}...')
                else:
                    char_id = random.choices([10, 11, 12, 13, 14, 15], weights = [20, 40, 30, 20, 30], k = 1)[0]
                    char_data = userDatabase.find_one({'chID': char_id})
                    userDatabase.update_one(account, {
                        '$addToSet': {'characters': char_id},
                        '$set': {'scamCoins': account['scamCoins'] - 500}
                    })
                    await event.reply(f'Вы получили...\n\nПерсонажа по имени {char_data["chName"]}!', file = InputPhoto(char_data["chImageID"], char_data["chAccessHash"], char_data["fileRef"]))
            else:
                userDatabase.insert_one({
                    'userId': str(event.sender_id),
                    'scamCoins': 0,
                    'lastWork': datetime.strptime('2024-07-03 22:34:09+00:00', '%Y-%m-%d %H:%M:%S%z')
                })
                await event.reply(f'У вас недостаточно скамкоинов для крутки!\nНеобходимо 500 скамкоинов, а у вас всего лишь 0\n\nНищета ебаная {choice(mat)}...')
                
    if event.is_private:
        if 'добавить персонажа 1133' in event.raw_text:
            chID = event.raw_text.split('\n')
            characterDatabase.insert_one({
                'chID': int(chID[1]),
                'chName': chID[2],
                'chImageID': event.message.photo.id,
                'chAccessHash': event.message.photo.access_hash,
                'fileRef': event.message.photo.file_reference
                })
                  
    #if event.is_private:
    if 'свидание' in event.raw_text or 'свиданка' in event.raw_text:
        account = userDatabase.find_one({'userId': str(event.sender_id)})
        if account:
            if "loveIntrest" in account:
                storyCluster = storyDatabase.find_one({"chId": account["loveIntrest"]["chId"]})
                #await event.reply(str(storyCluster[f'Date {randint(1, 20)}']))
                keyboard = []
                dateID = randint(1, len(storyCluster) - 1)
                dateNumber = "Date " + str(dateID)
                
                buttonData = 'a' + str(f"{storyCluster[dateNumber]['Option 1']['Value']}") + 'z' + str(event.sender_id) + 'i' + str(dateID)
                buttonData = buttonData.encode()
                keyboard.append([Button.inline(f"1. {storyCluster[dateNumber]['Option 1']['Value']}", buttonData)])
                
                buttonData = 'b' + str(f"{storyCluster[dateNumber]['Option 2']['Value']}") + 'z' + str(event.sender_id) + 'i' + str(dateID)
                buttonData = buttonData.encode()
                keyboard.append([Button.inline(f"2. {storyCluster[dateNumber]['Option 2']['Value']}", buttonData)])
                
                buttonData = 'c' + str(f"{storyCluster[dateNumber]['Option 3']['Value']}") + 'z' + str(event.sender_id) + 'i' + str(dateID)
                buttonData = buttonData.encode()
                keyboard.append([Button.inline(f"3. {storyCluster[dateNumber]['Option 3']['Value']}", buttonData)])

                #building the date string

                dateString = f"<b>{storyCluster[dateNumber]['Date name']}</b>\n\n{storyCluster[dateNumber]['Date description']}\n\n"
                dateString = dateString + f"1. <i>{storyCluster[dateNumber]['Option 1']['description']}</i>\n"
                dateString = dateString + f"2. <i>{storyCluster[dateNumber]['Option 2']['description']}</i>\n"
                dateString = dateString + f"3. <i>{storyCluster[dateNumber]['Option 3']['description']}</i>\n"

                await event.respond(dateString, buttons=keyboard, parse_mode='html')
            else:
                await event.reply('Любовный интерес не найден! Выберите его в личных сообщениях бота с помощью комманды "любовь".')
        else:
            await event.reply('Аккаунт не найден! Зарегистрируйтесь в личных сообщениях бота с помощью комманды "регистрация".')
        
        #keyboard = [
        #    [Button.inline("First option", b"1")],
        #    [Button.inline("Second option", b"2")],
        #    [Button.inline("Third option", b"3")]
        #]
        #await event.respond(f'весело задорно хули я ещё могу сказать {choice(mat)}', buttons=keyboard)
        

    if event.is_private:

        if 'любовь' in event.raw_text:
            account = userDatabase.find_one({'userId': str(event.sender_id)})
            keyboard = []
            if 13 in account["characters"]:
                answerString = 'l13' + str(event.sender_id)
                answerString = answerString.encode()
                keyboard.append([Button.inline("Zero_One", answerString)])
            if 12 in account["characters"]:
                answerString = 'l12' + str(event.sender_id)
                answerString = answerString.encode()
                keyboard.append([Button.inline("Rust", answerString)])
            if 11 in account["characters"]:
                answerString = 'l11' + str(event.sender_id)
                answerString = answerString.encode()
                keyboard.append([Button.inline("Doc", answerString)])
            if 15 in account["characters"]:
                answerString = 'l15' + str(event.sender_id)
                answerString = answerString.encode()
                keyboard.append([Button.inline("Armstrong", answerString)])
            if 14 in account["characters"]:
                answerString = 'l14' + str(event.sender_id)
                answerString = answerString.encode()
                keyboard.append([Button.inline("Tesla", answerString)])

            if len(keyboard) != 0:
                await event.respond(f'Выберите персонажа с которым вы хотите встречаться!', buttons=keyboard)
            else:
                await event.respond('У вас нет персонажей с которыми можно было бы встречаться! Время пойти в казик!!!')

        
        
        if 'регистрация' in event.raw_text:
            userData = event.raw_text.split()
            if len(userData) == 2:
                await event.respond('Чтобы зарегистрировать аккаунт для свиданий, напишите \"регистрация [М/Ж] [Имя]\"')
            if len(userData) == 4:
                errorHappened = False
                if userData[2] != 'Ж' and userData[2] != 'ж' and userData[2] != 'М' and userData[2] != 'м':
                    await event.respond('ало еблище отформатируй правильно команду мне лень писать адекватный процесс регистрации')
                    errorHappened = True
                else:
                    if userData[2] == 'Ж' or userData[2] == 'ж':
                        isuserMale = False
                    if userData[2] == 'М' or userData[2] == 'м':
                        isuserMale = True
                if userData[3].isalpha() and userData[3].istitle() :
                    userDatingName = userData[3]
                else:
                    await event.respond('имя должно быть одним словом и с большой буквы капец ты тупица нахуй хахаах учи русский язык мудила')
                    errorHappened = True
                if errorHappened:
                    await event.respond('ну короче регистрация не прошла, попробуй снова я хз, я обдолбан в нулину и не могу нормальную регистрацию сделать без утечек памяти и ошубок')
                else:
                    account = userDatabase.find_one({'userId': str(event.sender_id)})
                    if account:
                        userDatabase.update_one(account, {'$set':
                                {
                                "genderMale": isuserMale,
                                "userName": userDatingName
                                }
                        })
                        await event.reply('Регистрация прошла успешно!')
                    else:
                        userDatabase.insert_one({
                            'userId': str(event.sender_id),
                            'scamCoins': 0,
                            'lastWork': datetime.strptime('2024-07-03 22:34:09+00:00', '%Y-%m-%d %H:%M:%S%z'),
                            'genderMale': isuserMale,
                            'userName': userDatingName
                        })
                        await event.reply('Регистрация прошла успешно!')

@client.on(events.CallbackQuery())
async def callback(event):

    if str(event.data)[2] == 'l':
        if str(event.sender_id) == str(event.data)[5:-1]:
            account = userDatabase.find_one({'userId': str(event.sender_id)})
            if not ("loveIntrest" in account):
                if str(event.data)[3:5] == '11':
                    userDatabase.update_one(account, {'$set': {"loveIntrest": {'chId': 11, 'affection': 0}}})
                    await event.answer('Вы успешно выбрали Дока!')
                if str(event.data)[3:5] == '12':
                    userDatabase.update_one(account, {'$set': {"loveIntrest": {'chId': 12, 'affection': 0}}})
                    await event.answer('вы выбрали раста')
                if str(event.data)[3:5] == '13':
                    userDatabase.update_one(account, {'$set': {"loveIntrest": {'chId': 13, 'affection': 0}}})
                    await event.answer('Вы успешно выбрали Зирована!')
                if str(event.data)[3:5] == '14':
                    userDatabase.update_one(account, {'$set': {"loveIntrest": {'chId': 14, 'affection': 0}}})
                    await event.answer('Вы успешно выбрали Теслу!')
                if str(event.data)[3:5] == '15':
                    userDatabase.update_one(account, {'$set': {"loveIntrest": {'chId': 15, 'affection': 0}}})
                    await event.answer('Вы успешно выбрали Армстронга!')
            else:
                await event.answer('К сожалению, вы уже встречаетесь!')
        else:
            await event.answer('это не твоя кнопка ебло утиное блять')

    z = str(event.data).find('z')
    if z != -1:
        i = str(event.data).find('i')
        if str(event.sender_id) == str(event.data)[z+1:i]:
            account = userDatabase.find_one({'userId': str(event.sender_id)})
            if account["scamCoins"] >= int(str(event.data)[3:z]):
                storyCluster = storyDatabase.find_one({"chId": account["loveIntrest"]["chId"]})
                dateNumber = "Date " + str(event.data)[i+1:-1]
                if str(event.data)[2] == 'a':
                    await client.edit_message(event.chat_id, event.message_id, f"<a href='tg://user?id={str(event.sender_id)}'>{account['userName']}</a>,\n{storyCluster[dateNumber]["Result 1"]}", parse_mode='html')
                    newAffection = account["loveIntrest"]["affection"] + 1
                if str(event.data)[2] == 'b':
                    await client.edit_message(event.chat_id, event.message_id, f"<a href='tg://user?id={str(event.sender_id)}'>{account['userName']}</a>,\n{storyCluster[dateNumber]["Result 2"]}", parse_mode='html')
                    newAffection = account["loveIntrest"]["affection"] + 2
                if str(event.data)[2] == 'c':
                    await client.edit_message(event.chat_id, event.message_id, f"<a href='tg://user?id={str(event.sender_id)}'>{account['userName']}</a>,\n{storyCluster[dateNumber]["Result 3"]}", parse_mode='html')
                    newAffection = account["loveIntrest"]["affection"] -3
                    
                userDatabase.update_one(account, {'$set':
                    {
                    "loveIntrest": {
                        "affection": newAffection
                    },
                    "scamCoins": account["scamCoins"] - int(str(event.data)[3:z])
                    }
                })
                
            else:
                await event.answer(f"У вас недостаточно скамкоинов для этого действия!\nВаш балик: {account["scamCoins"]}\nНеобходимо: {int(str(event.data)[3:z])}")
        else:
            await event.answer("Exception logged in \"fuzzy-fishstick/main.py\":\nstr(event.data)[z+1:i-1] is not equal to userDatabase.find_one({'userId': str(event.sender_id)})")
            #await event.respond(f"{str(event.sender_id)}\n{str(event.data)[z+1:i-1]}")
    else:
        await event.answer("Exception: z > -1")

client.start()
client.run_until_disconnected()



