import json
def genderAnalyze(jsonFile)：
	genderFilter = jsonFile.filter(lambda line : "gender" in line ) # 过滤没有填性别的信息
	genderResult = genderFilter.map(lambda s: json.loads(s))
	genderRDD = genderResult.map(lambda s : s["gender"])
	genderkv = genderRDD.map(lambda s: (s, 1))
	genderCount = genderkv.reduceByKey(lambda a, b: a+b)
	return genderCount

def provinceAnalyze(jsonFile)：
	provinceFilter = jsonFile.filter(lambda line : "province" in line )
	provinceResult = provinceFilter.map(lambda s: json.loads(s))
	provinceRDD = provinceResult.map(lambda s : s["province"])
	provincekv = provinceRDD.map(lambda s: (s, 1))
	provinceCount = provincekv.reduceByKey(lambda a, b: a+b)
	maincityCount = provinceCount.filter(lambda line: "北京" in line or "重庆" in line or "上海" in line or "天津" in line or "香港"in line or "澳门" in line) # 直辖市与特区

	cityFilter = jsonFile.filter(lambda line : "province" in line and "city" in line) # 其他城市
	cityResult = cityFilter.map(lambda s: json.loads(s))
	cityRDD = cityResult.map(lambda s : s["province"]+" "+s["city"])
	cityRDD = cityResult.map(lambda s : (s.get("province"), s.get("city")))
	citykv = cityRDD.map(lambda s: (s, 1))
	cityCount = citykv.reduceByKey(lambda a, b: a+b)
	cityFilter = cityCount.filter(lambda a: "重庆" not in a[0] and "海外" not in a[0] and "香港" not in a[0] and "澳门" not in a[0] and "北京" not in a[0] and "上海" not in a[0] and "天津" not in a[0])
	cityCount2 = cityFilter.map(lambda a: (a[0][1], a[1]))
	return maincityCount, cityCount2 
	
def birthAnalyze(jsonFile):
	birthFilter = jsonFile.filter(lambda line : "birthday" in line and  "座" not in line) # 过滤没有填生日的信息以及填星座的信息
	birthResult = birthFilter.map(lambda s: json.loads(s))
	birthRDD = birthResult.map(lambda s : s["birthday"])
	yearRDD = birthRDD.map(lambda s: s.split('-')[0]) # 获取到的生日信息是XXXX-XX-XX格式 取年份
	yearkv = yearRDD.map(lambda s: (s, 1))
	yearCount = yearkv.reduceByKey(lambda a, b: a+b)
	yearSort = yearCount.sortByKey()
	yearSortFilter = yearSort.filter(lambda year: year[0]>='1980' and year[0]<='2004 ') # 获取1980-2004年出生的数据
	yearInt = yearSortFilter.map(lambda x: (int(x[0]), x[1]))
	yearReduce = yearInt.map(lambda a:(a[0]-1980, a[1]))
	yearReduce2 = yearReduce.map(lambda a:(a[0]//5, a[1]))
	yearReduce3 = yearReduce2.reduceByKey(lambda a,b : a+b)
	yearReduceSort = yearReduce3.sortByKey()
	yearReduceSort2 = yearReduceSort.map(lambda a:(a[0]*5+1980, a[1]))
	yearStr = yearReduceSort2.map(lambda a:(str(a[0]), a[1]))
	yearStr2 = yearStr.map(lambda a : (a[0][2:]+"后", a[1]))  # 获取到80后，85后，90后，95后，00后数据
	yearDetail = yearInt.filter(lambda a: a[0]<2002 and a[0]>1993)  # 94年到02年出生的较多，具体统计一下
	return yearStr2, yearDetail