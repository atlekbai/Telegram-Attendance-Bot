from telebot import TeleBot, types
import datetime
import consts
import sqlite3
bot = TeleBot(consts.token)
start_day = datetime.datetime(2017, 5, 1, 17, 00)
now = datetime.datetime.now()

conn = sqlite3.connect('my.db', check_same_thread=False)
c = conn.cursor()

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton('Поделиться моим местоположением',request_location=True))
    bot.send_message(message.chat.id, 'Утречка ✌️ Ты сейчас где?', reply_markup=markup)
    add_user(message.from_user.first_name,
             message.from_user.username,
             message.from_user.last_name,
             str(message.from_user.id),
             0)
    print("yay!")

@bot.message_handler(content_types=['location'])
def handle_location(message):

    upd = bot.get_updates()
    last_update = upd[-1]
    msg_from_user = last_update.message
    location = msg_from_user.location
    longitude = location.longitude
    latitude = location.latitude

    bot.send_message(message.chat.id,distance(latitude,longitude))
    is_here=distance(latitude,longitude)[1]

    c.execute('SELECT * FROM users')
    row = c.fetchone()
    while row is not None:
        if int(row[4]) == msg_from_user.from_user.id:
            at=row[5]
            print(at==26)
            if is_here == True:
                user_markup = types.ReplyKeyboardMarkup()
                user_markup.row('темное поло, светлые джинсы', 'арабская паранжа')
                user_markup.row('цветочное платье', 'клоунский парик')
                bot.send_message(message.chat.id, "Во что сегодня одет Дагар?", reply_markup=user_markup)

                @bot.message_handler(content_types=['text'])
                def handle_text(msg):
                    upd = bot.get_updates()
                    last_update = upd[-1]
                    msg_from_user = last_update.message
                    if msg_from_user.text == 'темное поло, светлые джинсы':
                        counter=at+1
                        print(counter)
                        c.execute("UPDATE users SET attend=%s WHERE user_id=%s" % (counter, msg_from_user.from_user.id))
                        user_markup = types.ReplyKeyboardMarkup()
                        user_markup.row('/game')
                        bot.send_message(msg.chat.id, 'Молодец, хорошего тебе дня! 😄',reply_markup=user_markup)
                    else:
                        bot.send_message(msg_from_user.chat.id, 'Ха, попался! Лучше бы тебе поторопиться в аудиторию😡')
            else:
                bot.send_message(message.chat.id, "Беги, " + msg_from_user.from_user.first_name)
        row = c.fetchone()

@bot.message_handler(commands=['game'])
def handle_game(message):
    delta = now - start_day
    diff_days=delta.days
    c.execute('SELECT * FROM users')
    row = c.fetchone()
    print(message.from_user.id)
    while row is not None:
        # print(row[4])
        if int(row[4]) == message.from_user.id:
            attendance = row[5]/(diff_days-diff_days/6)
            total = attendance*100
            bot.send_message(message.chat.id, (row[1]+" "+row[3]+" - attendance:"+" "+str(total)[0:4]+'%'))
            row = c.fetchone()

            if(total <= 100 and total > 80):
                bot.send_message(message.chat.id, 'Из тебя выйдет профессионал своего дела! Отличная посещаемость👍')
            elif (total <= 80 and total > 50):
                bot.send_message(message.chat.id, 'Стоит немного постараться и все будет. Главное - приходить почаще🤔')
            elif (total <= 50 and total > 20):
                bot.send_message(message.chat.id, 'Кто-то совсем разленился, и нужно стать ответственнее за свое будущее😛')
            else:
                bot.send_message(message.chat.id, 'А это уже серьезно! Может стоит наконец задуматься?!!😕')
        row = c.fetchone()

@bot.message_handler(commands=['all_game'])
def handle_allgame(message):
    delta = now - start_day
    diff_days=delta.days
    c.execute('SELECT * FROM users')
    row = c.fetchone()
    print(message.from_user.id)
    while row is not None:
        # print(row[4])
        attendance = row[5] / (diff_days - diff_days / 6)
        total = attendance * 100
        bot.send_message(message.chat.id, (row[1] + " " + row[3] + " - attendance:" + " " + str(total)[0:4] + '%'))
        row = c.fetchone()

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id,'/game - узнать свою посещаемость \n /lesson - отметиться на уроке')

@bot.message_handler(commands=['lesson'])
def handle_lesson(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton('Поделиться моим местоположением', request_location=True))
    bot.send_message(message.chat.id, 'Пойти на урок', reply_markup=markup)

@bot.message_handler(commands=['team'])
def handle_team(message):
    bot.send_message(message.chat.id, 'Сделана самой дружной командой \n 👩‍💻 - Alina D дизайнер \n 👩‍🎤 - Madina D муза \n👨‍⚖️ - Andrei K душа \n🤴  - Ali T капитан \n ')

def distance(lat,lon):
    cx = 51.1493317 #широта
    cy = 71.37946940000006 #долгота
    result=""
    is_here=False

    mx = abs(lat - cx)
    my = abs(lon - cy)

    dist = (mx ** 2 + my ** 2) ** 0.5
    min_dist = 0.2 #60 м
    dist=dist*100
    if dist<=min_dist:
        result="Красавчик. Ты успел!"
        is_here=True
    elif dist>min_dist:
        result="Самат за тобой выехал!\n"+"Ты находишься в "+str(dist)[0:4]+" км от универа"
    return result,is_here

def add_user(first,name,last,user_id,attend):
    c.execute("INSERT INTO users (first_name,username,last_name,user_id,attend) VALUES ('%s','%s','%s','%s','%s')"%(first,name,last,user_id,attend))
    conn.commit()


bot.polling(none_stop=True, interval=0)