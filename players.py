from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats, playerdashboardbyyearoveryear

def get_player_id(name):
    results = players.find_players_by_full_name(str(name))
    print(results)
    print(len(results))
    if len(results) == 0:
        return('Sorry, we were unable to find the player you were looking for. Please try again.')
    elif len(results) == 1:
        #Only one result found for the player search
        player_id = results[0]['id']
        print(player_id)
        return player_id
    elif len(results) > 1:
        output = 'Your query generated too many results. Were you looking for:\n'
        for player in results:
            output += player['full_name']
            print(output)
            return(output) 

def get_player_name(id):
    try:
        results = players.find_player_by_id(int(id))
        print(results['full_name'])
        return(results['full_name'])
    except:
        print('An error has occured, please try again.')

#TODO: Add Default Season String
def season_stats_lookup(id, season='2020-21'):
    stats = playerdashboardbyyearoveryear.PlayerDashboardByYearOverYear(player_id=id,season=season,per_mode_detailed='PerGame')
    dict = stats.overall_player_dashboard.get_dict()
    #Debugging
    print(dict)
    reply = "*Stats for {} in {}*\n".format(get_player_name(id),dict['data'][0][1])
    reply += "{:<9}".format('GP, MPG : ') + "{:^2}, ".format(dict['data'][0][5]) + "{:^2}".format(dict['data'][0][9]) + "\n\n"
    reply += '*Overview*:\n'
    reply += '{:<6}'.format('PTS : ') + '{:^4}'.format(dict['data'][0][29])+'\n'
    reply += '{:<6}'.format('AST : ') + '{:^4}'.format(dict['data'][0][22])+'\n'
    reply += '{:<6}'.format('REB : ') + '{:^4}'.format(dict['data'][0][21])+'\n'
    reply += '{:<6}'.format('TOV : ') + '{:^4}'.format(dict['data'][0][23])+'\n\n'
    reply += '*Shooting*:\n'
    reply += '{:<15}'.format('FG, FGA, FG% : ') + '{:^4},'.format(dict['data'][0][10]) + ' {:^4},'.format(dict['data'][0][11]) + ' {:^4.1%}'.format(dict['data'][0][12])+'\n'
    reply += '{:<15}'.format('3P, 3PA, 3P% : ') + '{:^4},'.format(dict['data'][0][13]) + ' {:^4},'.format(dict['data'][0][14]) + ' {:^4.1%}'.format(dict['data'][0][15])+'\n'
    reply += '{:<15}'.format('FT, FTA, FT% : ') + '{:^4},'.format(dict['data'][0][16]) + ' {:^4},'.format(dict['data'][0][17]) + ' {:^4.1%}'.format(dict['data'][0][18])+'\n\n'
    reply += '*Rebounding*:\n'
    reply += '{:<11}'.format('ORB, DRB : ') +  '{:^4},'.format(dict['data'][0][19]) + ' {:^4}'.format(dict['data'][0][20])+'\n\n'
    reply += '*Defensive*:\n'
    reply += '{:<15}'.format('STL, BLK, PF : ') + '{:^4},'.format(dict['data'][0][24]) + ' {:^4},'.format(dict['data'][0][25]) + ' {:^4}'.format(dict['data'][0][27])+'\n'   
    print(reply)
    return(reply)

#TODO: Add Default Season String
def get_season_stats(name, season='2020-21'):
    try:
        id = get_player_id(name)
        response = season_stats_lookup(id,season)
        return(response)
    except:
        return("An error has occured. Please try again.")

def career_stats_lookup(id):
    stats = playercareerstats.PlayerCareerStats(per_mode36='PerGame',player_id=id)
    dict = stats.career_totals_regular_season.get_dict()
    print(dict)
    reply = "*Career Stats for {}*\n".format(get_player_name(id))
    reply += "{:<9}".format('GP, MPG :') + "{:^2}, ".format(dict['data'][0][3]) + "{:^2}".format(dict['data'][0][5]) + "\n\n"
    reply += '*Overview*:\n'
    reply += '{:<6}'.format('PTS : ') + '{:^4}'.format(dict['data'][0][23])+'\n'
    reply += '{:<6}'.format('AST : ') + '{:^4}'.format(dict['data'][0][18])+'\n'
    reply += '{:<6}'.format('REB : ') + '{:^4}'.format(dict['data'][0][17])+'\n'
    reply += '{:<6}'.format('TOV : ') + '{:^4}'.format(dict['data'][0][21])+'\n\n'
    reply += '*Shooting*:\n'
    reply += '{:<15}'.format('FG, FGA, FG% : ') + '{:^4},'.format(dict['data'][0][6]) + ' {:^4},'.format(dict['data'][0][7]) + ' {:^4.1%}'.format(dict['data'][0][8])+'\n'
    reply += '{:<15}'.format('3P, 3PA, 3P% : ') + '{:^4},'.format(dict['data'][0][9]) + ' {:^4},'.format(dict['data'][0][10]) + ' {:^4.1%}'.format(dict['data'][0][11])+'\n'
    reply += '{:<15}'.format('FT, FTA, FT% : ') + '{:^4},'.format(dict['data'][0][12]) + ' {:^4},'.format(dict['data'][0][13]) + ' {:^4.1%}'.format(dict['data'][0][14])+'\n\n'
    reply += '*Rebounding*:\n'
    reply += '{:<11}'.format('ORB, DRB : ') +  '{:^4},'.format(dict['data'][0][15]) + ' {:^4}'.format(dict['data'][0][16])+'\n\n'
    reply += '*Defensive*:\n'
    reply += '{:<15}'.format('STL, BLK, PF : ') + '{:^4},'.format(dict['data'][0][19]) + ' {:^4},'.format(dict['data'][0][20]) + ' {:^4}'.format(dict['data'][0][22])+'\n'
    print(reply)
    return(reply)    

def get_career_stats(name, season='2020-21'):
    try:
        id = get_player_id(name)
        response = career_stats_lookup(id)
        return(response)
    except:
        return("An error has occured. Please try again.")

#Debugging
#get_season_stats('Lonzo Ball','2020-21')
#get_career_stats('Lonzo Ball','2020-21')