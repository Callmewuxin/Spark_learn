from pyspark.ml.feature import Word2Vec
word2Vec = Word2Vec(vectorSize=100, minCount=0, inputCol="word", outputCol="word2vec")
word2Vecmodel = word2Vec.fit(hebing)
hebing_w2v = word2Vecmodel.transform(hebing)
labeled_w2v = hebing_w2v.filter(hebing_w2v.set =="labeled")
sun_w2v = hebing_w2v.filter(hebing_w2v.set == "sun") 