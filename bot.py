from keys import api_key
import telebot
import datetime
from players import player_query
from teams import league_query 
from games import get_games

bot = telebot.TeleBot(api_key, parse_mode=None)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hi, I'm the NBA Statistics Bot!\nType /help for a list of commands")

@bot.message_handler(commands=['help'])
def send_help(message):
    output = "*Command List*\n1./playerstats player, year\nReturns a player's stats for a season from Basketball Reference.\n\n2./standings conference \nReturns the standings for the specified conference. Returns both conference standings if not mentioned\n\n3./games\nReturns a list of NBA games being played today with live scores and links to box scores from nba.com."
    bot.reply_to(message, output, parse_mode='MARKDOWN')

@bot.message_handler(commands=['playerstats'])
def player_stats(message):
    output = player_query(message.text)
    bot.send_message(message.chat_id, output, parse_mode='MARKDOWN')

@bot.message_handler(commands=['standings'])
def standings(message):
    output = league_query(message.text)
    bot.send_message(message.chat.id, output, parse_mode='MARKDOWN')

@bot.message_handler(commands=['games'])
def games(message):
    output = get_games()
    bot.send_message(message.chat.id, output, parse_mode='MARKDOWN',disable_web_page_preview=True)
   
bot.polling()
