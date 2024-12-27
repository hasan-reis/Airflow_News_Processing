import requests
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36"
    }

    def fetch_content(self, url):
        response = requests.get(url, headers=self.HEADERS)
        if response.status_code == 200:
            return response.content
        print(f"Failed to fetch {url}. HTTP Status: {response.status_code}")
        return None

    @abstractmethod
    def scrape(self):
        pass

    @abstractmethod
    def _process_main_page(self, content):
        pass

    @abstractmethod
    def _process_title(self, title):
        pass

    @abstractmethod
    def _process_sub_page(self, url, title):
        pass
