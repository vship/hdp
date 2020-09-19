from pyspark.sql import SparkSession
spark = SparkSession.builder \
  .master("local") \
  .appName("parquet_example") \
  .getOrCreate()
df = spark.read.parquet('df2.parquet')
df.show()
