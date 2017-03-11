# -*- coding: utf-8 -*-

import config
import telebot
from chess.game import Game
from collections import defaultdict

games = defaultdict(lambda: None)
bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["help"])
def help(message):
    with open("help.txt") as help:
        bot.send_message(message.chat.id, help.read())

@bot.message_handler(commands=["stop"])  
def stop(message):
    if games[message.chat.id]:
        games[message.chat.id] = None
        bot.send_message(message.chat.id, "Игра остановлена")
    else:
        bot.send_message(message.chat.id, "Игра не начиналась")

@bot.message_handler(commands=["start"])
def start(message):
    if games[message.chat.id]:
        bot.send_message(message.chat.id, "Вы не можете начать новую игру пока идет старая")
    elif message.text.split() == ["/start", "white"]:
        games[message.chat.id] = Game("white")
        output_board(message.chat.id, games[message.chat.id].start_game())
    elif message.text.split() == ["/start", "black"]:
        games[message.chat.id] = Game("black")
        output_board(message.chat.id, games[message.chat.id].start_game())
    else:
        bot.send_message(message.chat.id, "Неправильный формат ввода. Введите /help если вам нужна помощь")
        
@bot.message_handler(commands=["move"])
def move(message):
    game = games[message.chat.id]
    if not game:
        bot.send_message(message.chat.id, "Игра еще не начата")
        return
    output_board(message.chat.id, game.step(message.text[5:]))
    if game.get_end_verdict():
        bot.send_message(message.chat.id, game.get_end_verdict())
        games[message.chat.id] = None
        
def output_board(chat_id, fens):
    if isinstance(fens, str):
        bot.send_message(chat_id, fens)
        return
    for fen in fens:
        link = "http://kasparovchess.crestbook.com/extensions/chess_diagram/gendiag.php?fen={0}".format(fen)
        answer = '<a href="{0}">.</a>'.format(link)
        bot.send_message(chat_id, answer, parse_mode="HTML")


if __name__ == '__main__':
    bot.polling(none_stop=True)
