# Work with REST routes
import json
from src.console import Console


class Router:

    def __init__(self, db_file):
        try:
            with open(db_file) as f:
                self.data = json.load(f)
        except FileNotFoundError:
            Console.write(f'{db_file} not found !', 'red', bold=True)

    def get_data(self, url):
        print('Keys :', self.data.keys())
        print('URL :', url)



