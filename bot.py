# -*- coding: utf-8 -*-

import config
import telebot
from chess.game import Game

game = None
bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=["help"])
def help(message):
    with open("help.txt") as help:
        bot.send_message(message.chat.id, help.read())


@bot.message_handler(commands=["stop"])  
def stop(message):
    global game
    if game:
        game = None
        bot.send_message(message.chat.id, "Игра остановлена")
    else:
        bot.send_message(message.chat.id, "Игра не начиналась")

@bot.message_handler(commands=["start"])
def start(message):
    global game
    if game:
        bot.send_message(message.chat.id, "Вы не можете начать новую игру пока идет старая")
    elif message.text.split() == ["/start", "white"]:
        game = Game("white")
        output_board(message.chat.id, game.start_game())
    elif message.text.split() == ["/start", "black"]:
        game = Game("black")
        output_board(message.chat.id, game.start_game())
    else:
        bot.send_message(message.chat.id, "Неправильный формат ввода. Введите /help если вам нужна помощь")
        
@bot.message_handler(commands=["move"])
def move(message):
    global game
    if not game:
        bot.send_message(message.chat.id, "Игра еще не начата")
        return
    output_board(message.chat.id, game.step(message.text[5:]))
    if game.get_end_verdict():
        bot.send_message(message.chat.id, game.get_end_verdict())
        game = None
        
def output_board(chat_id, boards):
    bot.send_message(chat_id, '\n\n'.join(boards))

if __name__ == '__main__':
     bot.polling(none_stop=True)
