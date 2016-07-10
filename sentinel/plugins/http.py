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
    data = {}
    for name, url in config['endpoints'].items():
        data[name] = get_url(url)
    return data
