import requests


def send_message(config, key, message, contact):
    if message.startswith('[OK]'):
        type = 'resolve'
    else:
        type = 'trigger'

    data = {
        'service_key': config['service_key'],
        'event_type': type,
        'incident_key': key,
        'description': message,
    }

    resp = requests.post('https://events.pagerduty.com/generic/2010-04-15/create_event.json', json=data, timeout=10)
    resp.raise_for_status()
