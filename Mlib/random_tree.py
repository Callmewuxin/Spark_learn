from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

rf = RandomForestClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures", numTrees=10)
pipelinedClassifier = Pipeline().setStages([labelIndexer, featureIndexer, rf, labelConverter])

modelClassifier = pipelinedClassifier.fit(trainingData)

# 进行预测
predictionsClassifier = modelClassifier.transform(testData)
evaluatorClassifier = MulticlassClassificationEvaluator().setLabelCol("indexedLabel").setPredictionCol("prediction").setMetricName("accuracy")
 
accuracy = evaluatorClassifier.evaluate(predictionsClassifier)
 
print("Accuracy = ", accuracy)
# IDF Accuracy =  0.6049222797927462
# word2vec Accuracy =  0.6967351060249074