# 1. Работа с Yandex DataTransfer 

1. Скриншот созданной YDB в папке imgs '1_1.png'.
2. Использованы данные по транзакциям [ссылка](https://www.kaggle.com/datasets/skullagos5246/upi-transactions-2024-dataset). Bash команда для загрузки данных в таблицу (предварительно необходимо сформировать конфиг):
```
ydb -p quickstart import file csv -p upi_trans --header --null-value "" upi_transactions_2024.csv
```
3. Скриншот трансфера в папке imgs '1_3.png'
4. Скриншот результата загрузки в папке imgs '1_4.png'
      
        

# 2. Автоматизация работы с Yandex Data Processing при помощи Apache AirFlow

1. Инфраструктура развернута согласно документации по [ссылке](https://yandex.cloud/ru/docs/managed-airflow/tutorials/data-processing-automation)
2. PySpark-задание приведено в файле create-table.py
3. DAG-файл - 'Data-Processing-DAG.py'. Результаты выполнения DAG'а в скриншотах 'dag_run.png', 'DAG_res.png'.