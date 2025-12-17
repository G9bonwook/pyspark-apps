import time
from pyspark.sql.connect.session import SparkSession

spark = SparkSession \
    .builder \
    .appName('standalone_pyspark')  \
    .getOrCreate()

schema = 'id INT, country STRING, hit LONG'
df = spark.createDataFrame(data=[(1,'Korea',120),(2,'USA',80),(3,'Japan',40)], schema=schema)
df.count()

time.sleep(600)