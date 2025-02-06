from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from scrapers.un_news_scraper import UNNewsScraper
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
}

@dag(default_args=default_args, schedule_interval='@daily', catchup=False)
def news_scraping_dag():
    @task
    def scrape_news():
        scraper = UNNewsScraper(pages=2)
        raw_data = scraper.scrape()
        return raw_data  

    trigger_cleaning_dag = TriggerDagRunOperator(
        task_id='trigger_cleaning_dag',
        trigger_dag_id='news_cleaning_dag',
        conf={'raw_data': '{{ ti.xcom_pull(task_ids="scrape_news") }}'}  
    )

    scrape_news() >> trigger_cleaning_dag

news_scraping_dag = news_scraping_dag()