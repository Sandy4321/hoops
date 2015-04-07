import random
from prettytable import PrettyTable



def teamstats(team, query):

    opts = ['pids', 'names', 'points', 'assists', 'rebounds', 'pies' ]
    
    if query in opts:
        
        if query == 'pids':    
     
            #returns a list of PLAYER IDs for all contributing players
            return [k for k,v in team.masterdata.items() if team.masterdata[k][4] > 0]
        
        if query == 'names':
            
            #returns a list of PLAYER NAMES for all contributing players
            return [team.masterdata[k][0] for k,v in team.masterdata.items() if team.masterdata[k][4] > 0]
        
        elif query == 'points':
        
            #returns list of POINTS for all contributing players
            return [team.masterdata[k][1] for k,v in team.masterdata.items() if team.masterdata[k][4] > 0]
        
        elif query == 'assists':
        
            #returns list of ASSISTS for all contributing players
            return [team.masterdata[k][2] for k,v in team.masterdata.items() if team.masterdata[k][4] > 0]
        
        elif query == 'rebounds':
        
            #return list of REBOUNDS for all contributing players
            return [team.masterdata[k][3] for k,v in team.masterdata.items() if team.masterdata[k][4] > 0]
        
        elif query == 'pies':
        
            #returns list of PIEs for all contributing players
            return [team.masterdata[k][4] for k,v in team.masterdata.items() if team.masterdata[k][4] > 0]
        
    else:
        print "Something went wrong in teamstats()"
    

def excitement(team1, team2):
    #This will take PIE into consideration and give the weaker team a 50/50
    #chance to stay relevant, because the team with the higher PIE ratio would otherwise win
    
    #I have assigned around a 12% probability that the weaker team based on PIE will end up winning
    #in the event of a tie, we roll a 50/50 chance 7 times
    
    chance = bool(random.getrandbits(3)) 
           
    if team1.teampie > team2.teampie and not chance:
        return team2
    elif team1.teampie < team2.teampie and not chance:
        return team1
    
    elif team1.teampie > team2.teampie:
        return team1
    
    elif team1.teampie < team2.teampie:
        return team2
    
    elif team1.teampie == team2.teampie:    
        for x in range(0,7):
            chance = bool(random.getrandbits(1))
        if chance:
            return team1
        else:
            return team2
        

def tables(team1, team2, winner):
    print '*'*80
    print "Congratulations!\nThe winner of the simulation are the %s!" % winner.team_name
    print '*'*80+'\n'

    t1 = PrettyTable()
    t1.add_column("Name", teamstats(team1,'names'))
    t1.add_column("Player ID", teamstats(team1,'pids'))   
    t1.add_column("Points", teamstats(team1,'points'))
    t1.add_column("Assists", teamstats(team1,'assists'))
    t1.add_column("Rebounds", teamstats(team1,'rebounds'))
    t1.add_column("Player Impact", teamstats(team1,'pies'))
    print team1.team_name
    print t1
    
    print "\n"
    
    t2 = PrettyTable()
    t2.add_column("Name", teamstats(team2,'names'))
    t2.add_column("Player ID", teamstats(team2,'pids'))   
    t2.add_column("Points", teamstats(team2,'points'))
    t2.add_column("Assists", teamstats(team2,'assists'))
    t2.add_column("Rebounds", teamstats(team2,'rebounds'))
    t2.add_column("Player Impact", teamstats(team2,'pies'))
    print team2.team_name
    print t2

    print "\n"