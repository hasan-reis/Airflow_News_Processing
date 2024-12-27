from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from scrapers.un_news_scraper import UNNewsScraper
from processors.data_cleaner import DataCleaner
from storage.file_saver import FileSaver
from storage.mongo_saver import MongoSaver

def scrape_news(**kwargs):
    scraper = UNNewsScraper(pages=2)
    raw_data = scraper.scrape()
    kwargs['ti'].xcom_push(key='raw_data', value=raw_data)

def clean_news(**kwargs):
    raw_data = kwargs['ti'].xcom_pull(key='raw_data', task_ids='scrape_news')
    cleaner = DataCleaner(raw_data)
    cleaned_data = cleaner.clean()
    kwargs['ti'].xcom_push(key='cleaned_data', value=cleaned_data)

def save_to_files(**kwargs):
    cleaned_data = kwargs['ti'].xcom_pull(key='cleaned_data', task_ids='clean_news')
    file_saver = FileSaver(cleaned_data)
    file_saver.save_to_csv()
    file_saver.save_to_excel()

def save_to_mongo(**kwargs):
    cleaned_data = kwargs['ti'].xcom_pull(key='cleaned_data', task_ids='clean_news')
    mongo_saver = MongoSaver(cleaned_data)
    mongo_saver.save_to_mongo()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'news_pipeline_dag',
    default_args=default_args,
    description='A pipeline to scrape, clean, and store news data',
    schedule_interval='@daily',
    catchup=False
)

scrape_task = PythonOperator(
    task_id='scrape_news',
    python_callable=scrape_news,
    provide_context=True,
    dag=dag
)

clean_task = PythonOperator(
    task_id='clean_news',
    python_callable=clean_news,
    provide_context=True,
    dag=dag
)

save_to_files_task = PythonOperator(
    task_id='save_to_files',
    python_callable=save_to_files,
    provide_context=True,
    dag=dag
)

save_to_mongo_task = PythonOperator(
    task_id='save_to_mongo',
    python_callable=save_to_mongo,
    provide_context=True,
    dag=dag
)

scrape_task >> clean_task >> save_to_files_task >> save_to_mongo_task
