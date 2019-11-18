from pyspark.sql import Row,functions
from pyspark.ml.linalg import Vector,Vectors
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import Pipeline
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer,HashingTF, Tokenizer
from pyspark.ml.classification import LogisticRegression,LogisticRegressionModel,BinaryLogisticRegressionSummary, LogisticRegression

from pyspark import SparkContext 
from pyspark.sql import SQLContext

# def f(x):
    # rel = {}
    # t = x[:-1]
    # t = [float(xx) for xx in t]
    # rel['features'] = Vectors.dense(t)
    # rel['label'] = str(x[-1])
    # return rel
# # 获取数据并转为dataframe
# data = spark.sparkContext.textFile("file:///home/hadoop/Downloads/weibo_sentiment.txt").map(lambda line: line.split(' ')).map(lambda p: Row(**f(p))).toDF()
# # 构建索引


labelIndexer = StringIndexer().setInputCol("label").setOutputCol("indexedLabel").fit(labeled_idf)
featureIndexer = VectorIndexer().setInputCol("features").setOutputCol("indexedFeatures").fit(labeled_idf)

trainingData, testData = labeled_idf.randomSplit([0.7,0.3])  # 划分数据集
#  设置logistic的参数 迭代轮次100，正则项0.3
lr =  LogisticRegression().setLabelCol("indexedLabel").setFeaturesCol("indexedFeatures").setMaxIter(100).setRegParam(0.3).setElasticNetParam(0.8).setFamily("multinomial")
print("LogisticRegression parameters:\n" + lr.explainParams())

# 这里我们设置一个labelConverter，目的是把预测的类别重新转化成字符型的。
labelConverter = IndexToString().setInputCol("prediction").setOutputCol("predictedLabel").setLabels(labelIndexer.labels)

# ​ 构建pipeline，设置stage，然后调用fit()来训练模型。
lrPipeline =  Pipeline().setStages([labelIndexer, featureIndexer, lr, labelConverter])
lrPipelineModel = lrPipeline.fit(trainingData)

# pipeline本质上是一个Estimator，当pipeline调用fit()的时候就产生了一个PipelineModel，本质上是一个Transformer。然后这个PipelineModel就可以调用transform()来进行预测，生成一个新的DataFrame，即利用训练得到的模型对测试集进行验证。
lrPredictions = lrPipelineModel.transform(testData)

# 最后我们可以输出预测的结果，其中select选择要输出的列，collect获取所有行的数据，用foreach把每行打印出来。其中打印出来的值依次分别代表该行数据的真实分类和特征值、预测属于不同分类的概率、预测的分类。
preRel = lrPredictions.select("predictedLabel", "label", "features", "probability").collect()
for item in preRel:
    print(str(item['label'])+','+str(item['features'])+'-->prob='+str(item['probability'])+',predictedLabel'+str(item['predictedLabel']))

# 创建一个MulticlassClassificationEvaluator实例，用setter方法把预测分类的列名和真实分类的列名进行设置；然后计算预测准确率和错误率。	
evaluator = MulticlassClassificationEvaluator().setLabelCol("indexedLabel").setPredictionCol("prediction")
lrAccuracy = evaluator.evaluate(lrPredictions)
print("Accuracy = " , lrAccuracy)

# 通过model来获取我们训练得到的逻辑斯蒂模型。
lrModel = lrPipelineModel.stages[2]
trainingSummary = lrModel.summary
objectiveHistory = trainingSummary.objectiveHistory
for item in objectiveHistory:
	print(item)
	
# IDF Accuracy =  0.3943602948042552
# word2vec Accuracy =  0.389215853985014
