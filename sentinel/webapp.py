import flask
from flask import Flask
from sentinel.storage_utils import get_alert_data, get_metadata, get_config


app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/alerts')
def alerts():
    alerts = []
    metadata = get_metadata()
    for alert in get_config()['alerts'] + [{'name': 'monitoring'}]:
        item = get_alert_data(alert['name'])
        for name, data in item['keys'].items():
            data['name'] = name
            data['plugin'] = alert['name']
            data['last_state_change'] = float(data['last_state_change'])
            data['contacted_warn'] = bool(data['contacted_warn'])
            data['contacted_fail'] = bool(data['contacted_fail'])
            alerts.append(data)

    return flask.jsonify(**{
        'alerts': alerts,
        'last_checked': metadata.get('last_check_finished')
    })


if __name__ == '__main__':
    app.run()
