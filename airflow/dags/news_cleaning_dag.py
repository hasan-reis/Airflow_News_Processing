from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from processors.data_cleaner import DataCleaner #data_cleaner dosyasindan base_scraper sinifini import etmeye calisirem
from storage.file_saver import FileSaver
from storage.mongo_saver import MongoSaver

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
}

@dag(default_args=default_args, schedule_interval=None, catchup=False)
def news_cleaning_dag():
    @task
    def clean_news(raw_data):  
        cleaner = DataCleaner(raw_data)
        cleaned_data = cleaner.clean()
        return cleaned_data  

    @task
    def save_to_files(cleaned_data):  
        file_saver = FileSaver(cleaned_data)
        file_saver.save_to_csv()
        file_saver.save_to_excel()

    @task
    def save_to_mongo(cleaned_data): 
        mongo_saver = MongoSaver(cleaned_data)
        mongo_saver.save_to_mongo()

    raw_data = '{{ dag_run.conf["raw_data"] }}' 
    cleaned_data = clean_news(raw_data)
    save_to_files(cleaned_data) >> save_to_mongo(cleaned_data)

news_cleaning_dag = news_cleaning_dag()