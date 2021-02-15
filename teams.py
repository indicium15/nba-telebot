from bs4 import BeautifulSoup
import requests

def get_standings(conference_id):
    """Returns list of conference standings from Basketball Reference
    args - conference_id - table id for eastern/western conference"""
    output = ""
    if conference_id == 'div_confs_standings_E':
        output = "```\nEastern Conference\n"
    if conference_id == 'div_confs_standings_W':
        output = "```\nWestern Conference\n"
    page = requests.get('https://www.basketball-reference.com/')
    soup = BeautifulSoup(page.content, 'html.parser')
    standings = soup.find('div',attrs={'id': conference_id})
    team_names = [th.get_text(strip=True) for th in standings.find_all('th',attrs={'class':'left'})]
    team_names.pop(0) #Remove 'East', 'West'
    wins = [td.get_text() for td in standings.find_all('td',attrs={'data-stat':'wins'})]
    losses = [td.get_text() for td in standings.find_all('td',attrs={'data-stat':'losses'})]
    for i in range(len(team_names)):
        output += '{:<8}{:^2}{:>5}\n'.format(team_names[i].strip(),'|',wins[i].strip()+'-'+losses[i].strip())
    output += '```\n' 
    print(output)
    return output

def league_query(arg):
    """Parses user query to determine which conference standings to be scraped from Basketball Reference.
    args: arg - Eastern / Western Conferences. Returns both conferences if not defined"""
    result = None
    query = arg.lstrip('/standings ')
    query = query.lower()
    if query == "e" or query == "eastern" or query == "east":
        result = get_standings('div_confs_standings_E')
    elif query == "w" or query == "western" or query == "west":
        result = get_standings('div_confs_standings_W')
    elif query == "":
        result = get_standings('div_confs_standings_E') + '\n' + get_standings('div_confs_standings_W')
    return result
