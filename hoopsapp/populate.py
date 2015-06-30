#populates our SQL db with the data we need from the NBA.com JSON stats data

import requests
from hoopsapp.models import Teams, Players
from hoopsapp import db


def _create_team_data():
    
    
    url = 'http://stats.nba.com/stats/leaguedashteamstats?DateFrom=&DateTo=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&VsConference=&VsDivision='
    
    data = requests.get(url).json()

    #capturing all the data, but no headers
    team_data = data['resultSets'][0]['rowSet']


    #This has been confirmed working! We will use a for loop instead of execute many, and we use the * to unpack variables
    for team in team_data:
        item = Teams(*team)
        db.session.merge(item)

    db.session.commit()    


def _create_player_data(team_id):

    #Test data:
    #James Harden Player_ID: 201935
    #Washington Wizards Team_ID: 1610612764

    #FULL RESOLUTION ACTION PHOTO!!
    #http://stats.nba.com/media/players/700/201935.png

    #Profile photo, perhaps we can create a basketball "card"
    #http://stats.nba.com/media/players/230x185/201935.png


    url = "http://stats.nba.com/stats/teamplayerdashboard?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID="+str(team_id)+"&VsConference=&VsDivision="
    
    data = requests.get(url).json()
    #There is a lot of other data here, but we will only be using this to grab
    #all the players from each team for now
    result = data['resultSets']

    #We use teaminfo to grab the team_id and team_name info 
    teaminfo = result[0]['rowSet'][0][1:3]

    #We just grab the player_id and the player_name from the data and add it
    #after the team_id and team_name, the player_id is the primary key
    players = [teaminfo+row[1:3] for row in data['resultSets'][1]['rowSet']]

    #We will use a for loop instead of executemany, and we use the * to unpack
    for player in players:

        #Here we retrieve PST, AST, REB, and PIE for each player_id, append it, and write it to the db
        url = "http://stats.nba.com/stats/commonplayerinfo?LeagueID=00&PlayerID="+str(player[2])+"&SeasonType=Regular+Season"
        data = requests.get(url).json()
        player.extend(data['resultSets'][1]['rowSet'][0][3:])

        item = Players(*player)
        db.session.merge(item)

    db.session.commit()    


    #for now, we will keep a dict in memory of the player_Id's for the team and their corresponding names
    #Not much data here to store in memory, but if we choose to do this big, let's use Redis or just memcache
    #teamplayers = {players[x][2]:players[x][3] for x in range(0,len(players))}


def _populate_all():

    #this populates our db with all general team data
    _create_team_data()
    #this creates a dictionary to help us
    teams = Teams.query.all()
    for team in teams:
        _create_player_data(team.TEAM_ID)
