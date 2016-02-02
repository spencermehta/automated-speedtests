#!/usr/bin/python
import os
import sys
import csv
import datetime
import time
import sched
import twitter


#Download speed below which you are tweeted with warning of slow connection
warning_limit = 60
#Download speed below which your ISP is tweeted as well as you about slow connection
action_limit = 50

def test(sc):
        #Run speedtest-cli
        print("Running speedtest-cli")
        a = os.popen("python /path/to/speedtest_cli.py --simple --share").read()
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
                p = lines[0][6:11]
                d = lines[1][10:14]
                u = lines[2][8:12]
                img = lines[3][15:]
        print(date, p, d, u)
        
        #Save the data to file for local network plotting
        out_file = open('/path/to/webserver/data.csv', 'a')
        writer = csv.writer(out_file)
        writer.writerow((date,p,d,u))
        out_file.close()
        
        d = float(d)
        
        if d < warning_limit:
                print("UNEXPECTED RESULT - re-running test")
                retest(sc)
        else:
                sc.enter(1800, 1, test, (sc,))



def retest(sc):
        #Run speedtest-cli
        print("Running speedtest-cli")
        a = os.popen("python /path/to/speedtest_cli.py --simple --share").read()
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
                p = lines[0][6:11]
                d = lines[1][10:14]
                u = lines[2][8:12]
                img = lines[3][15:]
        print(date, p, d, u)
        
        #Save the data to file for local network plotting
        out_file = open('/path/to/webserver/data.csv', 'a')
        writer = csv.writer(out_file)
        writer.writerow((date,p,d,u))
        out_file.close()
        
        
        #Connect to twitter
        TOKEN=""
        TOKEN_KEY=""
        CON_SEC=""
        CON_SEC_KEY=""
        
        my_auth = twitter.OAuth(TOKEN,TOKEN_KEY,CON_SEC,CON_SEC_KEY)
        twit = twitter.Twitter(auth=my_auth)
        
        d = float(d)
        u = float(u)
        
        #Tweet ISP if significantly below what you pay for
        if d < action_limit:
                print("Download speed below action limit. Tweeting ISP")
                try:
                        tweet="@ISP @me My internet has fallen significantly below what I pay for, now at " + str(d) + "down\\" + str(u) + "up - " + str(img)
                        twit.statuses.update(status=tweet)
                except Exception as e:
                        print("Error tweeting:", e)
                        
        
        #Tweet you if slightly below what you pay for
        elif d < warning_limit:
                print("Download speed below warning limit. Tweeting you")
                try:
                        tweet="@me Your internet speed has fallen below acceptable levels, currently at " + str(d) + "down\\" + str(u) + "up - " + str(img)
                        twit.statuses.update(status=tweet)
                except Exception as e:
                        print("Error tweeting:", e)
        
        sc.enter(1800, 1, test, (sc,))



s = sched.scheduler(time.time, time.sleep)
s.enter(1800, 1, test, (s,))
s.run()