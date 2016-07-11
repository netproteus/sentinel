from sentinel.plugin_utils import get_datapoint


def get_disk_name(key):
    parts = key[14:-1].split('.')
    return '%s disk space on %s' % (parts[3].replace('_','/'), parts[1])


def get_data(config):
    used_key = config['used_space_key']
    avail_key = config['avail_space_key']

    hosts_used = {}
    for (host,used) in get_datapoint(config, used_key).items():
        hosts_used[get_disk_name(host)] = used

    hosts_prev_avail = {}
    for (host,avail) in get_datapoint(config, avail_key, 'from=-1425min&until=-1440min').items():
        hosts_prev_avail[get_disk_name(host)] = avail

    data = {}
    for (host,avail) in get_datapoint(config, avail_key).items():
        host = get_disk_name(host)
        rate_per_day = hosts_prev_avail.get(host, 0) - avail
        days_left = avail / rate_per_day if rate_per_day > 0 else None
        percent_free = (100 * avail / (avail + hosts_used[host]))
        change_desc = ('~%d days' % days_left) if days_left is not None else ('freed %dgb in the last 24 hours' % (rate_per_day * -1))
        data[host] = {
            'state': 'FAIL' if percent_free < 10 else 'WARN' if percent_free < 20 else 'OK',
            'message': '%d%% free space (%s)' % (percent_free, change_desc)
        }
    return data
