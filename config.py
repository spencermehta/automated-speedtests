#Download speed below which you are tweeted with warning of slow connection
warning_limit = 60

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
action_tweet = "@ISP @me My internet has fallen significantly below what I pay for, now at"
warning_tweet = "@me Your internet has fallen below the warning limits, now at"

#Path to speedest-cli module
speedtest_cli_path = "/path/to/speedtest_cli.py"
webserver_path = "/path/to/webserver" #Don't put / at end of this path