import json

def load_config():
    with open('lib_config/config.json', 'r') as config_file:
        return json.load(config_file)