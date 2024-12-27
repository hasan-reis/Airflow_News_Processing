from bs4 import BeautifulSoup

class ContentParser:
    def __init__(self, content, classes):
        self.soup = BeautifulSoup(content, "html.parser")
        self.classes = classes

    def get_summary(self):
        summary_div = self.soup.find("div", class_=self.classes["summary_div_class"])
        return summary_div.find("p").text.strip() if summary_div else "No summary available"

    def get_content(self):
        content_div = self.soup.find("div", class_=self.classes["content_div_class"])
        sub_headings = []
        paragraphs = []
        if content_div:
            sub_headings = [h2.text.strip() for h2 in content_div.find_all("h2")]
            paragraphs = [p.text.strip() for p in content_div.find_all("p")]
        return sub_headings, " ".join(paragraphs)
