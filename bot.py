# -*- coding: utf-8 -*-

import config
import telebot
from chess.game import Game
from collections import defaultdict

games = defaultdict(lambda: None)
busy = defaultdict(lambda: False)
bot = telebot.TeleBot(config.token)

def busy_handler(f):
    def result(message):
        if busy[message.chat.id]:
            return
        busy[message.chat.id] = True
        f(message)
        busy[message.chat.id] = False
    return result


@bot.message_handler(commands=["help"])
@busy_handler
def help(message):
    with open("help.txt") as help:
        bot.send_message(message.chat.id, help.read())


@bot.message_handler(commands=["stop"])
@busy_handler
def stop(message):
    if games[message.chat.id]:
        games[message.chat.id] = None
        bot.send_message(message.chat.id, "Игра остановлена")
    else:
        bot.send_message(message.chat.id, "Игра не начиналась")


@bot.message_handler(commands=["start"])
@busy_handler
def start(message):
    text = ''.join(message.text.lower().split()[1:])
    if games[message.chat.id]:
        bot.send_message(message.chat.id, "Вы не можете начать новую игру пока идет старая")
    elif text == "white":
        games[message.chat.id] = Game("white")
        output_board(message.chat.id, games[message.chat.id].start_game())
    elif text == "black":
        games[message.chat.id] = Game("black")
        output_board(message.chat.id, games[message.chat.id].start_game())
    else:
        bot.send_message(message.chat.id, "Неправильный формат ввода. Введите /help если вам нужна помощь")


@bot.message_handler(commands=["move"])
@busy_handler
def move(message):
    game = games[message.chat.id]
    if not game:
        bot.send_message(message.chat.id, "Игра еще не начата")
        return
    string = ''.join(message.text.split()[1:])
    if game.string_to_move(string):
        bot.send_message(message.chat.id, "Ваш ход принят")
    output_board(message.chat.id, game.step(string))
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
