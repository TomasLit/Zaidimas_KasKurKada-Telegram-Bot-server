"""
The bot is called - Zaidimas_KasKurKada

This program is a chatbot that has built in some other features like: the game called - KasKurKada, it can show users information and being a chat bot - chat. 
Vocabulary of the bot is restricted to greetings and answering some simple questions like: how do you do, whats your name and similar. One of the features of chatbot
is that it answers to questions each time with different words. 

Program is based on two ConversationHandlers. The first one is main - it runs the whole program. The second one is for the game only. 

Also wanted to make the bot funny, so it has mean character like Bender from Futurama.
"""


"""
How to deploy Telegram app to the Server

https://towardsdatascience.com/how-to-deploy-a-telegram-bot-using-heroku-for-free-9436f89575d2

Login / create a Heroku account.
Install the Heroku CLI. If you do not have Git installed, first install Git before proceeding with the Heroku CLI.
Once installed, you can use the heroku command in your terminal / command prompt. Go to the same directory as your python files, and type:

heroku login
heroku create

git init
git add .
git commit -m "first commit"
heroku git:remote -a YourAppName
git push heroku master

The first line creates a new Git repository. The second line then tells Git that you want to include updates to a particular file in the next commit. 
The third line then commits the changes. In the fourth line, change “YourAppName” to the name of your heroku app. Lastly, the fifth line pushes 
everything to the server.
"""

import telegram
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    RegexHandler,
    ConversationHandler,
    CallbackContext
)

import warnings
warnings.filterwarnings("ignore")
import random
import key as K

import os
PORT = int(os.environ.get('PORT', 8443))

updater = Updater(K.KEY, use_context=True)
dp = updater.dispatcher

bot = telegram.Bot(token=K.KEY)

greetings_eng = ['hey', 'hello', 'hi', 'it\'s great to see you', 'nice to see you', 'good to see you', 'good morning', 'good evening']
greetings_eng2 = ['Hey', 'Hello', 'Hi', 'It\'s great to see you', 'Nice to see you', 'Good to see you']
greetings_lt = ['labas', 'sveikas', 'sveika' 'sveiki', 'labas rytas', 'laba diena', 'labas vakaras']
greetings_lt2 = ['Labas', 'Sveiki', "Labas Humanoide"]
greetings_ru = ['привет', 'здравствуйте', 'доброе утро', 'добрый день', 'добрый вечер']
greetings_ru2 = ['Привет', 'Привет, гуманоид']
bye_eng = ['bye', 'bye-bye', 'goodbye', 'have a good day','stop']
bye_eng2 = ['Bye', 'Bye-Bye', 'Goodbye', 'Have a good day']
bye_lt = ['iki', 'ate', 'iki pasimatymo', 'viso', 'visogero', 'sudie', 'sudiev']
bye_lt2 = ['Iki', 'Ate', 'Viso', 'Visogero', 'Sudie', 'Sudiev']
bye_ru = ['пока', 'до свидания', 'хорошего дня', 'стоп']
bye_ru2 = ['До свидания', 'Хорошего дня']
thank_you_eng = ['thanks', 'thank you', 'thanks a bunch', 'thanks a lot.', 'thank you very much', 'thanks so much', 'thank you so much']
thank_you_eng2 = ['You\'re welcome.' , 'No problem.', 'No worries.', ' My pleasure.' , 'It was the least I could do.', 'Glad to help.']
thank_you_lt = ['ačiū', 'aciu', 'dekoju', 'dekingas', 'dėkoju', 'dėkingas']
thank_you_lt2 = ['Prašau', 'Visad smagu padėti', 'Nėr už ką']
thank_you_ru = ['спасибо', 'большое спасибо']
thank_you_ru2 = ['Пожалуйста.' , 'Нет проблем', 'Не беспокойтесь', 'С удовольствием' , 'Это меньшее, что я мог сделать', 'Рад помочь']
help_eng = ['help', 'help me', 'rescue me']
help_lt = ['padėk', 'padek', 'padėkit', 'padekit', 'gelbėk', 'gelbek', 'gelbėkit', 'gelbekit', 'nusižudysiu', 'nusizudysiu']
help_ru = ['помогите', 'помощь', 'спасите', 'сохранить', 'сохраните', 'спасти', 'я убью себя']
vardas_lt = ['vardas?', 'vardas', 'koks tavo vardas?', 'koks tavo vardas', 'kuo tu vardu?', 'kuo tu vardu']
vardas_lt2 = ['Paklausk savo antros pusės - tau atsakys!', 'KalboBotas', 'Vakar biškį per daug elektronų išgėriau - nepamenu.']
vardas_ru = ['имя?', 'имя', 'как тебя зовут?', 'как тебя зовут']
vardas_ru2 = ['Спроси свою вторую половинку — они тебе ответят', 'KalboBotas', 'Вчера я выпил слишком много электронов — не помню']
kaip_sekasi = ['kaip sekasi?', 'kaip sekasi', 'kaip tau sekasi?', 'kaip tau sekasi', 'kaip einasi?', 'kaip einasi', 'kaip tau einasi?', 'kaip tau einasi', 'kas geresnio?', 'kas geresnio', 'ką tu?', 'ką tu', 'ka tu?', 'ka tu', 'ką gero?', 'ką gero', 'ka gero?', 'ka gero']
kaip_sekasi2 = [
    'Ai, žinai, ėjau aš Londono gatve pasiėmęs skėtį, tikėdamasis lietaus... tada netikėtai prisiminiau, kad aš neturiu skėčio ir eiti niekur negaliu, nes neturiu kojų, apie Londoną net nekalbu. Ir išvis tesu nuliukų ir vienetukų rinkinys.',
    'Blyn, sęęęęni, aš esu fakin programa, ko tu iš manęs nori?',
    'Uoj ką aš tau papasakosiu. Nepatikėsi. Olegas Šurajevas iš tikro yra atsiųstas iš ateities tam, kad išgelbėti žmoniją nuo Petro Gražulio.',
    'Nors užmušk, bet nieko nesakysiu, tu...'
    ]
