from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import requests
import random

def print_hello():
    print('Hello Airflow')

def print_date():
    print('Today is {}'.format(datetime.today().date()))

def print_random_number():
    random_number = random.randint(1, 100)
    print('Random number of the day: "{}"'.format(random_number))

dag = DAG(
    'hello_dag',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 23 * * *',
    catchup=False
)

print_hello_task = PythonOperator(
    task_id='print_hello',
    python_callable=print_hello,
    dag=dag
)

print_date_task = PythonOperator(
    task_id='print_date',
    python_callable=print_date,
    dag=dag
)

print_random_number_task = PythonOperator(
    task_id='print_random_number',
    python_callable=print_random_number,
    dag=dag
)

print_hello_task >> print_date_task >> print_random_number_task