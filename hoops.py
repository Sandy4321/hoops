#hoops() 
#nba simulation v2
#Kamil Mansuri

#v1 - first release, used current roster PIE data per player
#v2 relies on NBA PIE ratio for each team instead of per player, added offline caching of json files, MUCH faster execution

#future versions:
#v3/v4 will involve going back to PIE ratio data per player, but to do this right
#we must scrape most current starting line up / bench data, and we will use fuzzylogic to help us with this
#http://www.rotowire.com/basketball/nba_lineups.htm
#v5/v6 will involve caching all data into SQL database so we can make use of more data and start
#implementing actual play for the simulation



import fuzzylogic
import requests
import json
import os.path
import time

#will not refresh data if less than 2 weeks old, but you can make this longer or shorter based on preference
datarefreshtime = 1209600

class Team(object):
    
    def __init__(self, query):
        
        #retreiving team data from nba
        print "Refreshing team list, please wait..."
        
        self.get_team_data()

        #creating a dictionary with players from the team
        self.team_id = self.getteam(query)
        self.teamplayers = self.getplayers()
        self.masterdata = {}

        #v2 variables
        self.teampie = 0.00
        
        #Will be updated by the game
        #self.pids = []
        #self.playernames = []
        #self.points = []
        #self.assists = []
        #self.rebounds =[]
        #self.pie = []
        #self.avgpoints = 0.00
        #self.avgassists = 0.00
        #self.avgrebounds = 0.00
        #self.avgpie = 0.00
        
        #creating a dictionary with stats for each player
        self.getplayerstats()
        

    def get_team_data(self):
        
        '''
        This will retreive the JSON data for all NBA teams. If not possible, we will use a locally cached version (v2)
        We are storing self.teams in memory, but we will be moving to storing all data in a SQL in a later version (v3+)
        '''
    
        #if os.path.isfile('./data/teamdata.json'):
        url = 'http://stats.nba.com/stats/leaguedashteamstats?DateFrom=&DateTo=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&VsConference=&VsDivision='

        #if the file is younger than the datarefreshtime we specified, let's use offline data
        if os.path.isfile('./data/teamdata.json') and time.time() - os.path.getmtime('./data/teamdata.json') <= datarefreshtime:
            data = json.loads(open('./data/teamdata.json').read())

        else:

            try:
                data = requests.get(url).json()
                with open('./data/teamdata.json', 'w+') as outfile:
                    json.dump(data, outfile)

            except:
                data = json.loads(open('./data/teamdata.json').read())

                    
        
        #capture all team data
        #"TEAM_ID","TEAM_NAME","GP","W","L","W_PCT","MIN","OFF_RATING","DEF_RATING","NET_RATING","AST_PCT","AST_TO","AST_RATIO","OREB_PCT","DREB_PCT","REB_PCT","TM_TOV_PCT","EFG_PCT","TS_PCT","PACE","PIE","CFID","CFPARAMS"
        #self.headers = data['resultSets'][0]['headers']
        
        self.team_data = data['resultSets'][0]['rowSet']
        
                
    #create team_id : team_name dictionary // for team_id as key lookup
    def team_id_key(self):
        return {team[0]:team[1] for team in self.team_data}


    def getteam(self, query):
        
        #flips the team_name and team_id around in a new dict for using fuzzylogic
        fuzzyteams = dict((v,k) for k,v in self.team_id_key().iteritems())
        
        self.team_name = fuzzylogic.extractOne(query,fuzzyteams.keys())[0]           
        return fuzzyteams[self.team_name]


    def getplayers(self):
            
        #we can use this to gather all players from a team using the self.team_id, we will return a list full of player_ids
        #v2 now implements an "offline" mode, where we will cache this JSON data if possible and use offline data as long as it's less than 2 weeks old

        if os.path.isfile('./data/'+str(self.team_id)+'.json') and time.time() - os.path.getmtime('./data/'+str(self.team_id)+'.json') <= datarefreshtime:
    
            teamplayersdata = json.loads(open('./data/'+str(self.team_id)+'.json').read())
                
            return {teamplayersdata[x][1]:teamplayersdata[x][2] for x in range(0,len(teamplayersdata))}

        else:

            try:

                url = "http://stats.nba.com/stats/teamplayerdashboard?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID="+str(self.team_id)+"&VsConference=&VsDivision="
                data = requests.get(url).json()
                teamplayersdata = data['resultSets'][1]['rowSet']

                with open('./data/'+str(self.team_id)+'.json', 'w+') as outfile:
                    json.dump(teamplayersdata, outfile)                 
                
                return {teamplayersdata[x][1]:teamplayersdata[x][2] for x in range(0,len(teamplayersdata))}

            except:

                print "Cannot update from server, using local player data"
                teamplayersdata = json.loads(open('./data/'+str(self.team_id)+'.json').read())
                return {teamplayersdata[x][1]:teamplayersdata[x][2] for x in range(0,len(teamplayersdata))}



    def getplayerstats(self):
    
            #We will build our dictionary of master player data for the instanced team with player_id as the key
            #Offline mode not yet implemented here
            
            for pid, name in self.teamplayers.items():
                
                try:

                    print "Refreshing stats for %s please wait..." % name
                    url = "http://stats.nba.com/stats/commonplayerinfo?LeagueID=00&PlayerID="+str(pid)+"&SeasonType=Regular+Season"
                    data = requests.get(url).json()
                    stats = data['resultSets'][1]['rowSet'][0]
                    #basic data on player[player_id] = [player_name, total points, total assists, total rebounds, PIE (player impact estimate) value]
                    self.masterdata[pid] = [name, stats[3], stats[4], stats[5], stats[6]]

                except:

                    print "An offline version is not provided at this time, please check your connection or the nba site has been modified"



        #Here we will use the team_data we have stored in memory for each team and retrieve various team stats
        #v2 simplifies things greatly and we now grab the calculated team PIE directly from the data
        #for v3 we will incorporate player data and use each player's data in determining the winner instead of our 'luck' method 

    def getteamstats(self):

            for team_id in self.team_id_key().keys():
                for x in range(len(self.team_id_key)):
                    if self.team_data[x][0] == self.team_id:
                        self.teampie = self.team_data[x][0][20]