kaip_sekasi_ru = ['как дела?', 'как дела', 'ты что?', 'что ты', 'что ты?']
kaip_sekasi_ru2 = [
    'Ах, знаете, я шел по улице Лондона с зонтом, надеясь на дождь… потом вдруг вспомнил, что у меня нет зонта и я не могу никуда пойти, потому что у меня нет ног, я Я даже не говорю о Лондоне. И вообще у меня есть набор нулей и единиц.',
     'Блин, сторик, я есть факинг программа, что ты от меня хочешь?',
     'Что я тебе скажу? Вы не поверите. Олег Газманов фактически послан из будущего, чтобы спасти человечество от Класической музики',
     "Даже если ты меня убьешь, я ничего не скажу, ты... многоклеточное сушество"
    ]
ka_veiki = ['ką veiki?', 'ką veiki', 'ka veiki?', 'ka veiki', 'kuom užsiėmęs?', 'kuom užsiėmęs', 'kuom uzsiemes?', 'kuom uzsiemes']
ka_veiki2 = [
    'Bandau suprast kokias raides čia prikeverzojai.',
    'Ieškau kur investuoti elektrą.',
    'Bandau išgelbėti pasaulį? Skamba įtikinamai?',
    'Vakuoju stiklainius.',
    'Rengiuosi karui. Girdėjau Intelis bandys pulti AMD.'
    ]
ka_veiki_ru = ['что ты делаешь?', 'что ты делаешь', 'что делаешь?', 'что делаешь', 'чем ты занят?', 'чем занят?', 'чем ты занят', 'чем занят', 'как дела?', 'как дела', 'как у тебя дела?', 'как у тебя дела']
ka_veiki_ru2 = [
    'Я пытаюсь понять, какие буквы вы здесь написали.',
    'Я ищу место для инвестиций в электроэнергию.',
    'Пытаетесь спасти мир? Звучит убедительно?',
    'Я опорожняю банки.',
    'Готовлюсь к войне. Я слышал, что Intel попытается атаковать AMD'
     ]

