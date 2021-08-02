from nba_api.stats.endpoints import leaguestandingsv3, scoreboardv2
from nba_api.stats.static import teams

def get_league_standings(conference):
    data = leaguestandingsv3.LeagueStandingsV3(season='2020-21',season_type="Regular Season").standings.get_dict()['data']
    print(data)
    eastern_conference_string = "*Eastern Conference*\n"
    western_conference_string = "*Western Conference*\n"
    for team in data:
        if team[6] == "West":
            western_conference_string += "{}. {} ({})\n".format(team[8],team[3] + " " + team[4],team[17])
        else:
            eastern_conference_string += "{}. {} ({})\n".format(team[8],team[3] + " " + team[4],team[17])
    
    if conference.lower == "western" or conference.lower == "w" or conference.lower == "west":
        print(eastern_conference_string)
        return(western_conference_string)
    elif conference.lower == "eastern" or conference.lower == "e" or conference.lower == "east":
        print(eastern_conference_string)
        return(eastern_conference_string)
    else:
        print(western_conference_string + '\n' + eastern_conference_string)
        return(western_conference_string + '\n' + eastern_conference_string)

def get_games():
    #Format for Date is YYYY-MM-DD
    games=scoreboardv2.ScoreboardV2(game_date='2021-07-20')
    print(games.game_header.get_dict())

get_games()
