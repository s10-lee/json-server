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

    def parse(self, data):
        pass

    def get_response(self, url):
        url = url.split('/')
        id = None
        alias = url[0]
        if len(url) == 2:
            id = url[1]

        response_data = []

        # print('Alias: ', alias)
        # print('ID: ', id)

        for a in self.data:
            if a == alias:
                response_data = self.data[a]

        if id:
            return list(filter(lambda x: str(x['id']) == id,  response_data))
        return response_data



