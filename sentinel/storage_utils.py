import json
import os


STATE_PATH = '/state/'
META_PATH = STATE_PATH + 'metadata.json'
ALERT_PATH = STATE_PATH + 'alert_%s.json'


def get_config():
    with open('/sentinel.conf') as f:
        return json.load(f)


def get_metadata():
    if os.path.exists(META_PATH):
        with open(META_PATH) as f:
            return json.load(f)

    return {}


def set_metadata(data):
    with open(META_PATH, 'wb') as f:
        json.dump(data, f)


def get_alert_data(name):
    plugin_path = ALERT_PATH % name
    if os.path.exists(plugin_path):
        with open(plugin_path) as f:
            return json.load(f)

    return {
        'keys': {}
    }


def set_alert_data(name, data):
    plugin_path = ALERT_PATH % name
    with open(plugin_path, 'wb') as f:
        json.dump(data, f)
