from pyspark.streaming import StreamingContext
ssc = StreamingContext(sc, 1)
lines = ssc.textFileStream('hdfs://master:9000/user/hadoop/streaming/comments/')
result = genderAnalyze(lines)
ssc.start()