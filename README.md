# automated-speedtests  

Automatically performs speedtests at custom intervals, graphs data and tweets when speeds fall below set thresholds  

Written for Ubuntu server. Will run on similar setups such as Raspberry Pi, Debian etc. and with some manual configuration OSX and Windows.  




##Prerequisites
* Python 3.5 - `add-apt-repository ppa:fkrull/deadsnakes`, `apt-get update`, `apt-get install python3.5` 

* Twitter module - `python3.5 -m pip install twitter`

* apache2 (or other webserver) - `apt-get install apache2`

* Automated-speedtests (this program) - `git clone https://github.com/spencermehta/automated-speedtests`




##Setup

###Config
Open `config.py` in an editor.  

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

**You shouldn't need to edit the following if you're just following this guide**  
Set `speedtest_cli_path` to the location of speedtest-cli.py.  
Set `webserver_path` to the'website' directory.  


###Website
Follow the wiki instructions below if you have no website running on the machine. Otherwise follow [these instructions](https://www.digitalocean.com/community/tutorials/how-to-set-up-apache-virtual-hosts-on-ubuntu-14-04-lts) to configure virtual hosts (multiple websites running on one machine).  

Execute `vi /etc/apache2/sites-enabled/000-default.conf`  
Change the path of `DocumentRoot` to where your git clone of `automated-speedtests` is - example: `DocumentRoot /home/spencer/automated-speedtests/website/`  
Save and exit the file then restart apache: `service apache2 restart`  




##Execution
If you are using SSH, open up a screen (`apt-get install screen`, `screen`) and navigate to the directory where `speedtest_bot.py` is located.  
Execute `python3.5 speedtest_bot.py`  

Or you can follow [these instructions](http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/) to run it as a process.  


The program is now running. Visit the IP address/domain configured for your webserver and you can see the graph for speed tests. The graph will be empty until the first speed test has completed.  




#Support
Contact [@spencermehta](http://twitter.com/spencermehta) on Twitter or [the official subreddit](http://reddit.com/r/automated_speedtests) for support.
