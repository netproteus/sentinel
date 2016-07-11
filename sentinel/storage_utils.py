import json
import os


STATE_PATH = '/state/'
META_PATH = STATE_PATH + 'metadata.json'
ALERT_PATH = STATE_PATH + 'alert_%s.json'


def get_config():
    with open('/sentinel.conf') as f:
        return json.load(f)


def get_metadata():
    state_config = get_config().get('state', {'plugin': 'file', 'config': {}})
    plugin_module = getattr(__import__('sentinel.state_plugins.' + state_config['plugin']), 'state_plugins')
    plugin_module = getattr(plugin_module, state_config['plugin'])
    state_def = getattr(plugin_module, 'get_metadata')
    return state_def(state_config['config'])


def set_metadata(data):
    state_config = get_config().get('state', {'plugin': 'file', 'config': {}})
    plugin_module = getattr(__import__('sentinel.state_plugins.' + state_config['plugin']), 'state_plugins')
    plugin_module = getattr(plugin_module, state_config['plugin'])
    state_def = getattr(plugin_module, 'set_metadata')
    state_def(state_config['config'], data)


def get_alert_data(name):
    state_config = get_config().get('state', {'plugin': 'file', 'config': {}})
    plugin_module = getattr(__import__('sentinel.state_plugins.' + state_config['plugin']), 'state_plugins')
    plugin_module = getattr(plugin_module, state_config['plugin'])
    state_def = getattr(plugin_module, 'get_alert_data')
    return state_def(state_config['config'], name)


def set_alert_data(name, data):
    state_config = get_config().get('state', {'plugin': 'file', 'config': {}})
    plugin_module = getattr(__import__('sentinel.state_plugins.' + state_config['plugin']), 'state_plugins')
    plugin_module = getattr(plugin_module, state_config['plugin'])
    state_def = getattr(plugin_module, 'set_alert_data')
    state_def(state_config['config'], name, data)
