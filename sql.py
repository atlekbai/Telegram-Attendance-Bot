import sqlite3
#Подключение к базе
conn = sqlite3.connect('my.db')
#Создание курсора
c = conn.cursor()
#Создание таблицы
c.execute('''CREATE TABLE users (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            first_name varchar, 
            username varchar,
            last_name varchar,
            user_id varchar,
            attend int)''')
#Наполнение таблицы
c.execute("INSERT INTO users (first_name,username,last_name,user_id,attend) VALUES ('Ali','Jango','Tlekbai','01111','1')")
#Подтверждение отправки данных в базу
conn.commit()
#Завершение соединения
c.close()
conn.close()