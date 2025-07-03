from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType

# 1. Create Spark session
# spark = SparkSession.builder \
#     .appName("KafkaSparkStreaming") \
#     .getOrCreate()
spark = SparkSession.builder \
        .appName("KafkaToParquet") \
        .getOrCreate()

# 2. Read from Kafka
# df_raw = spark.readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "kafka:9092") \
#     .option("subscribe", "test-topic") \
#     .option("startingOffsets", "latest") \
#     .load()
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "test-topic") \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .load()

# 3. Define schema and parse json messages
schema = StructType() \
    .add("name", StringType()) \
    .add("email", StringType()) \
    .add("phone", StringType()) \
    .add("address", StringType())

parsed_df = kafka_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# 4. Write to MinIO as Parquet
query = parsed_df.writeStream \
    .format("parquet") \
    .option("path", "/mnt/minio/kafka_data") \
    .option("checkpointLocation", "/mnt/minio/checkpoints") \
    .outputMode("append") \
    .start()

# # Convert binary value to string
# df_parsed = df_raw.selectExpr("CAST(value AS STRING)")

# # Parse JSON into columns
# df_json = df_parsed.select(from_json(col("value"), schema).alias("data")).select("data.*")

# # Output to console
# query = df_json.writeStream \
#     .format("console") \
#     .outputMode("append") \
#     .start()

query.awaitTermination()
