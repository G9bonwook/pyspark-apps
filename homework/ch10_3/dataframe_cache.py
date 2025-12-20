from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import time

spark = SparkSession.builder.appName("dataframe_cache").getOrCreate()

# 회사별 산업도메인 CSV READ
com_ind_path = 'hdfs://home/spark/sample/linkedin_jobs/company_industries.csv'
com_ind_schema= 'company_id STRING, industry STRING'
ind_df = spark.read.option("header", "true").option("multiline", "true").schema(com_ind_schema).csv(com_ind_path)

# 회사별 종업원 수 CSV READ
com_count_path = 'hdfs://home/spark/sample/linkedin_jobs/employee_counts.csv'
com_count_schema = 'company_id STRING, employee_count INT, follower_count INT, time_recorded INT'
count_df = spark.read.option("header", "true").option("multiline", "true").schema(com_count_schema).csv(com_count_path)

# company_id 컬럼으로 중복 제거 후 진행
# drop_duplicate : transform 함수
company_count_df = count_df.dropDuplicates(['company_id'])

# 캐시 저장
ind_df.persist()
company_count_df.persist()

# count : action 함수
print(ind_df.count())
print(company_count_df.count())

# filter : transform 함수
# it_df : 산업도메인이 IT Service and IT Consulting인 회사
# big_df : 직원 수가 1000명 이상인 회사
it_df = ind_df.filter(col('industry') == 'IT Services and IT Consulting')
big_df = company_count_df.filter(col('employee_count') >= 1000)

# join : transform 함수
it_big_df = it_df.join(big_df,'company_id','inner')

# 결과 출력
it_big_df.select(['company_id','employee_count']).sort('employee_count',ascending=False).show()

# 5분 대기
time.sleep(300)