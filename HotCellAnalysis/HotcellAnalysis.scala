package cse512

import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions._
import scala.math.abs

object HotcellAnalysis {
  Logger.getLogger("org.spark_project").setLevel(Level.WARN)
  Logger.getLogger("org.apache").setLevel(Level.WARN)
  Logger.getLogger("akka").setLevel(Level.WARN)
  Logger.getLogger("com").setLevel(Level.WARN)

  def runHotcellAnalysis(spark: SparkSession, pointPath: String): DataFrame = {
    var pickupInfo = spark.read.format("com.databricks.spark.csv").option("delimiter",";").option("header","false").load(pointPath)
    pickupInfo.createOrReplaceTempView("nyctaxitrips")
    pickupInfo.show()

    spark.udf.register("CalculateX", (pickupPoint: String) => HotcellUtils.CalculateCoordinate(pickupPoint, 0))
    spark.udf.register("CalculateY", (pickupPoint: String) => HotcellUtils.CalculateCoordinate(pickupPoint, 1))
    spark.udf.register("CalculateZ", (pickupTime: String) => HotcellUtils.CalculateCoordinate(pickupTime, 2))

    pickupInfo = spark.sql("select CalculateX(nyctaxitrips._c5),CalculateY(nyctaxitrips._c5), CalculateZ(nyctaxitrips._c1) from nyctaxitrips")
    var newCoordinateName = Seq("x", "y", "z")
    pickupInfo = pickupInfo.toDF(newCoordinateName: _*)
    pickupInfo.show()

    val minX = -74.50 / HotcellUtils.coordinateStep
    val maxX = -73.70 / HotcellUtils.coordinateStep
    val minY = 40.50 / HotcellUtils.coordinateStep
    val maxY = 40.90 / HotcellUtils.coordinateStep
    val minZ = 1
    val maxZ = 31
    val numCells = (maxX - minX + 1) * (maxY - minY + 1) * (maxZ - minZ + 1)
    
    // YOU NEED TO CHANGE THIS PART, Below here!
    
    val filteredPickups = pickupInfo.filter(s"x >= $minX and x <= $maxX and y >= $minY and y <= $maxY and z >= $minZ and z <= $maxZ")
    val cubeCounts = filteredPickups.groupBy("x", "y", "z").count()
    cubeCounts.printSchema()  // printSchema() is used to print the schema of the DataFrame

    val sumCounts = cubeCounts.agg(
      sum("count").cast("long").alias("sumCount"),
      sum(pow(col("count"), 2)).cast("long").alias("sumCountSquares")
    ).collect() // collect() returns an array of Row objects

    val totalSum = sumCounts(0).get(0) match {
      case d: Double => d.toLong  // get() is used to retrieve the value of a given column for a given row
      case l: Long => l  // match() is used to match the value of a given column for a given row
      case _ => 0L  // _ is used to match any value
    }
    val totalSumSquares = sumCounts(0).get(1) match {
      case d: Double => d.toLong  // get() is used to retrieve the value of a given column for a given row
      case l: Long => l  // match() is used to match the value of a given column for a given row
      case _ => 0L  // _ is used to match any value
    }

    val mean = totalSum / numCells  // mean is the average pickup count per cell
    val standardDeviation = Math.sqrt((totalSumSquares / numCells) - (mean * mean))  
    // standardDeviation is the standard deviation of the counts of all cells

    val selfJoin = cubeCounts.as("a").join(cubeCounts.as("b"),  // as() is used to alias a DataFrame
    org.apache.spark.sql.functions.abs(col("a.x") - col("b.x")) <= 1 &&  // abs() is used to return the absolute value of a column
    org.apache.spark.sql.functions.abs(col("a.y") - col("b.y")) <= 1 &&  // col() is used to retrieve a column from a DataFrame
    org.apache.spark.sql.functions.abs(col("a.z") - col("b.z")) <= 1)  // join() is used to join two DataFrames
    val weightedCounts = selfJoin.groupBy("a.x", "a.y", "a.z").agg(  // groupBy() is used to group the DataFrame by a.x, a.y, and a.z
      sum("b.count").alias("weight_sum"),  // sum() is used to sum the values of a column
      count("*").alias("weight_count")  // count() is used to count the number of rows in a DataFrame
    )

    val calculateGScore = udf((xi: Long, wx: Long, wc: Long) => {  // udf() is used to define a user-defined function
      val numerator = xi - mean * wc  // mean is the mean of the counts of all cells
      val denominator = standardDeviation * Math.sqrt((numCells * wc - wc * wc) / (numCells - 1))
      numerator / denominator  // return the G-score of a cell given its x, y, and z coordinates
    })

    val gScoreDF = weightedCounts.withColumn("gscore", calculateGScore(col("weight_sum"), col("weight_count"), col("weight_count")))
 
    val top50 = gScoreDF.sort(desc("gscore")).select("x", "y", "z").limit(50) // sort() is used to sort the DataFrame by gscore in descending order
    top50.show(50, false)  // show() is used to display the DataFrame in the console
    top50
  }
}

