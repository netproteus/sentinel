import requests
from requests.auth import HTTPBasicAuth


def get_data(config):
    auth = HTTPBasicAuth(config['authentication']['username'], config['authentication']['password'])
    resp = requests.get(config['host'] + '/api/queues', auth=auth)
    queues = resp.json()

    data = {}
    for queue in queues:
        name = queue['name']
        message_stats = queue.get('message_stats', {})
        queue_size = queue.get('messages')
        ack_rate = (message_stats.get('ack_details') or {}).get('rate')
        nack_rate = (message_stats.get('redeliver_details') or {}).get('rate')

        (inactive_threshold, active_threshold, nack_threshold) = (50, 5000, 1)
        for qs_name, qs_threshold in config['queue_sizes'].items():
            if name.startswith(qs_name):
                (inactive_threshold, active_threshold, nack_threshold) = qs_threshold

        data[name + ' queue'] = {
            'state': 'FAIL' if (queue_size > inactive_threshold and (ack_rate < 2 or ack_rate is None) or queue_size > active_threshold or nack_rate > nack_threshold) else 'OK',
            'message': 'size is %d, ack rate is %.2f, nack rate is %.2f' % (queue_size if queue_size else 0, ack_rate if ack_rate else 0, nack_rate if nack_rate else 0)
        }
    return data

