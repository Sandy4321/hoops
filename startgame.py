"""
hoops v3 - May 2015
Kamil Mansuri

NBA Game Simulation

v1 -  Player Data calculated: Total Points Scored, Total Assists, Total Rebounds, and Total PIE (NBA Player Impact Estimate),
Averages of all of this data as well.
The simulation doesn't use most of this data at present, I found more stable results from using just the average PIE value,
but I filter out any team player that has a negative PIE value before calculating this so out of commission players (or very new
players do not factor in). I also give the 'weaker' team around a 12.5% luck probability.

v2 -  Rewrite to use on disk caching for speedup

v3 - significant update, using SQLite for master cache of all NBA teams along with the essential player data, everything works lightning fast now. 
Removed a lot of unnecessary code since we are no longer storing JSON objects doing any File IO

future updates:
v4 - focus will be on moving application to web framework, correctly using starting lineup data to "predict" upcoming games. 
v5 - focus will be on using ALL of the appropriate data to better predict outcome and eliminate the need for a 12.5% 'luck' chance
v6 - RESTful API for all stats, and caching even more data -> switching over to using PostreSQL

"""

import hoops
import stats

    
def gamestart():
    
    #We allow for fuzzy logic responses to team names because of the multitude of nicknames ('knick'-names?) of NBA teams.
    
        
    queryteam1 = raw_input('Please enter an NBA team name for Team 1\n> ')
    team1 = hoops.Team(queryteam1)
    print "\n"
    print 'Team 1 is the %s' % team1.team_name
    print "\n"
    
    queryteam2 = raw_input('Please enter an NBA team name for Team 2\n> ')
    team2 = hoops.Team(queryteam2)
    print "\n"
    print 'Team 2 is the %s' % team2.team_name
    print "\n"
    
   
    winner = stats.excitement(team1, team2)
    stats.tables(team1, team2, winner)


if __name__ == "__main__":
    
    gamestart()
    raw_input("Thank you for playing!\nPlease press enter key to end game")
            
            