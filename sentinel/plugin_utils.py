import requests


def get_datapoint(config, target, time='from=-15min'):
    resp = requests.get('%s/render/?target=keepLastValue(%s)&format=json&%s' % (config['graphite']['host'], target, time), timeout=60)
    data = {}
    for target in resp.json():
        value = target['datapoints'][-1][0]
        if value is not None:
            data[target['target']] = value
    return data