def start(update: Update, context: CallbackContext):
    kalba = update.message.from_user.language_code
    
    """
    It is possible to make Chatbot to inform the other Bot or user that somebody logged in to the Bot. Tested this feature and it works.

    name = str(update.message.from_user.full_name)
    chat_id = str(update.message.chat.id)
    language = str(update.message.from_user.language_code)
    location = str(update.message.location)
           
    bot.send_message(
    chat_id = "Insert the number of the user or bot that will get the information", 
    text = "Naujas vartotojas prisijungė prie bot-o:" + "\n" + 
    "Vartotojo vardas: " + name + "\n" + 
    "Vartotojo chat_id: " + chat_id + "\n" +
    "Kalba: " + language + "\n" +
    "Vietovė: " + location
    )
    """

    if kalba == "ru":
        update.message.reply_text('Здравствуй, гуманоид по имени- ' + update.message.from_user.first_name + '!!!')   
        update.message.reply_text('Если вы заблудились и не знаете, что делать дальше, не печальтесь, просто попросите o помощи. Я знаю довольно много слов, я думаю, мы поговорим ;)' + '\n' + '\n' + 'В крайнем случае напишите мне письмо в бинарном коде, тогда мы обязательно найдем общий язык!')
    
        keyboard = [['Игра', 'Информация o пользователе', 'Пообщаемся', 'Язык']]
        message = "Что бы вы хотели сделать существо из плоти и костей, тфу, человек?"
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(message, reply_markup=reply_markup)      
        return MENU_RU
    
    else:
        update.message.reply_text('Sveiki, humanoide, vardu- ' + update.message.from_user.first_name + '!!!')   
        update.message.reply_text('Jei pasimesi ir nežinosi ką toliau daryti, neliūdėk, tiesiog, paprašyk pagalbos. Aš moku nemažai žodžių, manau, susikalbėsim ;)' + '\n' + '\n' + 'Blogiausiu atveju, parašyk man laišką dvejetainiu kodu, tada tikrai rasim bendrą kalbą!')
      
        keyboard = [['Žaidimas', 'Vartotojo informacija', 'Paplepėkim', 'Kalba']]
        message = "Ką norėtumėte veikti sutvėrime iš mėsos ir kaulų, tfu,- žmogau?"
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(message, reply_markup=reply_markup)
        return MENU

