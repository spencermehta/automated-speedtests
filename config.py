#Download speed below which you are tweeted with warning of slow connection
warning_limit = 70

#Download speed below which your ISP is tweeted as well as you about slow connection
action_limit = 50

#Interval between test starts
interval = 1800

#Twitter API
TOKEN=""  #Access Token
TOKEN_KEY=""  #Access Token Secret
CON_SEC=""  #Consumer Key
CON_SEC_KEY=""  #Consumer Secret

#Tweet content
action_tweet1 = "@ISP @me My internet has fallen significantly below what I pay for, now at "  #Before speeds
action_tweet2 = ""  #After speeds

warning_tweet1 = "@me Your internet has fallen below the warning limits, now at "  #Before speeds
warning_tweet2 = ""  #After speeds

#Path to speedest-cli module
speedtest_cli_path = "/path/to/speedtest_cli.py"
#Path to webserver
webserver_path = "/path/to/website"  #Don't put / at end of this path