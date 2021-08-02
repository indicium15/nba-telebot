# nba-telebot
NBA Chatbot for Telegram to provide information for players, teams and the league.
## Rewriting functions using nba_api
The previous APIs I was using were built from looking at websites using BeautifulSoup / Selenium. This often led to crashes and unstable behavior not producing the results I wanted.

After finding [nba-api](https://github.com/swar/nba_api), I am working on porting over functionality using these APIs.

Legacy code will remain in the "old" folder.

## Features:
1. /playerstats player
> Returns the specified player's stats for the current season from the [PlayerDashboardByYearOverYear](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/playerdashboardbyyearoveryear.md)
2. /careerstats player 
> Returns the career stats for the selected player.
3. /games (Pending Porting Over)
> Returns today's NBA games with live scores (if applicable) with links to game box scores from nba.com using Selenium.
4. /standings east/west
> Returns the standings for the specified conference from [LeagueStandings](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/leaguestandings.md) endpoint. Returns standings from both conferences if argument not specified.
5. /teamstats team_name
> Returns general statistics for the specified team taken from [TeamDashboardByYearOverYear](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/teamdashboardbyyearoveryear.md) endpoint.

## Upcoming Features:
- [X] /teamstats - Overview for a team with record, upcoming matches, injury reports and stat leaders
- [] Added functionality to playerstats with in-line buttons to present active seasons for a selected player
- [] Rewriting game command using nba_api endpoints