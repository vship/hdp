from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import *

addressSchema = [StructField("food", StringType(), True),
                 StructField("amount", FloatType(), True),
                 StructField("currency", StringType(), True)]

foodSchema = StructType(addressSchema)

spark = SparkSession.builder \
    .master("cluster") \
    .appName("food") \
    .getOrCreate()

df = spark \
    .read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "sandbox-hdp.hortonworks.com:6667") \
    .option("subscribe", "food") \
    .load() \
    .selectExpr("CAST(value AS STRING)")
#    .select(from_json(col("value").cast("string"), foodSchema))
#df.show(5)
#df.printSchema()
df2 = df.select(from_json("value", foodSchema).alias("Foods")).select("Foods.*")
df2.show(5)
df2.printSchema()
df2.write.parquet("/spark_files/df.parquet")