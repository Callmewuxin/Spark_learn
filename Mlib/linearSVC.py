from pyspark.ml.classification import LinearSVC
lsvc = LinearSVC(maxIter=100, regParam=0.3).setLabelCol("indexedLabel").setFeaturesCol("indexedFeatures")
pipelinedClassifier = Pipeline().setStages([labelIndexer, featureIndexer, lsvc, labelConverter])
modelClassifier = pipelinedClassifier.fit(trainingData)

# 进行预测
predictionsClassifier = modelClassifier.transform(testData)
evaluatorClassifier = MulticlassClassificationEvaluator().setLabelCol("indexedLabel").setPredictionCol("prediction").setMetricName("accuracy")
 
accuracy = evaluatorClassifier.evaluate(predictionsClassifier)
 
print("Test Accuracy = ", accuracy)
# IDF Test Accuracy =  0.6225473894246758
# word2vec Accuracy =  0.7060766182298547