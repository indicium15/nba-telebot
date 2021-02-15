from bs4 import BeautifulSoup
import requests
import re

def get_player_stats(url,year=2021):
    """Returns player's stats scraped from their Basketball-Reference player page for the specified year.
    args - url - url of player's basketball reference page
    year - season / year to scrape stats for"""
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        soup.find_all('tr', limit =2)
        stat_names = [th.getText() for th in soup.findAll('tr',limit=2)[0].findAll('th')]
        year_filter = 'per_game.'+ str(year) #Find table rows with stats for specified year
        stat_values = [tr.getText() for tr in soup.find('tr', attrs={'id':year_filter})]
        player_name = soup.find('h1',attrs={'itemprop':'name'})
        stats_dict = {}
        for i in range(len(stat_names)):
            stats_dict[stat_names[i]] = stat_values[i]
        reply = "*Stats for {0} in {1}: {2}*".format(player_name.getText().strip(),year,'\n')
        reply += '{:<6}'.format('Age : ') + '{:^2}'.format(stats_dict['Age'])+'\n'
        reply += '{:<17}'.format('Team, Position : ') + '{:^3},'.format(stats_dict['Tm']) +  ' {:^2}'.format(stats_dict['Pos']) + '\n'
        reply += '{:<14}'.format('GP, GS, MPG : ') + ' {:^2},'.format(stats_dict['G']) + ' {:^2},'.format(stats_dict['GS']) + ' {:^4}'.format(stats_dict['MP']) + '\n\n'
        reply += '*Overview*:\n'
        reply += '{:<6}'.format('PTS : ') + '{:^4}'.format(stats_dict['PTS'])+'\n'
        reply += '{:<6}'.format('AST : ') + '{:^4}'.format(stats_dict['AST'])+'\n'
        reply += '{:<6}'.format('REB : ') + '{:^4}'.format(stats_dict['TRB'])+'\n'
        reply += '{:<6}'.format('TOV : ') + '{:^4}'.format(stats_dict['TOV'])+'\n\n'
        reply += '*Shooting*:\n'
        reply += '{:<15}'.format('FG, FGA, FG% : ') + '{:^4},'.format(stats_dict['FG']) + ' {:^4},'.format(stats_dict['FGA']) + ' {:^4}'.format(stats_dict['FG%'])+'\n'
        reply += '{:<15}'.format('2P, 2PA, 2P% : ') + '{:^4},'.format(stats_dict['2P']) + ' {:^4},'.format(stats_dict['2PA']) + ' {:^4}'.format(stats_dict['2P%'])+'\n'
        reply += '{:<15}'.format('3P, 3PA, 3P% : ') + '{:^4},'.format(stats_dict['3P']) + ' {:^4},'.format(stats_dict['3PA']) + ' {:^4}'.format(stats_dict['3P%'])+'\n'
        reply += '{:<15}'.format('FT, FTA, FT% : ') + '{:^4},'.format(stats_dict['FT']) + ' {:^4},'.format(stats_dict['FTA']) + ' {:^4}'.format(stats_dict['FT%'])+'\n'
        reply += '{:<7}'.format('EFG% : ') + '{:^4}'.format(stats_dict['eFG%'])+'\n\n'
        reply += '*Rebounding*:\n'
        reply += '{:<11}'.format('ORB, DRB : ') +  '{:^4},'.format(stats_dict['ORB']) + ' {:^4}'.format(stats_dict['DRB'])+'\n\n'
        reply += '*Defensive*:\n'
        reply += '{:<15}'.format('STL, BLK, PF : ') + '{:^4},'.format(stats_dict['STL']) + ' {:^4},'.format(stats_dict['BLK']) + ' {:^4}'.format(stats_dict['PF'])+'\n'       
        print(reply)
        return reply      
    
    except TypeError: #Player was not active in current year, ask user to refine search
        reply = "Error: You may have entered a year in which this player was not active. Player's active years are:\n"
        active_years = [th.getText() for th in soup.findAll('th',attrs={'data-stat':'season'})]
        active_years.remove('Career')
        active_years.remove('Season')
        for i in active_years:
            if i == "":
                active_years.remove('')
            else:
                reply += i + '\n'
        print(active_years)               
        print(reply)
        return reply

def player_query(input):
    """Parses user input from Telegram to determine arguments for get_player_stats.
    args - input - user input."""
    stripped_input = input.lstrip('/playerstats ')
    parsed_input = stripped_input.split(',')
    print(parsed_input, stripped_input)
    
    if len(parsed_input) == 1:
        text = parsed_input[0]
        year = 2021
    if len(parsed_input) == 2:
        text = parsed_input[0]
        year = int(parsed_input[1])
    print(text, year)
    url = 'https://www.basketball-reference.com/search/search.fcgi?search='
    split = text.lower().split(' ')
    if len(split) == 1:
         url + split[0] #Creating URL to access Basketball Reference search page
    print(split)
    if len(split) >= 1: 
        for i in range(len(split)):
            url += split[i] + '+'
    page = requests.get(url) #Accessing search url
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        is_search = soup.find('h1') #Check to see if cursor has landed on search page
        if is_search.text == "Search Results":
            page = requests.get(url)
            results = {}
            player_name = soup.find_all('div',attrs={'class':'search-item-name'})
            for player in player_name:
                link = player.find('a', href=True)
                name = player.find('a').contents[0]
                modified_name = re.sub(r"\([^()]*\)",'',name).strip()
                if 'international' in link['href']:
                    pass
                elif 'gleague' in link['href']:
                    pass
                else:
                    results[modified_name] = link['href']
                    
            if len(results) == 1: #Only one search result
                for value in results.values():
                    new_url = 'https://www.basketball-reference.com' + value
                    print(new_url)
                    return get_player_stats(new_url,year)

            if len(results) in range(1,11): #Between 1-10 search results - worth looking for a match
                for key in results.keys(): #TODO: Present user with a list of players for them to choose from
                    if text.lower() in key.lower():
                        new_url = 'https://www.basketball-reference.com' + results[key]
                        print(new_url)
                        return get_player_stats(new_url,year)
                    else:
                        pass
            
            if len(results) >=10: #Too many search results - ask user to redefine query w/suggestions
                key_list = [key for key in results.keys()]
                output = "Your query generated too many results. Were you looking for:\n"
                for i in range(0,11):
                    output += key_list[i] + '\n'
                print(output)
                return(output)
        else: #Check to see if cursor has automatically been redirected to player page
            is_player = soup.find('div',attrs={'class':'media-item'})
            if 'players' in (is_player.find('img')['src']):
                return get_player_stats(url,year)
            else:
                pass
    else: #Connection not established
        reply = "An error has occured. Please try again."
        print(reply)
        return reply


