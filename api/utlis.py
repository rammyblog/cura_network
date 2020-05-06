import json


def load_and_dump_data(data):
    loaded_data = json.dumps(data)
    return json.loads(loaded_data)
