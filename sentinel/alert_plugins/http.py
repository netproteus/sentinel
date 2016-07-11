import requests


def get_url(url):
    try:
        resp = requests.get(url, timeout=10)
        state = 'OK' if resp.status_code == 200 else 'FAIL'
        message = 'response code is %s' % resp.status_code
    except Exception as e:
        state = 'FAIL'
        message = 'unexpected error: %s' % e
    return {
        'state': state,
        'message': message
    }


def get_data(config):
    return {
        config['friendly_name']: get_url(config['url'])
    }
