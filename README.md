# hoops
#####hoops is a nba basketball game prediction engine written to make it easier to predict the winner of an upcoming game based on NBA team and player metrics
#####This project is written in Python, utilizing the 'requests' library to grab JSON data from the NBA and populate relevant data to a database for rapid querying.

### Version
v4 - Coming in July 2015, stay tuned!
v3 - moved over to using SQL instead, significantly faster execution, much lower memory usage, and fewer lines of code!
v2 relies on NBA PIE ratio for each team instead of per player, added offline caching of json files, MUCH faster execution
v1 - first release, used current roster PIE data per player

###Upcoming features/fixes (v4 early July 2015):
  - Flask port with web host running over nginx/gunicorn (90% done)
  - Graphics, assets, making things beautiful  (100% done)
  - Twitter Bootstrap to keep project mobile-focused (100% done)
  - RESTful Web API service (70% done)
  - Speed/caching improvements (90% done)
  - Cleaning up codebase, reducing dependencies, integrating my 'hotfuzz' module (100% done)

### Future fixes (August 2015)
  - Publish Unit Tests
  - Implement some sort of authentication and vertification token
  - We MUST use starting lineup data, but this appears to only be available if we use web scraping on rotowire (cannot test in off-season as there is no available data to scrape) - possible to get from NBA directly?
  - Refine prediciton engine, this will be the primary focus after Flask port/API update is complete

###Attribution and Licensing
#####**MIT License**
#####**&copy; 2015 Kamil Mansuri**

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
