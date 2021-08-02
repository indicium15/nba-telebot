from telebot.types import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from keys import api_key
import telebot
#New Functions Written with nba_api
from players import get_season_stats, get_career_stats
from league import get_league_standings
from teams import get_team_stats
#Old Functions to Rewrite
#TODO: Rewrite Injury Function
#TODO: Rewrite Games and News Functions
from games import get_games, get_news

#Initialise Bot
bot = telebot.TeleBot(api_key, parse_mode=None)
#Bot Commands
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hi, I'm the NBA Statistics Bot!\nType /help for a list of commands")

@bot.message_handler(commands=['help'])
def send_help(message):
    output = "*Command List*\n1./playerstats player, year\nReturns a player's stats for the current NBA Season.\n\n2./standings conference \nReturns the standings for the specified conference. Returns both conference standings if not mentioned\n\n3./games\nReturns a list of NBA games being played today with live scores and links to box scores from nba.com."
    bot.reply_to(message, output, parse_mode='MARKDOWN')

@bot.message_handler(commands=['playerstats'])
def playerstats(message):
    output = get_season_stats(message.text.lstrip('/playerstats '))
    bot.reply_to(message, output, parse_mode='MARKDOWN')

@bot.message_handler(commands=['careerstats'])
def career_stats(message):
    output = get_career_stats(message.text.lstrip('/careerstats '))
    bot.reply_to(message, output, parse_mode='MARKDOWN')

@bot.message_handler(commands=['standings'])
def standings(message):
    output = get_league_standings(message.text.lstrip('/standings '))
    bot.send_message(message.chat.id, output, parse_mode='MARKDOWN')

@bot.message_handler(commands=['games'])
def games(message):
    output = get_games()
    bot.send_message(message.chat.id, output, parse_mode='MARKDOWN',disable_web_page_preview=True)

@bot.message_handler(commands=['teamstats'])
def teamstats(message):
    output = get_team_stats(message.text.lstrip('/teamstats '))
    bot.send_message(message.chat.id, output, parse_mode='MARKDOWN')

@bot.message_handler(commands=['news'])
def news(message):
    output = get_news()
    bot.send_message(message.chat.id, output, parse_mode='MARKDOWN',disable_web_page_preview=True)

# @bot.message_handler(commands=['injuries'])
# def injuries(message):
#     output = parse_injuries(message.text.lstrip('/injuries '))
#     bot.send_message(message.chat.id, output, parse_mode='MARKDOWN')

# @bot.message_handler(commands=['test'])
# def test(message):
#     pass

#Polling - Look for Commands
bot.polling()
