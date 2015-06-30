#sample player image
#http://stats.nba.com/media/players/700/201935.png


#Quick and dirty grab of high resolution player action images
#We save each logo as the appropriate playerID + png ext

import requests

#3rd party wget extension, we will not be using this file in production
#so I opted to use wget instead of urllib here
import wget


player_dict = {}

url = 'http://goo.gl/4yUw6x'
data = requests.get(url).json()
team_data = data['resultSets'][0]['rowSet']
for team in team_data:
    s_data = requests.get('http://stats.nba.com/stats/commonteamroster?LeagueID=00&Season=2015-16&TeamID='+str(team[0])).json()

    for player in s_data['resultSets'][0]['rowSet']:
        player_dict[player[12]] = playerurl = 'http://stats.nba.com/media/players/700/'+str(player[12])+'.png'
    	wget.download(playerurl)
