# hoops
hoops v3 - nba basketball simulation and prediction engine

v1 -  Player Data calculated: Total Points Scored, Total Assists, Total Rebounds, and Total PIE (NBA Player Impact Estimate),
Averages of all of this data as well.
The simulation doesn't use most of this data at present, I found more stable results from using just the average PIE value,
but I filter out any team player that has a negative PIE value before calculating this so out of commission players (or very new
players do not factor in). I also give the 'weaker' team around a 12.5% luck probability.

v2 -  Rewrite to use on disk caching for speedup, added in 2-week refresh period

v3 - significant update, using SQLite for master cache of all NBA teams along with the essential player data, everything works lightning fast now.  Removed a lot of unnecessary code since we are no longer storing JSON objects doing any File IO. Removed all refreshing for now, but I created separate methods for refreshing team data, player data, and all data.

future updates:

v4 - focus will be on moving application to web framework, correctly using starting lineup data to "predict" upcoming games. I would rather store all data on server side and we can use cron to refresh data in background. 

v5 - focus will be on using ALL of the appropriate data to better predict outcome and eliminate the need for a 12.5% 'luck' chance

v6 - RESTful API for all stats, and caching even more data -> switching over to using PostreSQL
