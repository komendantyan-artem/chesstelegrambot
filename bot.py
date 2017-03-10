# -*- coding: utf-8 -*-

import config
import telebot
from chess.game import Game

game = None
bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, '''
Введите /start white или /start black чтобы начать игру за соответствующий цвет.
Введите /stop чтобы закончить начатую игру
Во время игры ходы передаются в формате /move 'поле, где стоит фигура', 'поле куда идет фигура' и опционально 'в какую фигуру превращается пешка'
Например,
/move e2e4
/move g1f3
Для короткой рокировки
/move e1g1
Для превращения пешки
/move g7h8q
/move e7f8r
/move e7f8b
/move e7f8n
Вводить ход можно прописными и заглавными буквами с любым количеством пробелов''')


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