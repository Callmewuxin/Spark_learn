import json
import jieba
import re
def commentAnalyze(jsonFile):
	commentFilter = jsonFile.filter(lambda line : "content" in line )
	commentResult = commentFilter.map(lambda s: json.loads(s))
	commentRDD = commentResult.map(lambda s : s["content"])

	# 过滤
	commentFilter1 = commentRDD.filter(lambda a: "图片评论" not in a)  # 去除图片评论
	commentFilter2 = commentFilter1.map(lambda a: re.sub("回复@\S+:", '', a)) # 删除回复前缀 
	commentFilter3 = commentFilter2.map(lambda a: re.sub("\[\S*?\]", '',a)) # 删除表情
	commentFilter4 = commentFilter3.filter(lambda a: a!="")  # 删除空字符串

	comment_hb = commentFilter4.reduce(lambda a,b: a+" "+b)
	comment_jieba = list(jie.cut(comment_hb))  # spark分词太慢 先合并所有字符串再分词
	commentRDD = sc.parallelize(comment_hb)   #分词结果创建RDD
	commentRDDFilter = commentRDD.filter(lambda a: " "!=a)
	commentkv = commentRDDFilter.map(lambda a: (a, 1))
	commentCount = commentkv.reduceByKey(lambda a,b:a+b)
	commentCountVal = commentCount.map(lambda a:(a[1], a[0]))
	commentSort = commentCountVal.sortByKey(ascending=False)