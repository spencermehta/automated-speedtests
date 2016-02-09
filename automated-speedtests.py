#!/usr/bin/python3.5
import os
import sys
import csv
import datetime
import time
import twitter
import config



print("""
      
-----------------------------
Starting automated-speedtests
-----------------------------
""")



ping = False
down = False
up = False
img = False
tests = 0



def speedTest(ping, down, up, img, tests):
        print("\nConducting speed test...")
        speedTestOutput = os.popen("python " + config.speedtest_cli_path + " --simple --share").read()
        print("Speed test complete")

        lines = speedTestOutput.split("\n")
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        
        print("\n------------------------------------------------------")
        print(date + "\n" + speedTestOutput + "------------------------------------------------------\n")
        #Set speeds to 0 if speedtest-cli couldn't connect
        if "Cannot" in speedTestOutput:
            ping = 100
            down = 0
            up = 0
            img = "noimg"

        #Extract values for ping, download and upload
        else:
            ping = lines[0].split(' ')[1]
            down = lines[1].split(' ')[1]
            up = lines[2].split(' ')[1]
            img = lines[3].split(' ')[2]


        #Save the data to file for local network plotting
        fileSpeedResults = open(config.webserver_path + "/speedresults.csv", 'a')
        writer = csv.writer(fileSpeedResults)
        writer.writerow((date, ping, down, up))
        fileSpeedResults.close()

        ping = float(ping)
        down = float(down)
        up = float(up)

        tests += 1

        return(ping, down, up, img, tests)        



def tweet(tweetcontent, ping, down, up, img):
        #Twitter API connection
        my_auth = twitter.OAuth(config.TOKEN, config.TOKEN_KEY, config.CON_SEC, config.CON_SEC_KEY)
        twit = twitter.Twitter(auth=my_auth)

        print("Tweeting...")

        tweet = tweetcontent
        if '%p' in tweet:
            tweet = tweet.replace('%p', str(ping))
        if '%d' in tweet:
            tweet = tweet.replace('%d', str(down))
        if '%u' in tweet:
            tweet = tweet.replace('%u', str(up))
        if '%img' in tweet:
            tweet = tweet.replace('%img', str(img))

        try:
            twit.statuses.update(status=tweet)
            print(tweet)
            print("Tweeted successfully")

        except Exception as e:
            print("Error tweeting:", e)



def sleep(start_time):
    sleep_time = max(config.interval - (time.time() - start_time), 0)
    print("\nSleeping for ", round(sleep_time, 0), " seconds")
    time.sleep(sleep_time)




while True:
    start_time = time.time()
        
    ping, down, up, img, tests = speedTest(ping, down, up, img, tests)
    

    if down >= config.action_limit:
        sleep(start_time)
    elif down < config.action_limit and tests > 1:
        tweet(config.action_tweet, ping, down, up, img)
        sleep(start_time)
    elif down < config.warning_limit and tests > 1:
        tweet(config.warning_tweet, ping, down, up, img)
        sleep(start_time)
    else:
        print("***Unexpected result. Repeating speed test***")
