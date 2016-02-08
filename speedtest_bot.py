#!/usr/bin/python3.5
import os
import sys
import csv
import datetime
import time
import twitter
import config

def test():
    passed_test = False
    counter = 0
        
    while not passed_test and counter < 2:
        counter += 1
        if counter == 2:
            print("Result below warning limit. Re-running test")
        #Run speedtest-cli
        print("Running speedtest-cli")
        a = os.popen("python " + config.speedtest_cli_path + " --simple --share").read()
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
        out_file = open(config.webserver_path + "/speedresults.csv", 'a')
        writer = csv.writer(out_file)
        writer.writerow((date,p,d,u))
        out_file.close()
                
        d = float(d)
                
        if d >= config.warning_limit:
            passed_test = True
                        
    if not passed_test and counter == 2:
                     
        my_auth = twitter.OAuth(config.TOKEN, config.TOKEN_KEY, config.CON_SEC, config.CON_SEC_KEY)
        twit = twitter.Twitter(auth=my_auth)
        #Tweet ISP if significantly below what you pay fo
        if d < config.action_limit:
            print("Download speed below action limit. Tweeting ISP")
                        
            tweet = config.action_tweet
            if '%p' in tweet:
                tweet = tweet.replace('%p', str(p))
            if '%d' in tweet:
                tweet = tweet.replace('%d', str(d))
            if '%u' in tweet:
                tweet = tweet.replace('%u', str(u))
            if '%img' in tweet:
                tweet = tweet.replace('%img', str(img))

            try:
                twit.statuses.update(status=tweet)
                                              
            except Exception as e:
                print("Error tweeting:", e)
                                
                
        #Tweet you if slightly below what you pay for
        elif d < config.warning_limit:
            print("Download speed below warning limit. Tweeting you")
                             
            tweet = config.warning_tweet
            if '%p' in tweet:
                tweet = tweet.replace('%p', str(p))
            if '%d' in tweet:
                tweet = tweet.replace('%d', str(d))
            if '%u' in tweet:
                tweet = tweet.replace('%u', str(u))
            if '%img' in tweet:
                tweet = tweet.replace('%img', str(img))

            try:
                twit.statuses.update(status=tweet)
                                              
            except Exception as e:
                print("Error tweeting:", e)
                        

while True:
    start_time = time.time()
    test()
    sleep_time = max(config.interval - (time.time() - start_time), 0)
    print("Sleeping for ", round(sleep_time, 0), " seconds")
    time.sleep(sleep_time)
