This is written for Ubuntu server. Will run on similar setups such as Raspberry Pi, Debian etc.

#Prerequisites
* Python 3.5 - `add-apt-repository ppa:fkrull/deadsnakes`, `apt-get update`, `apt-get install python3.5` 

* Twitter module - `python3.5 -m pip install twitter`

* speedtest-cli - `git clone https://github.com/sivel/speedtest-cli`

* apache2 (or other webserver) - `apt-get install apache2`

* Automated-speedtests - `git clone https://github.com/spencermehta/automated-speedtests`


#Setup of directories
Move the `website` folder into your webserver directory (Usually `/var/www/html/` if you haven't set up virtual hosts)  or point apache2 to the git clone folder (requirement if you want to set up automatic updates).

Now open `config.py` to edit.  

Set `warning_limit` to the speed below which you want to be tweeted with a warning of a slow connection.  
Set `action_limit` to the speed below which you want your ISP tweeted about your slow connection.  

Set `interval` to the time, in seconds, you want to wait between tests.  

Set `TOKEN` to your Twitter API access token.  
Set `TOKEN_KEY` to your Twitter API access token secret.  
Set `CON_SEC` to your Twitter API consumer key.  
Set `CON_SEC_KEY` to your Twitter API consumer secret.  

Set `action_tweet` to the message you want to be tweeted when your download speed falls below `action_limit`. Use `%p`, `%d`, `%u` and `%img` to add in the results.

Set `warning_tweet` to the message you want to be tweeted when your download speed falls below `warning_limit`. Use `%p`, `%d`, `%u` and `%img` to add in the results.

Note that an image of the results will be automatically added to the end of the tweets and if you don't want any text in the tweeted before or after the results you can leave the variable blank.  

Set `speedtest_cli_path` to the location where your git clone for speedtest-cli is.  
Set `webserver_path` to the location where you placed the 'website' directory - either in your webserver directory (usually `/var/www/` or in the automated-speedtests git clone if you chose to instead point apache2 to that directory.  


#Execution
**Method 1** -  If you are using SSH, open up a screen (`apt-get install screen`, `screen`) and navigate to the directory where `speedtest_bot.py` is located.  
Execute `python3.5 speedtest_bot.py`  
**Method 2** - Follow [these instructions](http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/) to run it as a process.  


The program is now running. Visit the IP address/domain configured for your webserver and you can see the graph for speed tests. The graph will be empty until the first speed test has completed.  

#Graphs
There are three graphs available which you can choose from. To set a different chart as default simply rename the `html` file of the graph you want to `index.html`. The default is a line chart.  

`line.html` - a simple line graph.  
`stackedArea.html` - a stacked area graph.  
`animated.html` - an animated line graph  

#Support
Contact [@spencermehta](http://twitter.com/spencermehta) on Twitter or [the official subreddit](http://reddit.com/r/automated_speedtests) for support.
