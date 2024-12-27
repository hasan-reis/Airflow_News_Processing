from scrapers.un_news_scraper import UNNewsScraper
from processors.data_cleaner import DataCleaner
from storage.file_saver import FileSaver
from storage.mongo_saver import MongoSaver

def main():
    scraper = UNNewsScraper(pages=30)
    raw_data = scraper.scrape()

    cleaner = DataCleaner(raw_data)
    cleaned_data = cleaner.clean()

    file_saver = FileSaver(cleaned_data)
    file_saver.save_to_csv()
    file_saver.save_to_excel()

    mongo_saver = MongoSaver(cleaned_data)
    mongo_saver.save_to_mongo()

if __name__ == "__main__":
    main()
