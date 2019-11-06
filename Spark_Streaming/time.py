import os
import time
import json
fcomments = open("Comments.json"）
comment = fcomments.read()

with open("Tweets.json") as fhandle:
    res = []
    for line in fhandle:
        line = line.strip()
		line = json.loads(line)
		
		weibo_url = 
        res.append(line)
        if (len(res)%100 ==0):
            writestr = '\n'.join(res)
            res = []
            time_log = int(round(time.time() * 1000))
            filename = "log/" + str(time_log)+".txt"
            fwrite = open(filename, "w")
            fwrite.write(writestr)
            fwrite.close()
            os.system("/usr/local/hadoop/bin/hadoop fs -put ~/Downloads/"+filename+" /user/hadoop/streaming/comments")
            time.sleep(1)