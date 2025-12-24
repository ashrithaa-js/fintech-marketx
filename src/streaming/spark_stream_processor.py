from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("PriceStreamProcessor").getOrCreate()

def process_stream():
    df = spark.read.csv("data/raw/prices", header=True)
    df.show()

if __name__ == "__main__":
    process_stream()