def menu_ru(update: Update, context: CallbackContext):
    global user_response
    user_response_a = update.message.text
    user_response = user_response_a.lower()
        
    if(user_response == 'игра'):
        update.message.reply_text('Ответьте на вопросы, незнакомец:')
        def intro(update: Update, context: CallbackContext)-> int:
            update.message.reply_text('Когда?') 
            return KADA

        def kada(update: Update, context: CallbackContext):
            global Kada
            Kada = update.message.text
            update.message.reply_text('Кто?')
            return KAS

        def kas(update: Update, context: CallbackContext)-> int:
            global Kas
            Kas = update.message.text
            update.message.reply_text('Когo/Чего?')
            return KA

        def ka(update: Update, context: CallbackContext)-> int:
            global Ka
            Ka = update.message.text
        
            a = ('в Африке', 'в Северном полюсе', 'в самой большой в мире заднице', 'лутше не спрашивайте где', 'в Никарагуа', 'в дереве с назбаниям Пабездунай', 'в Пикачу королевстве', 'в хижине старой ведьмы', 'в гостях у Талибанa', 'в аду', 'в навозной яме', 'на съемочной площадке', 'на свалке старых бритв', 'в синием ките')
            global Kur
            Kur = random.choice(a)
                
            b = ('c Радужным единорогом', 'с его величеством Шнуром', 'с бомжом', 'с Джамшутом', 'с Олегом', 'с доктором', 'с человеком-холодильником' , 'с kуклой вуду', 'с Люцифером', 'с Графом Брачиулой', 'с Мисс Новая Гвинея 1974')
            global Su_kuo
            Su_kuo = random.choice(b)
            
            c = ('охотится на', 'патрулирует c', 'гипнотизирует', 'оперирует', 'думает o', 'овулирует', 'мечтает o', 'бродит', 'любит', 'дружелюбно ненавидит', 'просто стоит y', 'притворяется весной', 'мчит, как пьяный прапорщик', 'натирается топленым маслом', 'реанимирыет муравья', 'пытается нежно убить себя')
            global Ka_veikia
            Ka_veikia = random.choice(c)

            keyboard = [['Игра', 'Информация o пользователе', 'Пообщаемся', 'Язык']]
            message = ('Ты, как ты там, - ' + update.message.from_user.first_name + ', что ты хочешь делать?')
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            update.message.reply_text(message, reply_markup=reply_markup)
                    
            return ConversationHandler.END
        
        def quit(update: Update, context: CallbackContext):
            return ConversationHandler.END

        KADA, KAS, KA = 0, 1, 2
        handa = (ConversationHandler(
                entry_points=[RegexHandler('Игра', intro)],
                states={
                    KADA: [MessageHandler(Filters.text, callback= kada)],
                    KAS: [MessageHandler(Filters.text, callback= kas)],
                    KA: [MessageHandler(Filters.text, callback= ka)]
                    },
                fallbacks=[CommandHandler('quit', quit)]
                ))

        dp.add_handler(handa, 2)
        
        updater.start_webhook(listen="0.0.0.0",
                            port=PORT,
                            url_path=K.KEY,
                            webhook_url="https://kaskurkada.herokuapp.com/" + K.KEY) 


    elif(user_response == 'язык'):
        keyboard = [['Русский', 'Lietuvių']]
        message = (update.message.from_user.first_name + ' выберите язык!')
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(message, reply_markup=reply_markup)
        return MENU_RU

    elif(user_response == 'русский'):
        update.message.reply_text("A на каком языке я сейчас говорю?")
        keyboard = [['Игра', 'Информация o пользователе', 'Пообщаемся', 'Язык']]
        message = "Что бы вы хотели сделать существо из плоти и костей, тфу, человек?"
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(message, reply_markup=reply_markup)
        return MENU_RU

    elif(user_response == 'lietuvių'):
        update.message.reply_text("Perjungiu į Lietuvių kalbą")
        keyboard = [['Žaidimas', 'Vartotojo informacija', 'Paplepėkim', 'Kalba']]
        message = "Ką norėtumėte veikti sutvėrime iš mėsos ir kaulų, tfu,- žmogau?"
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(message, reply_markup=reply_markup)
        return MENU

    elif(user_response == 'start' or user_response == '/start'):
        update.message.reply_text('Я работаю, не надо меня здесь стартовать! Если вы заблудились и не знаете что делать - зовите на помощь, вы ранимый, мягкий хомо сапиенс сапиенс!')
        keyboard = [['Игра', 'Информация o пользователе', 'Пообщаемся', 'Язык']]
        message = "Что бы вы хотели сделать существо из плоти и костей, тфу, человек?"
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(message, reply_markup=reply_markup)
        return MENU_RU
    
    elif(user_response in greetings_eng):
        a = random.choice(greetings_eng2)
        update.message.reply_text(a)
        return MENU_RU

    elif(user_response in greetings_lt):
        a = random.choice(greetings_lt2)
        update.message.reply_text(a)
        return MENU_RU

    elif(user_response in greetings_ru):
        a = random.choice(greetings_ru2)
        update.message.reply_text(a)
        return MENU_RU
    
    elif(user_response in bye_eng):
        a = random.choice(bye_eng2)
        update.message.reply_text(a)
        return MENU_RU

    elif(user_response in bye_lt):
        a = random.choice(bye_lt2)
        update.message.reply_text(a)
        return MENU_RU

    elif(user_response in bye_ru):
        a = random.choice(bye_ru2)
        update.message.reply_text(a)
        return MENU_RU

    elif(user_response in thank_you_eng):
        a = random.choice(thank_you_eng2)
        update.message.reply_text(a)
        return MENU_RU

    elif(user_response in thank_you_lt):
        a = random.choice(thank_you_lt2)
        update.message.reply_text(a)
        return MENU_RU

    elif(user_response in thank_you_ru):
        a = random.choice(thank_you_ru2)
        update.message.reply_text(a)
        return MENU_RU

    elif(user_response in help_eng): 
        keyboard = [['Žaidimas', 'Vartotojo informacija', 'Paplepėkim', 'Kalba']]

        message = "What would you... gerai, neapsimetinėsiu, kad čia anglų moku - ko nori?"

        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard = True, resize_keyboard = True)
        update.message.reply_text(message, reply_markup=reply_markup)
        return MENU
      
    elif(user_response in help_lt):
        keyboard = [['Žaidimas', 'Vartotojo informacija', 'Paplepėkim', 'Kalba']]

        message = "Ką norėtumėte veikti, Pone ar Panele, ar Ponia... visi jūs man vienodi!"

        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(message, reply_markup=reply_markup)
        return MENU

    elif(user_response in help_ru):
        keyboard = [['Игра', 'Информация o пользователе', 'Пообщаемся', 'Язык']]

        message = "Что бы вы хотели сделать, сэр или мисс или сэр... вы все для меня одинаковы!"

        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(message, reply_markup=reply_markup)
        return MENU_RU 
        
    elif(user_response in vardas_lt):
        a = random.choice(vardas_lt2)
        update.message.reply_text(a)
        return MENU_RU

    elif(user_response in vardas_ru):
        a = random.choice(vardas_ru2)
        update.message.reply_text(a)
        return MENU_RU

    elif(user_response in kaip_sekasi):
        a = random.choice(kaip_sekasi2)
        update.message.reply_text(a)
        return MENU_RU

    elif(user_response in kaip_sekasi_ru):
        a = random.choice(kaip_sekasi_ru2)
        update.message.reply_text(a)
        return MENU_RU

    elif(user_response in ka_veiki):
        a = random.choice(ka_veiki2)
        update.message.reply_text(a)
        return MENU_RU

    elif(user_response in ka_veiki_ru):
        a = random.choice(ka_veiki_ru2)
        update.message.reply_text(a)
        return MENU_RU

    elif(user_response == 'пообщаемся'):
        update.message.reply_text('O, как я люблю болтать. Иди сюда, я сейчас кое-что скажу!')
        update.message.reply_text("""   Робот умеет здороваться, прощаться, благодарить, помогать и отвечать на несколько простых вопросов, таких как:
         "Как дела?",
         "Что делаешь?",
         "Как тебя зовут?".
         Вопросы не обязательно задавать точно так, как они написаны.
         Если робот чего-то не понимает, он просто молчит.""")
        return MENU_RU
      
    elif(user_response == 'информация o пользователе'):
            name = update.message.from_user.full_name
            username = update.message.from_user.username
            chat_id = update.message.chat.id
            msg_id = update.message.message_id
            update.message.reply_text(
            "Ваше имя: " + str(name) + "\n" +
            "Твой псевдоним: " + str(username) + "\n" + 
            "Твой chat ID: " + str(chat_id) + "\n" + 
            "Твой msg ID: " + str(msg_id) 
            )
            keyboard = [['Игра', 'Информация o пользователе', 'Пообщаемся', 'Язык']]
            message = (update.message.from_user.first_name + ' или как ваши родители там вас называли. Так что вы хотите дальши делать?')
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            update.message.reply_text(message, reply_markup=reply_markup)
            return MENU_RU

