from bs4 import BeautifulSoup
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from keys import chromedriver_path

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

def get_team_stats(url):
    """Function to scrape basic information about a team (stat overview, team leaders and injuries, if any) from an NBA team's ESPN website.
    args: url - ESPN url website to scrape data from"""
    options = Options()
    options.headless = True
    output = ""
    driver = webdriver.Chrome(chromedriver_path, chrome_options=options)  
    driver.get(url)
    time.sleep(3)
    team_name = driver.find_element_by_xpath('//h1[@class="ClubhouseHeader__Name"]').get_attribute('innerText').split('\n')
    output += '*{} {}*\n'.format(team_name[0],team_name[1])
    team_record = driver.find_element_by_xpath('//ul[@class="ClubhouseHeader__Record"]').text
    output += 'Record: {}\n\n'.format(team_record)
    time.sleep(1)
    team_stats = [i.get_attribute('innerText') for i in driver.find_elements_by_xpath('//span[@class="number"]')]
    output += '*Team Stat Overview:*\nPoints Per Game: {}\nRebounds Per Game: {}\nAssists Per Game: {}\nPoints Allowed Per Game: {}\n\n*Team Leaders:*\n'.format(team_stats[0],team_stats[1],team_stats[2],team_stats[3])
    stat_name_dict = {
            0:'Points Per Game',
            1:'Assists Per Game',
            2:'Field Goal %',
            3:'Rebounds Per Game',
            4:'Steals Per Game',
            5:'Blocks Per Game'
        }
    time.sleep(1)
    team_leaders = driver.find_elements_by_xpath('//div[@class="content-meta"]') #Scrape leading scorers
    for i in range(0,6): #Six categories of leading scoreres on ESPN
        player_name = team_leaders[i].find_element_by_name('&lpos=nba:teamclubhouse:performers:player').get_attribute('innerText')
        stat_value = team_leaders[i].find_element_by_class_name('number').get_attribute('innerText')
        stat_name = stat_name_dict[i]
        output += '{}: {} ({})\n'.format(stat_name, player_name, stat_value)
    try: #Try looking for injury section on website 
        team_injuries = driver.find_element_by_xpath('//article[@class="sub-module"]') #Look for injured players and add to output string
        injured_players = team_injuries.find_elements_by_class_name('content-meta')
        output += '\n*Injuries:*\n'
        for player in injured_players:
            player_name = player.find_element_by_name('&lpos=nba:teamclubhouse:injuries:player').get_attribute('innerText')
            player_status = player.find_element_by_tag_name('p').get_attribute('innerText')
            output += '{}({})\n'.format(player_name,player_status)
    except NoSuchElementException: #Team has no injuries, do not add to output string
        pass
    driver.close()
    print(output)
    return output
    
def team_query(input):
    """Parses user query from telegram and passes the url to scrape data from to get_team_stats if a match is found.
    args - input - user input from telegram chat"""
    parsed_input = input.lstrip('/teamstats ')
    team_url_dict = { #Dictionary of team names and their corresponding ESPN URLs
        'boston celtics,bos':'https://www.espn.com.sg/nba/team/_/name/bos/boston-celtics',
        'brooklyn nets,bkn':'https://www.espn.com.sg/nba/team/_/name/bkn/brooklyn-nets',
        'new york knicks,nyk':'https://www.espn.com.sg/nba/team/_/name/ny/new-york-knicks',
        'toronto raptors,tor':'https://www.espn.com.sg/nba/team/_/name/tor/toronto-raptors',
        'golden state warriors,gsw':'https://www.espn.com.sg/nba/team/_/name/gs/golden-state-warriors',
        'los angeles clippers,lac':'https://www.espn.com.sg/nba/team/_/name/lac/la-clippers',
        'phoenix suns,phx':'https://www.espn.com.sg/nba/team/_/name/phx/phoenix-suns',
        'sacramento kings,sac':'https://www.espn.com.sg/nba/team/_/name/sac/sacramento-kings',
        'denver nuggets,den':'https://www.espn.com.sg/nba/team/_/name/den/denver-nuggets',
        'minnesota timberwolves,min':'https://www.espn.com.sg/nba/team/_/name/min/minnesota-timberwolves',
        'oklahoma city thunder,okc':'https://www.espn.com.sg/nba/team/_/name/okc/oklahoma-city-thunder',
        'utah jazz,uta':'https://www.espn.com.sg/nba/team/_/name/utah/utah-jazz',
        'dallas mavericks,dal':'https://www.espn.com.sg/nba/team/_/name/dal/dallas-mavericks',
        'houston rockets,hou':'https://www.espn.com.sg/nba/team/_/name/hou/houston-rockets',
        'memphis grizzlies,mem':'https://www.espn.com.sg/nba/team/_/name/mem/memphis-grizzlies',
        'new orleans pelicans,nol':'https://www.espn.com.sg/nba/team/_/name/no/new-orleans-pelicans',
        'san antonio spurs,sas':'https://www.espn.com.sg/nba/team/_/name/sa/san-antonio-spurs'
    }
    res = [val for key, val in team_url_dict.items() if parsed_input.lower() in key] #Look for partial match in key from user input.
    if len(res) > 1: #Too many results
        output = 'Sorry, your query generated too many responses. Please try again.'
        print(output)
        return(output)
    elif len(res) == 0: #No match found
        output = 'Sorry, we were unable to find the team you are looking for. Please try again.'
        print(output)
        return(output)
    elif len(res) == 1: #One result, proceed with scraping data
        url = str(res[0])
        print(url)
        return(get_team_stats(url))
