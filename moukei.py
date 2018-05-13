# -*- coding: utf-8 -*-
# @swgoh_moukei_bot

import os
import logging
from telegram import ReplyKeyboardMarkup #, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler
import guild_raid
import storage
import types

class Bot:
  def __init__(self):
    self.data = storage.Data()

    self.updater = Updater(token=os.environ['BOT_TOKEN'])
    self.dispatcher = self.updater.dispatcher
    self.raidReminder = guild_raid.Reminder(self.updater, self.data)
    self.dispatcher.add_handler(CommandHandler('start', self.newUser))
    self.dispatcher.add_handler(
        CommandHandler('raids', self.raidReminder.diag))

    msg_handler = MessageHandler(Filters.text, self.messageReceived)
    self.dispatcher.add_handler(msg_handler)

  def run(self):
    self.updater.start_polling() 
    self.updater.idle()

  def newUser(self, bot, update): 
    print("new user!")
    chat = update.message.chat_id
    print("new user chat %d!" % chat)
    self.data.addUser(update.effective_user, chat)

    try:
      bot.send_message(chat_id=chat, text="Привет! Я служу гильдии Mou Kei, буду напоминать тебе о выжных событиях!")
    except:
      pass
 
    self.showMenu0(bot, update)

  def messageReceived(self, bot, update):
    print("received string: %s!" % update.message.text)
    chat = update.message.chat_id
    print("try get phrase!")
    phrase = self.data.phraseForKeyword(update.message.text)
    print("find phrase: %s!" % phrase)
    if isinstance(phrase, str) and phrase:
      bot.send_message(chat_id=update.message.chat_id, text=phrase)
    print("continue handling...")

    if update.message.text == 'Штрафбат':
      self.showJail(bot, update)
    elif update.message.text == 'Расписание':
      self.showShedule(bot, update)
    elif update.message.text == 'Связь':
      self.showContact(bot, update)
    elif update.message.text == 'Правила':
      self.showMenuRules(bot, update)
    elif update.message.text == 'Правила ГИ':
      self.showGuildRules(bot, update)
    elif update.message.text == 'Яма':
      self.showRankorRules(bot, update)
    elif update.message.text == 'Танк':
      self.showTankRules(bot, update)
    elif update.message.text == 'ТБ':
      self.showTBRules(bot, update)
    elif update.message.text == 'ВГ':
      self.showGWRules(bot, update)
    elif update.message.text == 'назад':
      self.showMenu0(bot, update)
    else:
      try:
        bot.send_message(chat_id=chat, text="Когда-то я смогу понять, что тебе нужно... ")
        showMenu0(bot, update)
      except:
        pass
 
  def showMenu0(self, bot, update):
    #custom_keyboard = [['Руководство', 'Правила'], ['bottom-left', 'bottom-right']]
    custom_keyboard = [['Правила', 'Штрафбат'], ['Расписание', 'Связь']]
    reply_markup = ReplyKeyboardMarkup(keyboard=custom_keyboard, resize_keyboard=True)
    try:
      bot.send_message(chat_id=update.message.chat_id, text="Гильдия Mou Kei приветствует тебя!", reply_markup=reply_markup)
    except:
      pass
 
  def showMenuRules(self, bot, update):
    #custom_keyboard = [['Руководство', 'Правила'], ['bottom-left', 'bottom-right']]
    custom_keyboard = [['Правила ГИ'], ['Яма', 'Танк'], ['ТБ', 'ВГ'], ['назад']]
    reply_markup = ReplyKeyboardMarkup(keyboard=custom_keyboard, resize_keyboard=True)
    try:
      bot.send_message(chat_id=update.message.chat_id, text="Выбери интересующий раздел правил", reply_markup=reply_markup)
    except:
      pass

  def showGuildRules(self, bot, update):
    try:
      bot.send_message(chat_id=update.message.chat_id, text= """‼️‼️ГЛАВНОЕ ПРАВИЛО:  В ГИ КАЖДЫЙ ДЕНЬ ДОЛЖНО БЫТЬ 30К КУПОНОВ В ДЕНЬ‼️‼️
ТЕПЕРЬ НАС ПОКАЗЫВАЮТ ПО ТВ В ИГРЕ, ТАК ЧТО ПРОДОЛЖАЕМ В ТОМ ЖЕ ДУХЕ!!!💪🏻✊🏻

‼️‼️САМОЕ ПРИ САМОЕ ГЛАВНОЕ ОТ ВАС - ЭТО СДАВАТЬ 600 ‼️‼️
ДЕЛАЕМ 600 ДО 15-00 МСК, КРАЙНИЙ СРОК 17-30, ЕСЛИ НЕТ 600 К ЭТОМУ СРОКУ, ТО КИКАЕМ ИГРОКА (ВНЕ ЗАВИСИМОСТИ ОТ РЕЙДОВ И ТБ), ЗАВОДИМ ТВИНК ДЛЯ 600, ПОСЛЕ 18-30 ВЕРНЕМ ОБРАТНО.

‼️ПОСЛЕДНЕЕ ПРЕДУПРЕЖДЕНИЕ‼️
Касается тех, у кого до сих пор нет нужных персов на СТБ на спецмиссии, а так же тех, у кого они есть, но игроки просто забивают отыгравать битву. Вашим "пропуском" для получения наград с СТБ теперь будут пройденые спецмиссии, соответственно, если не прошел спецмиссию, то соснул тунца вместо наград. Всё, хватит быть приживалами, или вы тащите на равне со всеми или на хуй с мопеда, у вас было ТРИ МЕСЯЦА блять и это уже выходит за все рамки приличия!!!!""")
    except:
      pass

  def showRankorRules(self, bot, update):
    try:
      bot.send_message(chat_id=update.message.chat_id, text= """Рейд проходится в два дня:
— день первый: 0 урона сразу после открытия, чтобы всем достались награды;
— день второй: ЗЕРГ-РАШ; в указанное время завершается попытка при закрытии до 2х фаз за раз; закрываешь рейд соло — завершаешь попытку на 10 минут позже!

‼️ШТРАФ за закрытие попытки до указанного времени - это запрет на дальнейшее участие в текущем рейде + пропуск 1 рейда Яма и 1 рейда Танк!!!
‼️‼️Если Вы закрыли в Соло Ранкора до назначенного времени, то у вас есть 2 варианта:
1) Отбыть наказание в виде пропуска рейда + Запрет на закрытие в Соло Ранкора в течение недели
2) Давай, До Свидания!👣""")
    except:
      pass

  def showTankRules(self, bot, update):
    try:
      bot.send_message(chat_id=update.message.chat_id, text= """Рейд проходится в два дня:
— день первый: 1 фаза -- сразу после открытия, 2 фаза -- сразу после завершения первой;
— день второй: 12:00 -- 3 фаза; 20:30 -- 4 фаза.

‼️Закрываешь больше 80% фазы или всю фазу соло — завершаешь попытку на 10 минут позже указанного времени‼️

На танк разрешено выполнить один заход, одним паком на каждую фазу, в случае необходимости только офицер может разрешить зайти вторым паком на фазу. На 4 фазе — ЗЕРГ-РАШ

‼️ШРАФ за закрытие попытки на фазе танка до указанного времени это запрет на дальнейшее участие в текущем рейде + пропуск 1 рейда Яма и 1 рейда Танк!!!""")
    except:
      pass

  def showTBRules(self, bot, update):
    try:
      bot.send_message(chat_id=update.message.chat_id, text= """1. После старта фазы в первые 1-2 часа необходимо чтобы все игроки зашли в игру чтобы мы быстро заполнили взводы (радары).
2. Пройти ВСЕ пистолеты на ❗️ВСЕХ❗️ территориях!!!!
3. После того как Вы прошли ВСЕ пистолеты, на ВСЕХ территориях, необходимо заглянуть в канал ТБ https://t.me/TB_Mou_kei, посмотреть куда Вам лично указано высаживаться. В соответствии с таблицами или указаниями — сливайте остатки.

Развертываться нужно только на той территории, которая будет прописана в таблице рядом в вашим именем на канале ТБ, если командующий впоследствии не изменит требование к размешению на этой территории. 
Для этого ВСЕГДА ПЕРЕД СЛИВОМ ПРОВЕРТЕ КАНАЛ ТБ и уточните не было ли дополнительных распоряжений.

Территориальные Битвы
Координация действий при прохождении Территориальных битв https://t.me/TB_Mou_kei""")
    except:
      pass

  def showGWRules(self, bot, update):
    try:
      bot.send_message(chat_id=update.message.chat_id, text="""Чат координации — https://t.me/joinchat/D7yV9UujDh0GC9SRqS3RDQ

1. Подготовить список пачек в виде скринов своих паков в разделе "Выбрать отряд", сделать скрины и во время выставления защитных отрядов сначала показать свои паки командующему ВГ офицеру, чтобы он сказал что и куда от вас надо закинуть для дэфа. 
НЕ ТУПИТЬ!!! Персов в голубом тире в дэф не ставить!!!
2. В атаке рационально используйте свой гараж, дрышей бьем дрыщами, а мощных, соответствено сильными паками.""")
    except:
      pass
  
  def showJail(self, bot, update):
    try:
      bot.send_message(chat_id=update.message.chat_id, text="""=== ШТРАФБАТ ===

🛑 на рейд Танк: 
1)  
2) 
3) 

🛑 на рейд Яма:
1) 
2)  
3)
""")
    except:
      pass

  def showShedule(self, bot, update):
    self.raidReminder.shedule(bot, update)
    
  def showContact(self, bot, update):
    try:
      bot.send_message(chat_id=update.message.chat_id, text="""Глава гильдии - РУС (@Shortrus)

Основной чат — https://t.me/MouKei
Координация ТБ — https://t.me/TB_Mou_kei""")
    except:
      pass

