# nba-telebot
NBA Chatbot for Telegram to provide information for players, teams and the league.

## Features:
1. /playerstats player, year
> Returns the specified player's stats for the given season from Basketball Reference. Defaults to current season (2021) if not specified.
2. /games
> Returns today's NBA games with live scores (if applicable) with links to game box scores from nba.com
3. /standings east/west
> Returns the standings for the specified conference from Basketball Reference. Returns standings from both conferences if argument not specified.
4. /teamstats team name
> Returns general statistics for the specified team taken from ESPN.com

## Upcoming Features:
- [ ] Added functionality to /playerstats: Obtaining data for multiple seasons and career averages
- [X] /teamstats - Overview for a team with record, upcoming matches, injury reports and stat leaders
