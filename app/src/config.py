import json

class Config:
    def __init__(self, json_file):
        self.json_file = json_file
        self.folder = None
        self.url = None
        self.country = None
        self.configuration = None
        self.load_data()

    def load_data(self):
        try:
            with open(self.json_file, 'r') as file:
                data = json.load(file)
                self.folder = data.get("folder")
                self.url = data.get("url")
                self.country = data.get("country")
                self.configuration = data.get("configuration")
        except FileNotFoundError:
            print(f"Error: The file {self.json_file} was not found.")
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON.")
