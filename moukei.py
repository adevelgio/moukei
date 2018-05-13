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
    phrase = self.data.phraseForKeyword(update.message.text)
    if isinstance(phrase, str) and phrase:
      bot.send_message(chat_id=update.message.chat_id, text=phrase)

    if update.message.text == 'Расписание':
      self.showShedule(bot, update)
    elif update.message.text == 'Правила':
      self.showMenuRules(bot, update)
    elif update.message.text == 'назад':
      self.showMenu0(bot, update)
    elif not phrase:
      try:
        bot.send_message(chat_id=chat, text="Когда-то я смогу понять, что тебе нужно... ")
        showMenu0(bot, update)
      except:
        pass
 
  def showMenu0(self, bot, update):
    custom_keyboard = [['Правила', 'Штрафбат'], ['Расписание', 'Связь']]
    reply_markup = ReplyKeyboardMarkup(keyboard=custom_keyboard, resize_keyboard=True)
    try:
      bot.send_message(chat_id=update.message.chat_id, text="Гильдия Mou Kei приветствует тебя!", reply_markup=reply_markup)
    except:
      pass
 
  def showMenuRules(self, bot, update):
    custom_keyboard = [['Правила ГИ'], ['Яма', 'Танк'], ['ТБ', 'ВГ'], ['назад']]
    reply_markup = ReplyKeyboardMarkup(keyboard=custom_keyboard, resize_keyboard=True)
    try:
      bot.send_message(chat_id=update.message.chat_id, text="Выбери интересующий раздел правил", reply_markup=reply_markup)
    except:
      pass

  def showShedule(self, bot, update):
    self.raidReminder.shedule(bot, update)
