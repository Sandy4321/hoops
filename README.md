# hoops
hoops v3 - nba basketball simulation

v3 - significant update, using SQLite for master cache of all NBA teams along with the essential player data, everything works lightning fast now. Removed a lot of unnecessary code since we are no longer storing JSON objects doing any File IO, and have no use for pandas... for now.

future updates:
v4 - focus will be on moving application to web framework, correctly using starting lineup data to "predict" upcoming games. 
v5 - focus will be on using ALL of the appropriate data to better predict outcome and eliminate the need for a 12.5% 'luck' chance
