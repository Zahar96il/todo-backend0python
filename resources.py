import json
import os
def print_with_indent(value, indent=0):
    indentation = '\t' * indent
    print(f'{indentation}{value}')


class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    def add_entry(self,entry):
        self.entries.append(entry)
        entry.parent = self

    @classmethod
    def from_json(cls, value: dict):
        new_entry = cls(value['title'])
        for item in value.get('entries', []):
            new_entry.add_entry(cls.from_json(item))
        return new_entry

    @classmethod
    def load(cls, filename):
        with open(filename, 'r',  encoding='utf-8') as file:
            content = json.load(file)
        return cls.from_json(content)


    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def json(self):
        res = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }
        return res

    def save(self, path):
        file_path = os.path.join(path, f'{self.title}.json')
        value = self.json()
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(value, file, indent=4, ensure_ascii=False)


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)


    def load(self):
        for item in os.listdir(self.data_path):
            if item.endswith('.json'):
                file_path = os.path.join(self.data_path, item)
                load_entry = Entry.load(file_path)
                self.entries.append(load_entry)

    def add_entry(self, title: str):
        entry = Entry(title)
        self.entries.append(entry)