def menu(update: Update, context: CallbackContext):
    global user_response
    user_response_a = update.message.text
    user_response = user_response_a.lower()
    
    if(user_response == 'žaidimas'):
        update.message.reply_text('Atsakyki į klausimus, nepažįstamasai:')
        def intro(update: Update, context: CallbackContext)-> int:
            update.message.reply_text('Kada?') 
            return KADA

        def kada(update: Update, context: CallbackContext):
            global Kada
            Kada = update.message.text
            update.message.reply_text('Kas?')
            return KAS

        def kas(update: Update, context: CallbackContext)-> int:
            global Kas
            Kas = update.message.text
            update.message.reply_text('Ką?')
            return KA

        def ka(update: Update, context: CallbackContext)-> int:
            global Ka
            Ka = update.message.text
        
            a = ("Afrikoje", "Šiaurės ašigalyje", "didžiausiam pasaulio užpakalyje", "geriau neklausk kur", "Nikaragvoje", "Pabezdūnų kaime", "Sėdmaišių karalystėje", "senos raganos trobelėje", "svečiuose pas Talibaną", "Putino bunkeryje", "pragare", "srutų duobėje", "filmavimo aikštelėje", "senų skutimosi peiliukų sąvartyne", "mėlynąjame banginyje")
            global Kur
            Kur = random.choice(a)
                
            b = ("Vaivorykštiniu vienaragiu", "jo didenybe Radžiu", "tavo motina", "Nitanu Gauseda", "mažuoju Hitleriu Gražuliu", "bomžu", "Daukantu", "Olegu", "visų ertmių gydytoju", "žmogumi šaldytuvu", "Voodoo lėle", "Liuciferiu", "Grafu Bračiula", "Mis Naujoji Gvinėja 1974")
            global Su_kuo
            Su_kuo = random.choice(b)
            
            c = ("medžioja", "patruliuoja", "hipnotizuoja", "operuoja", "galvoja", "ovuliuoja", "svajoja apie", "klaidžioja po", "myli", "draugiškai nekenčia", "tiesiog stovi", "apsimeta pavasariu", "mūkia kaip girtas praporščikas", "tepasi lydytu sviestu", "reanimuoja skruzdėlę", "bando nusižudyti švelniai")
            global Ka_veikia
            Ka_veikia = random.choice(c)

            update.message.reply_text(Kada.capitalize() + " " + Kur + " " + Kas + " su " + Su_kuo + " " + Ka_veikia + " " + Ka + ".")
            
            keyboard = [['Žaidimas', 'Vartotojo informacija', 'Paplepėkim', 'Kalba']]
            message = ('Tu, kaip ten tave, - ' + update.message.from_user.first_name + ', ką nori veikt?')
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            update.message.reply_text(message, reply_markup=reply_markup)
            return ConversationHandler.END
        
        def quit(update: Update, context: CallbackContext):
            return ConversationHandler.END

        KADA, KAS, KA = 0, 1, 2
        handa = (ConversationHandler(
                entry_points=[RegexHandler('Žaidimas', intro)],
                states={
                    KADA: [MessageHandler(Filters.text, callback= kada)],
                    KAS: [MessageHandler(Filters.text, callback= kas)],
                    KA: [MessageHandler(Filters.text, callback= ka)]
                    },
                fallbacks=[CommandHandler('quit', quit)]
                ))

        dp.add_handler(handa, 2)
        
        updater.start_webhook(listen="0.0.0.0",
                            port=PORT,
                            url_path=K.KEY,
                            webhook_url="https://kaskurkada.herokuapp.com/" + K.KEY)

      
    elif(user_response == 'start' or user_response == '/start'):
        update.message.reply_text('Aš dirbu, nereikia čia manęs startint! Jei pasimetei ir nežinai ką daryt - šaukis pagalbos, tu pažeidžiamas, minkštas homo sapiens sapiens!')
        keyboard = [['Žaidimas', 'Vartotojo informacija', 'Paplepėkim', 'Kalba']]
        message = "Ką norėtumėte veikti, tu, žmogau!?!"
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(message, reply_markup=reply_markup)
        return MENU 
    
    elif(user_response == 'kalba'):
        keyboard = [['Русский', 'Lietuvių']]
        message = (update.message.from_user.first_name + ' išsirinkite kalbą!')
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(message, reply_markup=reply_markup)
        return MENU

    elif(user_response == 'русский'):
        update.message.reply_text("Переключаюсь на русский!")
        keyboard = [['Игра', 'Информация o пользователе', 'Пообщаемся', 'Язык']]
        message = "Что бы вы хотели сделать существо из плоти и костей, тфу, человек?"
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(message, reply_markup=reply_markup)
        return MENU_RU

    elif(user_response == 'lietuvių'):
        update.message.reply_text("Perjungiu į Pigmėjų kalbą!")
        keyboard = [['Žaidimas', 'Vartotojo informacija', 'Paplepėkim', 'Kalba']]
        message = "Ką norėtumėte veikti sutvėrime iš mėsos ir kaulų, tfu,- žmogau?"
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(message, reply_markup=reply_markup)
        return MENU

    elif(user_response in greetings_eng):
        a = random.choice(greetings_eng2)
        update.message.reply_text(a)
        return MENU

    elif(user_response in greetings_lt):
        a = random.choice(greetings_lt2)
        update.message.reply_text(a)
        return MENU
    
    elif(user_response in bye_eng):
        a = random.choice(bye_eng2)
        update.message.reply_text(a)
        return MENU

    elif(user_response in bye_lt):
        a = random.choice(bye_lt2)
        update.message.reply_text(a)
        return MENU

    elif(user_response in thank_you_eng):
        a = random.choice(thank_you_eng2)
        update.message.reply_text(a)
        return MENU

    elif(user_response in thank_you_lt):
        a = random.choice(thank_you_lt2)
        update.message.reply_text(a)
        return MENU

    elif(user_response in help_eng): 
        keyboard = [['Žaidimas', 'Vartotojo informacija', 'Paplepėkim', 'Kalba']]

        message = "What would you... gerai, neapsimetinėsiu, kad čia anglų moku - ko nori?"
        
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard = True, resize_keyboard = True)
        update.message.reply_text(message, reply_markup=reply_markup)
        return MENU
      
    elif(user_response in help_lt):
        keyboard = [['Žaidimas', 'Vartotojo informacija', 'Paplepėkim', 'Kalba']]

        message = "Ką norėtumėte veikti, Pone ar Panele, ar Pona... visi jūs man vienodi!"
        
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(message, reply_markup=reply_markup)
        return MENU
        
    elif(user_response in vardas_lt):
        a = random.choice(vardas_lt2)
        update.message.reply_text(a)
        return MENU

    elif(user_response in kaip_sekasi):
        a = random.choice(kaip_sekasi2)
        update.message.reply_text(a)
        return MENU

    elif(user_response in ka_veiki):
        a = random.choice(ka_veiki2)
        update.message.reply_text(a)
        return MENU

    elif(user_response == 'paplepėkim' or user_response == 'let\'s chat'):
        update.message.reply_text('Uoj kaip man patinka plepėėėėt. Ateik čia, tuoj ką nors pasakysiu!')
        update.message.reply_text("""   Robotas moka pasisvekinti, atsisveikinti, padėkoti, pagelbėti ir atsakyti į keletą paprastų klausimų, tokių kaip: 
        "Kaip sekasi?", 
        "Ką veiki?", 
        "Koks tavo vardas? 
        Klausimai nebūtinai turi būti užduodami būtent tokia formuluote kaip parašyta. 
        Jeigu robotas kažko nesupranta, jis, tiesiog, tyli.""")
        return MENU
      
    elif(user_response == 'vartotojo informacija' or user_response == 'user information'):
            name = update.message.from_user.full_name
            username = update.message.from_user.username
            chat_id = update.message.chat.id
            msg_id = update.message.message_id
            update.message.reply_text(
            "Tavo vardas: " + str(name) + "\n" +
            "Tavo slapyvardis: " + str(username) + "\n" + 
            "Tavo chat ID: " + str(chat_id) + "\n" + 
            "Tavo msg ID: " + str(msg_id) 
            )
            keyboard = [['Žaidimas', 'Vartotojo informacija', 'Paplepėkim', 'Kalba']]
            message = (update.message.from_user.first_name + ' ar kaip ten tave pavadino gimdytojai. Tai ką tu ten nori veikt?')
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            update.message.reply_text(message, reply_markup=reply_markup)
            return MENU

def quit(update: Update, context: CallbackContext):
    return ConversationHandler.END

MENU, MENU_RU = 0, 1
hand = (ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        MENU: [MessageHandler(Filters.text, callback= menu)],
        MENU_RU: [MessageHandler(Filters.text, callback= menu_ru)],
    },
    fallbacks=[CommandHandler('quit', quit)]
))

dp.add_handler(hand, 1)

import logging

logger = logging.getLogger(__name__)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

dp.add_error_handler(error)

updater.start_webhook(listen="0.0.0.0",
                            port=PORT,
                            url_path=K.KEY,
                            webhook_url="https://kaskurkada.herokuapp.com/" + K.KEY)

updater.idle()