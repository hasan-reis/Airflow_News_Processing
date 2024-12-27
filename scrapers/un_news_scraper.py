from scrapers.base_scraper import BaseScraper
from utils.content_parser import ContentParser
from bs4 import BeautifulSoup

class UNNewsScraper(BaseScraper):
    BASE_URL = "https://news.un.org/en/news?page="

    def __init__(self, pages=1):
        self.pages = pages
        self.data = []
        self.classes = {
            "main_title_class": "node__title",
            "content_div_class": "clearfix text-formatted field field--name-field-text-column field--type-text-long field--label-hidden field__item",
            "summary_div_class": "field-content",
        }

    def scrape(self):
        for page in range(self.pages):
            url = f"{self.BASE_URL}{page}"
            print(f"Processing page: {page}")
            content = self.fetch_content(url)
            if content:
                self._process_main_page(content)
        return self.data

    def _process_main_page(self, content):
        soup = BeautifulSoup(content, "html.parser")
        titles = soup.find_all("h2", class_=self.classes["main_title_class"])
        for title in titles:
            self._process_title(title)

    def _process_title(self, title):
        link_tag = title.find("a")
        if link_tag and "href" in link_tag.attrs:
            full_url = f"https://news.un.org{link_tag['href']}"
            title_text = title.text.strip()
            self._process_sub_page(full_url, title_text)

    def _process_sub_page(self, url, title):
        content = self.fetch_content(url)
        if content:
            parser = ContentParser(content, self.classes)
            summary = parser.get_summary()
            sub_headings, paragraphs = parser.get_content()
            self.data.append({
                "Main Title": title,
                "Link": url,
                "Summary": summary,
                "Sub Headings": "; ".join(sub_headings),
                "Content": paragraphs,
            })
