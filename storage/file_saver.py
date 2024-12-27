import os
import pandas as pd

class FileSaver:
    def __init__(self, data):
        self.data = data
        self.output_dir = "data_outputs"
        os.makedirs(self.output_dir, exist_ok=True)

    def save_to_csv(self, file_name="news_data.csv"):
        file_path = os.path.join(self.output_dir, file_name)
        df = pd.DataFrame(self.data)
        df.to_csv(file_path, index=False, encoding="utf-8-sig")
        print(f"Data saved to {file_path}")

    def save_to_excel(self, file_name="news_data.xlsx"):
        file_path = os.path.join(self.output_dir, file_name)
        df = pd.DataFrame(self.data)
        df.to_excel(file_path, index=False, engine="openpyxl")
        print(f"Data saved to {file_path}")
