import os
import datetime
import json
import time
from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
db = conn.spark #连接mydb数据库，没有则自动创建
tweets = db.tweets
comments = db.comments
def timediff(timeStra, timeStrb):
    # print(timeStra, timeStrb)
    if len(timeStra) == 16:
        timeStra+=":00"
    if len(timeStrb) == 16:
        timeStrb+=":00"
    # print(timeStra, timeStrb)
    ta = time.strptime(timeStra, "%Y-%m-%d %H:%M:%S")
    tb = time.strptime(timeStrb, "%Y-%m-%d %H:%M:%S")
    y,m,d,H,M,S = ta[0:6]
    dataTimea=datetime.datetime(y,m,d,H,M,S)
    y,m,d,H,M,S = tb[0:6]
    dataTimeb=datetime.datetime(y,m,d,H,M,S)
    secondsDiff=(dataTimea-dataTimeb).total_seconds()
    #两者相加得转换成分钟的时间差
    minutesDiff=round(secondsDiff/60,1)
    return minutesDiff



cnt = 0
result = []
for line in tweets.find():
    cnt = cnt + 1
    res = []
    weibo_url = None
    weibo_time = None
    if "weibo_url" in line:
        weibo_url = line["weibo_url"]
    if "created_at" in line:
        weibo_time = line["created_at"]
    if weibo_time is None or weibo_url is None or weibo_time=="" or weibo_url=="":
        continue
    for comment in comments.find({"weibo_url":weibo_url}):
        comment_time = None
        comment_weibo = None
        if "weibo_url" not in comment:
            continue    
        comment_weibo = comment["weibo_url"]
        if comment_weibo != weibo_url:
            continue
        if "created_at" not in comment:
                continue
        comment_time = comment["created_at"]
        if comment_time == "":
            continue
        minutes = timediff(comment_time, weibo_time)
        res.append(minutes)
    res = [str(t) for t in res]
    res = ' '.join(res)
    result.append(res)
    writestr = '\n'.join(result)
    print(cnt)
    if cnt%10==0:
        result = []
        time_log = int(round(time.time() * 1000))
        filename = "log/" + str(time_log)+".txt"
        fwrite = open(filename, "w")
        fwrite.write(writestr)
        fwrite.close()
        os.system("/usr/local/hadoop/bin/hadoop fs -put ~/Downloads/"+filename+" /user/hadoop/streaming/comments")
        # time.sleep(1)