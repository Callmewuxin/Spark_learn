from pyspark.ml.linalg import Vector,Vectors
from pyspark.sql import Row
from pyspark.ml import Pipeline
from pyspark.ml.feature import IndexToString,StringIndexer,VectorIndexer
from pyspark.ml.classification import MultilayerPerceptronClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
def f(x):
    rel = {}
    t = x[:-1]
    t = [float(xx) for xx in t]
    rel['features'] = Vectors.dense(t)
    rel['label'] = str(x[-1])
    return rel
# 获取数据并转为dataframe
data = spark.sparkContext.textFile("file:///home/hadoop/Downloads/weibo_sentiment.txt").map(lambda line: line.split(' ')).map(lambda p: Row(**f(p))).toDF()
# 构建索引
labelIndexer = StringIndexer().setInputCol("label").setOutputCol("indexedLabel").fit(labeled_w2v)
featureIndexer = VectorIndexer().setInputCol("word2vec").setOutputCol("indexedFeatures").fit(labeled_w2v)

# 这里我们设置一个labelConverter，目的是把预测的类别重新转化成字符型的。
labelConverter = IndexToString().setInputCol("prediction").setOutputCol("predictedLabel").setLabels(labelIndexer.labels)
# 接下来，我们把数据集随机分成训练集和测试集，其中训练集占70%。
trainingData, testData = labeled_w2v.randomSplit([0.7, 0.3])
layers = [100, 16, 2]
trainer = MultilayerPerceptronClassifier(maxIter=100, layers=layers, blockSize=128, seed=1234).setLabelCol("indexedLabel").setFeaturesCol("indexedFeatures")
pipelinedClassifier = Pipeline().setStages([labelIndexer, featureIndexer, trainer, labelConverter])
modelClassifier = pipelinedClassifier.fit(trainingData)

# 进行预测
predictionsClassifier = modelClassifier.transform(testData)
evaluatorClassifier = MulticlassClassificationEvaluator().setLabelCol("indexedLabel").setPredictionCol("prediction").setMetricName("accuracy")

accuracy = evaluatorClassifier.evaluate(predictionsClassifier)
print("Accuracy = ", accuracy)

# IDF Accuracy =  0.5942357512953368
# word2vec Accuracy =  0.737410071942446


sunPrediction = modelClassifier.transform(sun_w2v)
sunPrediction.filter(sunPrediction.prediction==1).count()
# 0: 430
# 1: 570