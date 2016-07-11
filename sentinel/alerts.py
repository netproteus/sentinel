import logging
import time
import sys
from sentinel.storage_utils import get_alert_data, set_alert_data, get_metadata, set_metadata, get_config


logging.basicConfig(stream=sys.stdout, format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


def send_alert(message, contacts):
    for contact in contacts:
        try:
            contact_type = get_config()['contact_types'][contact['type']]
            plugin_module = getattr(__import__('sentinel.contact_type_plugins.' + contact_type['plugin']), 'contact_type_plugins')
            plugin_module = getattr(plugin_module, contact_type['plugin'])
            message_def = getattr(plugin_module, 'send_message')
            message_def(contact_type['config'], message, contact)
        except Exception:
            log.exception('Could not send alert to %s', contact)


def check_alert(plugin_name, new_data, warn_contacts, fail_contacts, warn_delay, fail_delay):
    item = get_alert_data(plugin_name)

    for (key, state) in new_data.items():
        value = item['keys'].get(key, {})
        state['contacted_warn'] = value.get('contacted_warn', False)
        state['contacted_fail'] = value.get('contacted_fail', False)

        now = time.time()
        if value.get('state','OK') == state['state']:
            state['last_state_change'] = value.get('last_state_change',now)
        else:
            state['last_state_change'] = now
        state_age = now - float(state['last_state_change'])

        if state['state'] == 'FAIL' and not state['contacted_fail'] and state_age >= fail_delay:
            send_alert('[FAIL] %s, %s' % (key, state['message']), fail_contacts)
            state['contacted_fail'] = True

        if state['state'] == 'FAIL' and not state['contacted_warn'] and state_age >= fail_delay:
            send_alert('[FAIL] %s, %s' % (key, state['message']), warn_contacts)
            state['contacted_warn'] = True

        if state['state'] == 'WARN' and not state['contacted_warn'] and state_age >= warn_delay:
            send_alert('[WARN] %s, %s' % (key, state['message']), warn_contacts)
            state['contacted_warn'] = True

        if state['state'] == 'OK' and state['contacted_fail']:
            send_alert('[OK] %s, %s' % (key, state['message']), fail_contacts)
            state['contacted_fail'] = False

        if state['state'] == 'OK' and state['contacted_warn']:
            send_alert('[OK] %s, %s' % (key, state['message']), warn_contacts)
            state['contacted_warn'] = False

    item['keys'] = new_data
    item['last_checked'] = time.time()
    set_alert_data(plugin_name, item)


def check_alerts():
    metadata = get_metadata()

    if metadata.get('last_check_started', 0) > time.time() - 240:
        log.info('Alerts checked recently, skipping')
        return

    metadata['last_check_started'] = time.time()
    set_metadata(metadata)

    log.info('Checking alerts')
    config = get_config()
    overall_data = {}
    for alert_name, alert in config['alerts'].items():
        plugin_module = getattr(__import__('sentinel.alert_plugins.' + alert['plugin']), 'alert_plugins')
        plugin_module = getattr(plugin_module, alert['plugin'])
        data_def = getattr(plugin_module, 'get_data')

        log.info('Checking %s', alert_name)
        try:
            new_data = data_def(alert['config'])
            check_alert(alert_name, new_data, alert.get('warn_contacts', []), alert.get('fail_contacts', []), alert.get('warn_delay', 0), alert.get('fail_delay', 0))
            state = {'state': 'OK', 'message': 'ran successfully'}
            log.info('Checked %s', alert_name)
        except Exception:
            state = {'state': 'FAIL', 'message': 'an exception was thrown, check sentinel logs for details'}
            log.exception('Check of %s failed', alert_name)
        overall_data['%s monitoring plugin' % alert_name] = state
    check_alert('monitoring', overall_data, [], config['monitoring_fail_contacts'], 0, 14*60)

    metadata['last_check_finished'] = time.time()
    set_metadata(metadata)

    log.info('Checked alerts')


if __name__ == '__main__':
    while True:
        check_alerts()
        time.sleep(5*60)
