from flask import Flask, request
from resources import EntryManager


FOLDER = 'C:\Misha'

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/entries/")
def get_entries():
    value = EntryManager(FOLDER)
    value.load()
    entries = []
    for item in value.entries:
        entries.append(item.json())
    return entries


@app.route("/api/save_entries/", methods=['POST'])
def save_entries():
    entry_manager = EntryManager(FOLDER)
    value = request.get_json(entry_manager.load())
    print(value)
    return {'status': 'success'}

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)