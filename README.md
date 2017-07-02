# Telegram-Attendance-Bot
Telegram Bot on Python 3.6 for classroom attendance check
Featuring:
  - 2 leveled check scheme:
      1. By Geolocation
      2. By any secret word provided
  - SQlite 3 Data Base integrated (table users:first_name,username,last_name,user_id,attendance_counter)
  - Distance calculation (if user is in classroom radius of 50 meters)
  - Attendance calculation in percents (result=attendance_counter/( (today-start_day) - (today-start_day)/6))
Libraries required:
  telebot
  datetime
  sqlite3
