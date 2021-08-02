from nba_api.stats.endpoints import teamdashboardbyyearoveryear
from nba_api.stats.static import teams

def get_team_id(name):
    results = teams.find_teams_by_full_name(str(name.lower()))
    if len(results) == 1:
        print(results[0]['id'])
        return (results[0]['id'])
    elif len(results) >=1:
        return("Sorry, your query generated too many responses. Please try again.")
    elif len(results) == 0:
        return("Sorry, we couldn't find the team you were looking for. Please try again.")
    else:
        return("An error has occured. Please try again")

def get_team_name(id):
    try:
        #Function will fail on any multiple matches, hence there is no need to verify the length of the results
        search = teams.find_team_name_by_id(int(id)) 
        print(search)
        return(search['full_name'])
    except:
        print("An error has occured. Please try again.")
        return("An error has occured. Please try again.")

def team_stats_lookup(id,season='2020-21'):
    #TODO: Try different measure types - maybe add that as another function
    #TODO: Standardize formatting across messages
    dict = teamdashboardbyyearoveryear.TeamDashboardByYearOverYear(team_id=id,measure_type_detailed_defense='Base',per_mode_detailed='PerGame',season=season).overall_team_dashboard.get_dict()
    #Debugging
    #print(dict)
    #Formatting output string - is there a better way to do this?
    reply = "*Stats for {} in {}*\n".format(get_team_name(id),dict['data'][0][1])
    reply += "{:<8}{:^5}\n".format('Record:',(str(dict['data'][0][3])+'-'+str(dict['data'][0][4])))
    reply += "*General Stats*\n"
    reply += "{:<3}: {:^4}\n".format('PPG',dict['data'][0][26])
    reply += "{:<3}: {:^3}\n".format('APG',dict['data'][0][19])
    reply += "{:<3}: {:^3}\n".format('RPG',dict['data'][0][18])
    reply += '*Shooting*:\n'
    reply += '{:<15}'.format('FG, FGA, FG% : ') + '{:^4},'.format(dict['data'][0][7]) + ' {:^4},'.format(dict['data'][0][8]) + ' {:^4.1%}'.format(dict['data'][0][9])+'\n'
    reply += '{:<15}'.format('3P, 3PA, 3P% : ') + '{:^4},'.format(dict['data'][0][10]) + ' {:^4},'.format(dict['data'][0][11]) + ' {:^4.1%}'.format(dict['data'][0][12])+'\n'
    reply += '{:<15}'.format('FT, FTA, FT% : ') + '{:^4},'.format(dict['data'][0][13]) + ' {:^4},'.format(dict['data'][0][14]) + ' {:^4.1%}'.format(dict['data'][0][15])+'\n\n'
    reply += '*Rebounding*:\n'
    reply += '{:<11}'.format('ORB, DRB : ') +  '{:^4},'.format(dict['data'][0][16]) + ' {:^4}'.format(dict['data'][0][17])+'\n\n'
    reply += '*Defensive*:\n'
    reply += '{:<15}'.format('STL, BLK, PF : ') + '{:^4},'.format(dict['data'][0][21]) + ' {:^4},'.format(dict['data'][0][22]) + ' {:^4}'.format(dict['data'][0][24])+'\n'
    #Debugging
    print(reply)
    return(reply)

def get_team_stats(name):
    try:
        response = team_stats_lookup(get_team_id(name),season='2020-21')
        return(response)
    except:
        return("An error has occured. Please try again.")

#Debugging
#team_stats_lookup(get_team_id('Pelicans'),'2020-21')
get_team_stats('Lakers')