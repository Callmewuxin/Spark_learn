from pyspark.ml.linalg import Vector,Vectors
from pyspark.sql import Row
from pyspark.ml import Pipeline
from pyspark.ml.feature import IndexToString,StringIndexer,VectorIndexer

def f(x):
    rel = {}
    t = x[2:]
    t = [float(xx) for xx in t]
    rel['features'] = Vectors.dense(t)
    rel['label'] = str(x[1])
    return rel
# 获取数据并转为dataframe
# 构建索引
labelIndexer = StringIndexer().setInputCol("label").setOutputCol("indexedLabel").fit(labeled_w2v)
featureIndexer = VectorIndexer().setInputCol("word2vec").setOutputCol("indexedFeatures").fit(labeled_w2v)

# 这里我们设置一个labelConverter，目的是把预测的类别重新转化成字符型的。
labelConverter = IndexToString().setInputCol("prediction").setOutputCol("predictedLabel").setLabels(labelIndexer.labels)
# 接下来，我们把数据集随机分成训练集和测试集，其中训练集占70%。
trainingData, testData = labeled_w2v.randomSplit([0.7, 0.3])

# 导入所需要的包
from pyspark.ml.classification import DecisionTreeClassificationModel,DecisionTreeClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# 训练决策树模型,这里我们可以通过setter的方法来设置决策树的参数，也可以用ParamMap来设置（具体的可以查看spark mllib的官网）。具体的可以设置的参数可以通过explainParams()来获取。
dtClassifier = DecisionTreeClassifier().setLabelCol("indexedLabel").setFeaturesCol("indexedFeatures")

# 在pipeline中进行设置
pipelinedClassifier = Pipeline().setStages([labelIndexer, featureIndexer, dtClassifier, labelConverter])

# 训练决策树模型
modelClassifier = pipelinedClassifier.fit(trainingData)

# 进行预测
predictionsClassifier = modelClassifier.transform(testData)

#查看部分预测的结果
predictionsClassifier.select("predictedLabel", "label", "features").show(20)


evaluatorClassifier = MulticlassClassificationEvaluator().setLabelCol("indexedLabel").setPredictionCol("prediction").setMetricName("accuracy")
 
accuracy = evaluatorClassifier.evaluate(predictionsClassifier)
 
print("Accuracy = ", accuracy)
 
treeModelClassifier = modelClassifier.stages[2]
 
print("Learned classification tree model:\n" + str(treeModelClassifier.toDebugString))

# IDF Accuracy =  0.5877590673575129
# word2vec Accuracy 0.6681252103668799