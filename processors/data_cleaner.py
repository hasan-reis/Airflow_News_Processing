class DataCleaner:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def clean(self):
        cleaned_data = []
        for item in self.raw_data:
            cleaned_item = {
                "Main Title": item["Main Title"].strip(),
                "Link": item["Link"].strip(),
                "Summary": item["Summary"].strip() if "Summary" in item else "No summary available",
                "Sub Headings": item["Sub Headings"].strip() if "Sub Headings" in item else "",
                "Content": item["Content"].strip() if "Content" in item else "",
            }
            cleaned_data.append(cleaned_item)
        return cleaned_data
