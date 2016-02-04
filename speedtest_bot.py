#!/usr/bin/python3.5
import os
import sys
import csv
import datetime
import time
import twitter



###Variables
#Download speed below which you are tweeted with warning of slow connection
warning_limit = 60
#Download speed below which your ISP is tweeted as well as you about slow connection
action_limit = 50
#Interval between test starts (seconds)
interval = 1800

#Twitter API connection
TOKEN=""
TOKEN_KEY=""
CON_SEC=""
CON_SEC_KEY=""

#Tweet content
action_tweet = "@ISP @me My internet has fallen significantly below what I pay for, now at"
warning_tweet = "@me Your internet has fallen below the warning limits, now at"

#Path to speedest-cli module
speedtest_cli_path = "/path/to/speedtest_cli.py"
webserver_path = "/path/to/webserver" #Don't put / at end of this path


def test():
        passed_test = False
        counter = 0
        
        while not passed_test and counter < 2:
                counter += 1
                if counter == 2:
                        print("Result below warning limit. Re-running test")
                #Run speedtest-cli
                print("Running speedtest-cli")
                a = os.popen("python " + speedtest_cli_path + " --simple --share").read()
                print("Ran speedtest-cli")
                
                lines = a.split("\n")
                print(a)
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
                
                #Set speeds to 0 if speedtest-cli couldn't connect
                if "Cannot" in a:
                        p = 100
                        d = 0
                        u = 0
                        
                #Extract values for ping, download and upload
                else:
                        p = lines[0].split(' ')[1]
                        d = lines[1].split(' ')[1]
                        u = lines[2].split(' ')[1]
                        img = lines[3].split(' ')[2]
                print(date, p, d, u)
                
                #Save the data to file for local network plotting
                out_file = open(webserver_path + "/data.csv", 'a')
                writer = csv.writer(out_file)
                writer.writerow((date,p,d,u))
                out_file.close()
                
                d = float(d)
                
                if d >= warning_limit:
                        passed_test = True
                        
        if not passed_test and counter == 2:
                     
                     
                my_auth = twitter.OAuth(TOKEN,TOKEN_KEY,CON_SEC,CON_SEC_KEY)
                twit = twitter.Twitter(auth=my_auth)
                #Tweet ISP if significantly below what you pay fo
                if d < action_limit:
                        print("Download speed below action limit. Tweeting ISP")
                        try:
                                tweet = action_tweet + " " + str(d) + "down\\" + str(u) + "up - " + str(img)
                                twit.statuses.update(status=tweet)
                        except Exception as e:
                                print("Error tweeting:", e)
                                
                
                #Tweet you if slightly below what you pay for
                elif d < warning_limit:
                        print("Download speed below warning limit. Tweeting you")
                        try:
                                tweet = warning_tweet + " " + str(d) + "down\\" + str(u) + "up - " + str(img)
                                twit.statuses.update(status=tweet)
                        except Exception as e:
                                print("Error tweeting:", e)
                        

while True:
        start_time = time.time()
        test()
        sleep_time = max(interval - (time.time() - start_time), 0)
        #print("Sleeping for ", round(sleep_time, 0), " seconds")
        time.sleep(sleep_time)
