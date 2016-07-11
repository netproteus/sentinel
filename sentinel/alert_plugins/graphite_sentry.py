from sentinel.plugin_utils import get_datapoint


def get_data(config):
    errors = get_datapoint(config, config['errors_key'], time='from=-2hour').values()[0]
    return {
        'sentry errors': {
            'state': 'OK' if errors < 500 else 'FAIL',
            'message': '%d errors in the last hour' % errors
        }
    }
