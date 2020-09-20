from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local") \
    .appName("parquet_example") \
    .getOrCreate()
df = spark.read.parquet('df2.parquet')
df.show(10)
filterdf = df.filter(df.food == "Pizza").sort(df.currency)
filterdf.show(10)
filterdf.write \
    .format("jdbc") \
    .mode("append") \
    .option("driver", 'org.postgresql.Driver') \
    .option("url", "jdbc:postgresql://172.18.0.9:5432/spark") \
    .option("dbtable", "pizza") \
    .option("user", "spark") \
    .option("password", "spark") \
    .save()
