#!/usr/bin/python3.5
import os
import sys
import csv
import datetime
import time
import twitter
import json



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



with open('/home/spencer/projects/autospeed/config.json', 'r') as f:
        config = json.load(f)


def speedTest(ping, down, up, img, tests):
        print("\nConducting speed test...")
        speedTestOutput = os.popen("python " + config['speedtestPath'] + " --simple --share").read()
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
        fileSpeedResults = open(config['webserverPath'] + "/speedresults.csv", 'a')
        writer = csv.writer(fileSpeedResults)
        writer.writerow((date, ping, down, up))
        fileSpeedResults.close()

        ping = float(ping)
        down = float(down)
        up = float(up)

        tests += 1

        return(ping, down, up, img, tests)        



def tweet(tweetmsg, ping, down, up, img):
        #Twitter API connection
        api = twitter.Api(consumer_key=config['twitter']['consumerKey'],
                          consumer_secret=config['twitter']['consumerSecret'],
                          access_token_key=config['twitter']['token'],
                          access_token_secret=config['twitter']['tokenSecret'])

        print("Tweeting...")
        
        if '%p' in tweetmsg:
                tweetmsg = tweetmsg.replace('%p', str(ping))
        if '%d' in tweetmsg:
                tweetmsg = tweetmsg.replace('%d', str(down))
        if '%u' in tweetmsg:
                tweetmsg = tweetmsg.replace('%u', str(up))
        if '%img' in tweetmsg:
                tweetmsg = tweetmsg.replace('%img', str(img))

        try:
                print(tweetmsg)
                status = api.PostUpdate(tweetmsg)
                print("Tweeted successfully")

        except Exception as e:
                print("Error tweeting:", e)



def sleepInterval(start_time):
        sleep_time = max(float(config['interval']) - (time.time() - start_time), 0)
        print("\nSleeping for ", round(sleep_time, 0), " seconds")
        time.sleep(sleep_time)



tweeting = str(config['twitter']['tweeting'])
tweets = config['thresholds']

while True:
        start_time = time.time()
        ping, down, up, img, tests = speedTest(ping, down, up, img, tests)
        
        if tweeting == 'enabled':
                for (threshold, tweetmsg) in tweets.items():
                        threshold = float(threshold)
                        if down < threshold:
                               tweetmsg = tweetmsg[0]
                
                tweet(tweetmsg, ping, down, up, img)
        sleepInterval(start_time)
#                print("***Unexpected result. Repeating speed test***")