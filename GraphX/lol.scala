import org.apache.log4j.{Level,Logger}
import org.apache.spark._
import org.apache.spark.graphx._
import org.apache.spark.rdd.RDD
import java.io.PrintWriter


 /**
    * 统计关系出现的次数
    * @param sc
    * @param path：边文件
    * @param num：关系数量阈值
    * @return
    */
def edgeCount(sc:SparkContext,path:String,num:Int) ={
	val textFile = sc.textFile(path)
	val counts = textFile.map(word => (word, 1)).reduceByKey(_ + _).filter(_._2>num)
	// counts.collect().foreach(println)
	counts
}

/**
    * 构建图
    * @param sc
    * @param path1:顶点文件
    * @param path2：边文件
    * @param num：关系数量阈值
    */
def creatGraph(sc:SparkContext,path1:String,path2:String,num:Int) ={
	val hero = sc.textFile(path1)
	val counts = edgeCount(sc,path2,num)

	val verticesAll = hero.map { line =>
	  val fields = line.split(' ')
	  (fields(0).toLong, fields(1))
	}

	val edges = counts.map { line =>
	  val fields = line._1.split(" ")
	  Edge(fields(0).toLong, fields(1).toLong, line._2)//起始点ID必须为Long，最后一个是属性，可以为任意类型
	}
	val graph_tmp = Graph.fromEdges(edges,1L)
	//    经过过滤后有些顶点是没有边，所以采用leftOuterJoin将这部分顶点去除
	val vertices = graph_tmp.vertices.leftOuterJoin(verticesAll).map(x=>(x._1,x._2._2.getOrElse("")))
	val graph = Graph(vertices,edges)

	graph
}

  /**
    * 输出为gexf格式
    * @param g：图
    * @tparam VD
    * @tparam ED
    * @return
    */
def toGexf[VD,ED](g:Graph[VD,ED]) ={
	"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" +
	  "<gexf xmlns=\"http://www.gexf.net/1.2draft\" version=\"1.2\">\n" +
	  " <graph mode=\"static\" defaultedgetype=\"directed\">\n  " +
	  "<nodes>\n " +
	  g.vertices.map(v => "  <node id=\""+v._1+"\" label=\""+v._2+"\" />\n").collect().mkString+
	  "</nodes>\n  "+
	  "<edges>\n"+
	  g.edges.map(e => "  <edge source=\""+e.srcId+"\" target=\""+e.dstId+"\" weight=\""+e.attr+"\"/>\n").
		collect().mkString+
	  "</edges>\n        </graph>\n      </gexf>"

}
Logger.getLogger("org.apache.spark").setLevel(Level.WARN)
Logger.getLogger("org.eclipse.jetty.server").setLevel(Level.OFF)
//设置运行环境
val conf = new SparkConf().setAppName("SimpleGraphX").setMaster("172.19.240.187")
val sc = new SparkContext(conf)
val graph = creatGraph(sc,"hdfs://master:9000/user/hadoop/hero.txt","hdfs://master:9000/user/hadoop/relation.txt",0)
val pw1 = new PrintWriter("hero_graph.gexf")
pw1.write(toGexf(graph))
   
val ranks = graph.pageRank(0.0001).vertices
val hero = sc.textFile("hdfs://master:9000/user/hadoop/hero.txt")
val heroes = hero.map { line =>
	  val fields = line.split(' ')
	  (fields(0).toLong,  fields(1), fields(2), fields(3))
}
val heroes = hero.map { line =>
	  val fields = line.split(' ')
	  (fields(0).toLong,  fields(2))
}
val ranksByUsername = heroes.join(ranks).map {  case (id, (name, rank)) => (name, rank)}
val ranksByrank = heroes.join(ranks).map {  case (id, (name, rank)) => (rank, name)}
println(ranksByUsername.collect().mkString("/"))
println(ranksByrank.collect().mkString("\n"))
val edgecount = edgeCount(sc,"hdfs://master:9000/user/hadoop/relation.txt",0)
