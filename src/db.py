import json
import os
from src.settings import CRLF


class DatabaseRecord:

    def __init__(self, record):
        if isinstance(record, dict):
            self.items = record.items()

    def __repr__(self):
        result = []
        for k, v in self.items:
            if isinstance(v, int) or isinstance(v, bool):
                result.append(f'"{k}": {str(v).lower()}')
            else:
                result.append(f'"{k}": "{v}"')
        output = '{\r\n  ' + ',\r\n  '.join(result) + '\r\n}'
        return output

    def filter(self, search):
        r = [field for field, value in self.items if field in search and str(value) == str(search.get(field))]
        return r


class Database:

    def __init__(self, db_path):
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                self._file = db_path
                self._db = json.load(f)
        except FileNotFoundError as err:
            print(err)
            return

    # Generate name for debug
    def _get_name(self):
        i = 0
        while True:
            i += 1
            new_file = self._file.replace('.json', f'_{str(i).zfill(2)}.json')
            if not os.path.exists(new_file):
                break
        return new_file

    # Search in database
    def select(self, route, pk=None):
        result = self._db.get(route)
        convert = str
        default = False
        search = ['slug', 'alias']

        if result and pk:
            if isinstance(pk, str) and pk.isnumeric():
                pk = int(pk)
                search = ['id', 'pk']
                convert = int
                default = 0

            for item in result:
                for field_name in search:
                    if convert(item.get(field_name, default)) == pk:
                        result = item
                        break

        return result

    # Save data to JSON File
    def save(self):
        # self._get_name()
        file_name = self._file
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(self._db, f, sort_keys=False, indent=2)

    #
    # todo: Database methods
    #
    def insert(self, route, data):
        pass

    def update(self, route, data, pk=None):
        pass

    def delete(self, route, pk=None):
        pass

