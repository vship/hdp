from datetime import datetime
from airflow import DAG
from airflow_livy.session import LivySessionOperator
from airflow_livy.batch import LivyBatchOperator

dag = DAG(
    "02_session_lyvy",
    description="Run Spark job via Livy Sessions",
    schedule_interval=None,
    start_date=datetime(2020, 2, 3),
    catchup=False,
)

# See ready statements with parameter values substituted
# in the "Rendered template" tab of a running task.

pyspark_code = """
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
"""

# See the results of each statement's executions under "Logs" tab of the task.
df = LivySessionOperator(
    name="02_session_lyvy_{{ run_id }}",
    statements=[
        LivySessionOperator.Statement(code=pyspark_code, kind="pyspark"),
    ],
#    params={"your_number": 5, "your_string": "Hello world"},
    conf={"spark.jars.packages": "org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.1"},
    driver_memory='1g',
    task_id="02_lyvy_readkafka",
    dag=dag,
)

db = LivySessionOperator(
    name="02_session_lyvy_{{ run_id }}",
    statements=[
        LivySessionOperator.Statement(code=pyspark_code, kind="pyspark"),
    ],
#    params={"your_number": 5, "your_string": "Hello world"},
    conf={"spark.jars.packages": "org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.1"},
    driver_memory='1g',
    task_id="02_lyvy_writedb",
    dag=dag,
)

df >> db