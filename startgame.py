"""
nba game simulation v1 - March 2015
Kamil Mansuri

The project is my entry into using live data to feed into a simulation, and to use this data to calculate an end result.
The idea is to eventually turn this into a graphical NBA Manager simulation game similar to 'Football Manager',
given the large amount of player data that NBA has on games in the more recent seasons.


v1 -
Player Data calculated: Total Points Scored, Total Assists, Total Rebounds, and Total PIE (NBA Player Impact Estimate),
Averages of all of this data as well.
The simulation doesn't use most of this data at present, I found more stable results from using just the average PIE value,
but I filter out any team player that has a negative PIE value before calculating this so out of commission players (or very new
players do not factor in). I also give the 'weaker' team around a 12.5% luck probability.
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
            
            