
#Quick and dirty grab of high resolution SVG logos
#We save each logo as the appropriate teamID + .svn ext

import requests

#3rd party wget extension, we will not be using this file in production
#so I opted to use wget instead of urllib here
import wget


team_dict = {}

url = 'http://goo.gl/4yUw6x'
data = requests.get(url).json()
team_data = data['resultSets'][0]['rowSet']
for team in team_data:
    s_data = requests.get('http://stats.nba.com/stats/teaminfocommon?LeagueID=00&SeasonType=Regular+Season&TeamID='+str(team[0])+'&season=2015-16').json()
    team_dict[team[0]] = logourl = str('http://stats.nba.com/media/img/teams/logos/'+s_data['resultSets'][0]['rowSet'][0][4]+'_logo.svg')
    wget.download(logourl, str(team[0])+'.svg')