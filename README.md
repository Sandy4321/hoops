#Test data:
#James Harden Player_ID: 201935
#Washington Wizards Team_ID: 1610612764

#FULL RESOLUTION ACTION PHOTO!!
#http://stats.nba.com/media/players/700/201935.png

#Profile photo, perhaps we can create a basketball "card"
#http://stats.nba.com/media/players/230x185/201935.png




# hoops
#####hoops is a nba basketball game prediction engine written to make it easier to predict the winner
of an upcoming game based on NBA team and player metrics
#####This project is written in Python, utilizing the 'requests' library to grab JSON data from the NBA and populate relevant data to a database for rapid querying.
<br>
### Version
v4 - updated to use my hotfuzz project, fixed up code, Flask Web API porting in progress
v3 - moved over to using SQL instead, significantly faster execution, much lower memory usage, and fewer lines of code!
v2 relies on NBA PIE ratio for each team instead of per player, added offline caching of json files, MUCH faster execution
v1 - first release, used current roster PIE data per player

###Upcoming features/fixes:

  - Finalize porting over to Flask as Web API project
  - We must scrape most current starting line up / bench data, and we will use beautiful soup to help us with this (Good source for web scrape data : http://www.rotowire.com/basketball/nba_lineups.htm ) although the NBA would be a better source for starting lineup data, may be difficult to test in off-season using live data
  - Start implementing external variables and additional data


###Bugs / Upcoming fixes

#####Fixes coming in next update
  - Correctly authenticate users and send verification token emails
  - Publish unit tests

#####Fixes coming in future updates
  - Implement websockets to replace POST requests
  - Move over to using Postgres, and use memcache to handle session data

###Attribution and Licensing
#####**MIT License**
#####**(c)2015 Kamil Mansuri**
<br>
#####**hoops is not affiliated with the NBA**
#####**NBA and its associated trademarks are (C) National Basketball Association**
#####**[@supermansuri]**
<br>

[Flask]:http://flask.pocoo.org/
[gunicorn]:http://gunicorn.org/
[Twitter Bootstrap]:http://twitter.github.com/bootstrap/
[jQuery]:http://jquery.com
[@supermansuri]:http://twitter.com/supermansuri
[nginx]:http://nginx.org/
[jenkins]:https://jenkins-ci.org/
