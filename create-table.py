import os
import urllib.request

from pyspark.sql.types import *
from pyspark.sql import SparkSession

urllib.request.urlretrieve("https://pasteur.epa.gov/uploads/10.23719/1531143/SupplyChainGHGEmissionFactors_v1.3.0_NAICS_CO2e_USD2022.csv", "USD2022.csv")

# Создание Spark-сессии
spark = SparkSession.builder \
    .appName("create-table") \
    .enableHiveSupport() \
    .getOrCreate()


# Создание датафрейма
df = spark.read.csv('USD2022.csv', header=True, inferSchema=True)

# Запись датафрейма в бакет в виде таблицы usd
df.write.mode("overwrite").option("path","s3a://psprk-data/usd").saveAsTable("USD2022")

os.remove("USD2022.csv")
