#populates our SQL db with the data we need from the NBA.com JSON stats data

import requests
import sqlite3

#set the global connection to our database
db = sqlite3.connect('hoops.db')

#set the initial cursor to our database
cur = db.cursor()

'''
may need to add a db_join() method at the end
'''

#this populates general team data for all teams

def _create_team_data():

       
    url = 'http://stats.nba.com/stats/leaguedashteamstats?DateFrom=&DateTo=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&VsConference=&VsDivision='
    data = requests.get(url).json()
               
    #capturing all the data, but no headers
    team_data = data['resultSets'][0]['rowSet']

    #create the table and set up the headers with types
    #(TEAM_ID, TEAM_NAME, GP, W, L, W_PCT, MIN, OFF_RATING, DEF_RATING, NET_RATING, AST_PCT, AST_TO, AST_RATIO, OREB_PCT, DREB_PCT, REB_PCT, TM_TOV_PCT, EFG_PCT, TS_PCT, PACE, PIE, CFID, CFPARAMS)
    cur.execute('''CREATE TABLE IF NOT EXISTS teams (TEAM_ID INT PRIMARY KEY, TEAM_NAME TEXT, GP INT, W INT, L INT, W_PCT REAL, MIN INT, OFF_RATING REAL, DEF_RATING REAL, NET_RATING REAL, AST_PCT REAL, AST_TO REAL, AST_RATIO REAL, OREB_PCT REAL, DREB_PCT REAL, REB_PCT REAL, TM_TOV_PCT REAL, EFG_PCT REAL, TS_PCT REAL, PACE REAL, PIE REAL, CFID INT, CFPARAMS TEXT)''')

    #getting all the team data in there
    cur.executemany('''INSERT OR REPLACE INTO teams VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', team_data)

    #write the data
    db.commit()



#we will pass on the team_id parameter to this method
#to populate the player data for team_id
def _create_player_data(team_id):

    #Test data:
    #James Harden Player_ID: 201935
    #Washington Wizards Team_ID: 1610612764


    #There is a lot of other data here, but we will only be using this to grab all the players from each team for now
    url = "http://stats.nba.com/stats/teamplayerdashboard?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID="+str(team_id)+"&VsConference=&VsDivision="
    data = requests.get(url).json()
    result = data['resultSets']


    #We use teaminfo to grab the team_id and team_name info 
    teaminfo = result[0]['rowSet'][0][1:3]
    
   
    #We just grab the player_id and the player_name from the data and add it after the team_id and team_name
    #We are ensuring the player_id is the primary key here
    players = [teaminfo+row[1:3] for row in data['resultSets'][1]['rowSet']]

    cur.execute(''' CREATE TABLE IF NOT EXISTS players (TEAM_ID INT, TEAM_NAME TEXT, PLAYER_ID INT PRIMARY KEY, PLAYER_NAME TEXT, PST REAL, AST REAL, REB REAL, PIE REAL)''')

    try: 
        cur.executemany('''INSERT OR REPLACE INTO players(TEAM_ID, TEAM_NAME, PLAYER_ID, PLAYER_NAME) VALUES (?, ?, ?, ?)''', players)
    
    except sqlite3.OperationalError:
        print "Values already inserted or something went wrong!"

    #for now, we will keep a dict in memory of the player_Id's for the team and their corresponding names
    teamplayers = {players[x][2]:players[x][3] for x in range(0,len(players))}
    #alternative could be: {result[1]['rowSet'][x][1]: result[1]['rowSet'][x][2] for x in range(len(result[1]['rowSet']))}



    for pid, name in teamplayers.items():

        print "Refreshing stats for %s (%s) please wait..." % (name, teaminfo[1])
        url = "http://stats.nba.com/stats/commonplayerinfo?LeagueID=00&PlayerID="+str(pid)+"&SeasonType=Regular+Season"
        data = requests.get(url).json()
        stats = data['resultSets'][1]['rowSet'][0][3:] + [pid]

        try: 
            
            cur.executemany('''UPDATE players SET PST=?, AST=?, REB=?, PIE=? WHERE PLAYER_ID = ?''', (stats,))

        except sqlite3.OperationalError:

            print "Values already inserted or something went wrong!"

        
    db.commit()


def _populate_all():

    global db

    #this populates our db with all general team data
    _create_team_data()
    #this creates a dictionary to help us
    cur.execute('''SELECT TEAM_ID, TEAM_NAME FROM teams''')
    teams = dict(cur.fetchall())
    #this populates our db with all player data for all teams
    for k in teams.keys():
        _create_player_data(k)

    db.close()