
import requests
#import json -- we may not even need this anymore since we are moving to SQL
import sqlite3
import fuzzylogic

#set the global connection to our database
db = sqlite3.connect('test.db')

#set the initial cursor to our database
cur = db.cursor()

#current data refresh time (seconds) is set to 5 days [there are 86400 seconds per day]
datarefreshtime = 432000

#v3 - we no longer keep the data in memory, we'll leave the data in a sqlite3 db and query as necessary
#we should notice a nice speed increase from this

class Team(object):
    
    def __init__(self, query):
        
        #start refreshing team data from nba, and write to sql db
        print "Refreshing team list, please wait..."
        self.create_team_data()
        
        #this will set a self.team_name and self.team_id
        self.getteam(query)

        #sets a self.masterdata list for each player -> **WE WANT TO USE SQL INSTEAD OF THIS**
        #refreshes each player's stats from the nba, and write to sql db

        self.masterdata = []

        self.create_player_data()


        #v2 variables
        self.teampie = 0.00
   



    #this was formerly get_team_data()
    def create_team_data(self):

           
        url = 'http://stats.nba.com/stats/leaguedashteamstats?DateFrom=&DateTo=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&VsConference=&VsDivision='
        data = requests.get(url).json()
                   
        #capture all team data
        #"TEAM_ID","TEAM_NAME","GP","W","L","W_PCT","MIN","OFF_RATING","DEF_RATING","NET_RATING","AST_PCT","AST_TO","AST_RATIO","OREB_PCT","DREB_PCT","REB_PCT","TM_TOV_PCT","EFG_PCT","TS_PCT","PACE","PIE","CFID","CFPARAMS"
        ##(TEAM_ID, TEAM_NAME, GP, W, L, W_PCT, MIN, OFF_RATING, DEF_RATING, NET_RATING, AST_PCT, AST_TO, AST_RATIO, OREB_PCT, DREB_PCT, REB_PCT, TM_TOV_PCT, EFG_PCT, TS_PCT, PACE, PIE, CFID, CFPARAMS)


        #data type is list
        #headers = data['resultSets'][0]['headers']

        #data type is list
        team_data = data['resultSets'][0]['rowSet']


        cur.execute('''CREATE TABLE IF NOT EXISTS teams (TEAM_ID INT PRIMARY KEY, TEAM_NAME TEXT, GP INT, W INT, L INT, W_PCT REAL, MIN INT, OFF_RATING REAL, DEF_RATING REAL, NET_RATING REAL, AST_PCT REAL, AST_TO REAL, AST_RATIO REAL, OREB_PCT REAL, DREB_PCT REAL, REB_PCT REAL, TM_TOV_PCT REAL, EFG_PCT REAL, TS_PCT REAL, PACE REAL, PIE REAL, CFID INT, CFPARAMS TEXT)''')

        cur.executemany('''INSERT OR REPLACE INTO teams VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', team_data)

        db.commit()


    #this was formerly getplayers()
    def create_player_data(self):

        #Test data:
        #James Harden Player_ID: 201935
        #Washington Wizards Team_ID: 1610612764


        url = "http://stats.nba.com/stats/teamplayerdashboard?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID="+str(self.team_id)+"&VsConference=&VsDivision="
        data = requests.get(url).json()

        #We use teaminfo to grab the team_id and team_name info from the same json for use in our upcoming junction table
        teaminfo = data['resultSets'][0]['rowSet'][0][1:3]
       
        #We just grab the player_id and the player_name from the data and add it after the team_id and team_name
        #We are ensuring the player_id is the primary key here
        players = [teaminfo+row[1:3] for row in data['resultSets'][1]['rowSet']]

        cur.execute(''' CREATE TABLE IF NOT EXISTS players (TEAM_ID INT, TEAM_NAME TEXT, PLAYER_ID INT PRIMARY KEY, PLAYER_NAME TEXT, PST REAL, AST REAL, REB REAL, PIE REAL)''')

        try: 
            cur.executemany('''INSERT OR REPLACE INTO players(TEAM_ID, TEAM_NAME, PLAYER_ID, PLAYER_NAME) VALUES (?, ?, ?, ?)''', players)
        
        except sqlite3.OperationalError:
            print "Values already inserted or something went wrong!"

        #for now, we will keep a dict in memory of the player_Id's for the team and their corresponding names
        self.teamplayers = {players[x][2]:players[x][3] for x in range(0,len(players))}

        #this used to be getplayerstats but we merged everything to create_player_data

        for pid, name in self.teamplayers.items():
                        
            print "Refreshing stats for %s please wait..." % name
            url = "http://stats.nba.com/stats/commonplayerinfo?LeagueID=00&PlayerID="+str(pid)+"&SeasonType=Regular+Season"
            data = requests.get(url).json()
            stats = data['resultSets'][1]['rowSet'][0][3:] + [pid]

            #basic data on player[player_id] = [player_name, total points, total assists, total rebounds, PIE (player impact estimate) value]
            #self.masterdata[pid] = [name, stats[0], stats[1], stats[2], stats[3]]

            try: 
                
                cur.executemany('''UPDATE players SET PST=?, AST=?, REB=?, PIE=? WHERE PLAYER_ID = ?''', (stats,))

            except sqlite3.OperationalError:

                print "Values already inserted or something went wrong!"

            
        db.commit()





    #does not return anything, but stores the team's name and id in memory
    def getteam(self, query):
        #create a dict with a k:v of TEAM_NAME: TEAM_ID for fuzzylogic usage
        v2 = dict(cur.execute('''SELECT TEAM_NAME, TEAM_ID FROM TEAMS'''))
        self.team_name = fuzzylogic.extractOne(query,v2.keys())[0]           
        self.team_id = v2[self.team_name]



#---------------------EDIT THIS STUFF BELOW---------------------------------------

    #this is here for getteamstats(), let's get rid of it!
    #returns a dict with k:v of TEAM_ID: TEAM_NAME
    def team_id_key(self):
        v1 = cur.execute('''SELECT TEAM_ID, TEAM_NAME FROM TEAMS''')
        return {k:v for (k,v) in v1}


    def getteamstats(self):

            #this was done very poorly, let's just do a sql lookup for speed
            '''
            for team_id in self.team_id_key().keys():
                for x in range(len(self.team_id_key)):
                    if self.team_data[x][0] == self.team_id:
                        self.teampie = self.team_data[x][0][20]
            '''
