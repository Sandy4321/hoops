#hoops() 
#nba simulation v3 - May 2015
#Kamil Mansuri

#v1 - first release, used current roster PIE data per player
#v2 relies on NBA PIE ratio for each team instead of per player, added offline caching of json files, MUCH faster execution
#v3 - moved over to using SQL instead, significantly faster execution, much lower memory usage, and fewer lines of code!

#*future versions*:
#v4 will involve going back to PIE ratio data per player, but to do this right
#we must scrape most current starting line up / bench data, and we will use fuzzylogic/beautiful soup to help us with this
#http://www.rotowire.com/basketball/nba_lineups.htm
#v5 start implementing external variables and additional data

import fuzzylogic
import sqlite3

import populate


#will not refresh data if less than 2 weeks old, but you can make this longer or shorter based on preference
#datarefreshtime = 1209600

#set the global connection to our database
db = sqlite3.connect('hoops.db')

#set the initial cursor to our database
cur = db.cursor()

#cur.execute('''SELECT TEAM_ID, TEAM_NAME FROM teams''')
#teams = dict(cur.fetchall())



class Team(object):
    
    def __init__(self, query):

        self.team_id, self.team_name = self.getteam(query)
        self.players = self.getplayers()
        self.teampie = self.getteampie()
                           

    def getteam(self, query):
        
        #flips the team_name and team_id around in a new dict for using fuzzylogic
        cur.execute('''SELECT TEAM_NAME, TEAM_ID FROM teams''')
        teams = dict(cur.fetchall())        
        team_name = fuzzylogic.extractOne(query,teams.keys())[0]        
        return teams[team_name], team_name


    def getplayers(self):
        
        #we will grab all of the players data for the selected team    
        cur.execute('''SELECT PLAYER_ID, PLAYER_NAME, PST, AST, REB, PIE FROM players WHERE TEAM_ID = (?)''', (self.team_id,))
        return cur.fetchall()

    def getteampie(self):

        #assign PIE value to the current team
        cur.execute('''SELECT PIE FROM teams WHERE TEAM_ID = (?)''', (self.team_id,))
        return float(cur.fetchone()[0])*100

    def getotherstats(self):
        pass


    #We can call on these two methods to refresh our data from the nba when we need to

    def refresh_teams(self):
        populate._create_team_data()

    def refresh_players(self):
        populate._create_player_data(self.team_id)


