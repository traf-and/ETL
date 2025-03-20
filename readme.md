Примечание: инструкция readme.md подразумевает уже установленный инстанс postgresql. Файл migration.sql содержит код для создания структур в postgresql.

1. Первым шагом создаем виртуальное окружение и устанавливаем зависимости:  
```
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```  
  
2. Пока устанавливаются библиотеки можно установить и запустить mongodb в отдельном терминале
```
$ curl -fsSL https://pgp.mongodb.com/server-7.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
$ echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
$ cd /etc/apt/sources.list.d/
$ cat mongodb-org-7.0.list
$ sudo apt update
$ sudo apt install mongodb-org
$ sudo systemctl start mongod
```

3. Далее, после установки зависимотей 1го шага запускаем airflow 
```
airflow standalone
```
и после останавливаем сочетанием ```ctrl+c```

4. Теперь нужно скорректировать файл конфигурации "airflow.cfg" airflow по пути ```/home/USER_NAME/airflow```, где "USER_NAME" - имя пользователя.
5. Для переменной ```load_examples``` установить значение ```False```.  
Для переменной ```dags_folder``` указать абсолютный путь до директории с с дагами.
6. Повторно запускаем airflow в терминале
```
airflow standalone
```
И переходим по адресу ```http://localhost:8080/```
7. Вводим login/password указанный в терминале и переходим на вкладку Admin->Connections.  
Создаем подключение к postgre с именем "postgres_conn_id"
8. Теперь можно запускать даги:  
```dag_generate_mongo_data.py``` - для генерации случайных данных в mongodb по предложенной структуре  
```dag_load_data_to_postgre.py``` - для обработки НОВЫХ данных из mongodb и записи их в плоской структуре в postgresql