from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp
import uuid

def ingest_csv_to_delta(spark, csv_files, has_header, delta_table):

    df = spark.read.option("header", has_header).csv(csv_files)


    df_with_extra_columns = df.withColumn("ingestion_tms", current_timestamp()) \
                              .withColumn("batch_id", uuid.uuid4().cast("string"))


    df_with_extra_columns.write.format("delta").mode("append").save(delta_table)

if __name__ == "__main__":

    spark = SparkSession.builder.appName("CSV to Delta Job").getOrCreate()

    spark.sql("SET spark.databricks.delta.formatCheck.enabled=false")

    csv_files = "/path/to/csv/files"
    has_header = True
    delta_table = "/path/to/delta/table"

    ingest_csv_to_delta(spark, csv_files, has_header, delta_table)

    spark.stop()
