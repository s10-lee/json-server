import json
import os
from collections import OrderedDict
from src.settings import PK_FIELDS



class DatabaseRecord:
    pass


class Database:

    def __init__(self, db_path):
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                self._file = db_path
                self._db = json.load(f)
                # self._db = json.loads(''.join(f.readlines()))
        except FileNotFoundError as err:
            print(err)
            return

    @property
    def db(self):
        return self._db

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
        default = ''
        search = ['slug', 'alias']

        if result and pk:
            if isinstance(pk, str) and pk.isnumeric():
                pk = int(pk)
                search = ['id', 'pk']
                convert = int
                default = 0

            print('Search is')
            print(search)
            print('PK:', type(pk), pk)

            for item in result:
                for field_name in search:
                    if convert(item.get(field_name, default)) == pk:
                        result = item
                        break

        return result

    def save(self):
        # self._get_name()
        file_name = self._file
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(self._db, f, sort_keys=False, indent=2, ensure_ascii=False)

    def create_entity(self, route, data):
        pass

