package cse512

object HotzoneUtils {

  def ST_Contains(queryRectangle: String, pointString: String): Boolean = {
    // Check if queryRectangle or pointString is null or empty
    if(queryRectangle == null || queryRectangle.isEmpty || pointString == null || pointString.isEmpty) {
      return false
    }
    // YOU NEED TO CHANGE THIS PART
    // Split pointString to get X and Y coordinates
    val pointArray = pointString.split(",")
    val pointX = pointArray(0).toDouble
    val pointY = pointArray(1).toDouble

    // Split queryRectangle to get coordinates
    val rectangleArray = queryRectangle.split(",")
    val recX1 = rectangleArray(0).toDouble
    val recY1 = rectangleArray(1).toDouble
    val recX2 = rectangleArray(2).toDouble
    val recY2 = rectangleArray(3).toDouble

    // Find the lower and upper points of the rectangle
    val lowerX = Math.min(recX1, recX2)
    val lowerY = Math.min(recY1, recY2)
    val upperX = Math.max(recX1, recX2)
    val upperY = Math.max(recY1, recY2)

    // Check if the point is within the rectangle including the boundary
    if (pointX >= lowerX && pointX <= upperX && pointY >= lowerY && pointY <= upperY) {
      return true
    }
    // If the point is outside the rectangle
    return false
  }
}

