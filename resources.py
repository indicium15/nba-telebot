import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table

def url_name(name):
    split = name.lower().split(' ')
    return('https://www.basketball-reference.com/players/'+split[1][0]+'/'+split[1][0:5]+split[0][0:2]+'01.html')

def get_player_stats(input):
    if ',' in input:
        split = input.split(',')
        player = split[0]
        year = split[1].strip(' ')
    else:
        player = input
        year = 2021
    print(player)
    print(year)
    try:
        URL = url_name(player)
        print(URL)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        soup.find_all('tr', limit =2)
        stat_names = [th.getText() for th in soup.findAll('tr',limit=2)[0].findAll('th')]
        print(stat_names)
        year_filter = 'per_game.'+ str(year)
        stat_values = [tr.getText() for tr in soup.find('tr', attrs={'id':year_filter})]
        print(stat_values)
        reply = ""
        for i in range(len(stat_names)):
            reply += str(stat_names[i]) + ":" +str(stat_values[i]) + "\n"
        print(reply)
        return reply        
    except TypeError:
        reply = "Error: You may have entered a year in which {} was not active. Please try again.".format(player)
        print(reply)
        return reply
