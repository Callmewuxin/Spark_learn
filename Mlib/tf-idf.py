from pyspark.ml.linalg import Vector,Vectors
from pyspark.sql import Row
from pyspark.ml import Pipeline
from pyspark.ml.feature import IndexToString,StringIndexer,VectorIndexer
from pyspark.ml.classification import MultilayerPerceptronClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import HashingTF,IDF,Tokenizer

import jieba
import re
import random
from pyspark.sql.functions import lit
from pyspark.sql import SparkSession

	
def tokenize(text):
    """
    带有语料清洗功能的分词函数
    """
    text = re.sub("\{%.+?%\}", " ", text)           # 去除 {%xxx%} (地理定位, 微博话题等)
    text = re.sub("回复@\S+:", '', text)            # 去除回复@
    text = re.sub("@.+?( |$)", " ", text)           # 去除 @xxx (用户名)
    
    text = re.sub("【.+?】", " ", text)              # 去除 【xx】 (里面的内容通常都不是用户自己写的)
    icons = re.findall("\[.+?\]", text)             # 提取出所有表情图标
    text = re.sub("\[.+?\]", "IconMark", text)      # 将文本中的图标替换为`IconMark`
    
    tokens = []
    for k, w in enumerate(jieba.lcut(text)):
        w = w.strip()
        if "IconMark" in w:                         # 将IconMark替换为原图标
            for i in range(w.count("IconMark")):
                tokens.append(icons.pop(0))
        elif w and w != '\u200b' and w.isalpha():   # 只保留有效文本
                tokens.append(w)
    return tokens



def load_corpus(path):
    """
    加载语料库
    """
    data = []
    with open(path, "r", encoding="utf8") as f:
        for line in f:
            content = tokenize(line)             # 分词
            if len(content) !=0:
                data.append((line, content))
    return data

def load_corpus_2(path):
    """
    加载语料库
    """
    data = []
    with open(path, "r", encoding="utf8") as f:
        for line in f:
            [_, seniment, line] = line.split(",", 2)
            content = tokenize(line)             # 分词
            if len(content) !=0:
                data.append((line, content, int(seniment)))
    return data

	
sun_data = load_corpus("/home/hadoop/Downloads/sun.txt")
sun_data = random.sample(sun_data, 1000)
sun_df = spark.createDataFrame(sun_data, ["text", "word"])
sun_df  = sun_df.withColumn("label", lit(0))
# 获取数据并转为dataframe

labeled_data = load_corpus_2("/home/hadoop/Downloads/weibo_train.txt")
labeled_df = spark.createDataFrame(labeled_data, ["text", "word", "label"])


df1 = labeled_df.withColumn("set", lit("labeled"))
df2 = sun_df.withColumn("set", lit("sun"))
hebing = df1.unionAll(df2)

# TF-IDF
hashingTF = HashingTF(inputCol="word", outputCol="rawFeatures", numFeatures=100)
featurizedData = hashingTF.transform(hebing)

idf = IDF(inputCol="rawFeatures", outputCol="features")
idfModel = idf.fit(featurizedData)
rescaledData = idfModel.transform(featurizedData)

labeled_idf = rescaledData.filter(rescaledData.set =="labeled")
sun_idf = rescaledData.filter(rescaledData.set == "sun") 


# 构建索引