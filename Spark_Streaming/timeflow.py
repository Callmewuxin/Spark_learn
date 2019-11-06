from pyspark.streaming import StreamingContext
from pymongo import MongoClient
ssc = StreamingContext(sc, 5)
textFile = ssc.textFileStream('hdfs://master:9000/user/hadoop/streaming/comments/')
def updateFunc(new_values, last_sum):
        return sum(new_values) + (last_sum or 0)
ssc.checkpoint("hdfs://master:9000/user/hadoop/streaming/result/")
initialStateRDD = sc.parallelize([("0-10", 1), ("10-20", 1)])
timeRDD = textFile.flatMap(lambda x:x.split(" "))
minuteRDD = timeRDD.map(lambda x:int(float(x)))
tenRDD = minuteRDD.map(lambda x:x//10)
tenFilter = tenRDD.filter(lambda x:x<12)
tenkv = tenFilter.map(lambda s:(str(s*10) + "-" + str((s+1)*10) , 1))
tencount = tenkv.updateStateByKey(updateFunc, initialRDD=initialStateRDD)
tencount.pprint()
def dbfunc(records):
	conn = MongoClient('localhost', 27017)
	db = conn.spark
	set = db.result
	def doinsert(p):
		set.insert({"time":str(p[0]), "count":str(p[1])})

	for item in records:
		doinsert(item)
 
def func(rdd):
	repartitionedRDD = rdd.repartition(3)
	repartitionedRDD.foreachPartition(dbfunc)
 
tencount.foreachRDD(func)
ssc.start()
ssc.awaitTermination()
'''
tencount.saveAsTextFiles("hdfs://master:9000/user/hadoop/streaming/result/output.txt")
tencount.pprint()
ssc.start()
ssc.awaitTermination()
'''