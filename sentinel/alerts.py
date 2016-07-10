import logging
import smtplib
import time
from email.mime.text import MIMEText
import sys
from sentinel.storage_utils import get_alert_data, set_alert_data, get_metadata, set_metadata, get_config


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)


def send_email(message, address):
    smtp_config = get_config()['smtp']
    msg = MIMEText(message)
    msg['Subject'] = message
    msg['From'] = smtp_config['from_address']
    msg['To'] = address
    s = smtplib.SMTP(smtp_config['host'])
    s.starttls()
    if 'authentication' in smtp_config:
        s.login(smtp_config['authentication']['username'], smtp_config['authentication']['password'])
    s.sendmail(smtp_config['from_address'], [address], msg.as_string())
    s.quit()


def send_alert(message, contacts):
    for contact in contacts:
        try:
            if contact['type'] == 'email':
                send_email(message, contact['address'])
            else:
                raise Exception('Unknown contact type')
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
    for alert in config['alerts']:
        plugin_module = getattr(__import__('sentinel.plugins.' + alert['plugin']), 'plugins')
        plugin_module = getattr(plugin_module, alert['plugin'])
        data_def = getattr(plugin_module, 'get_data')

        log.info('Checking %s', alert['name'])
        try:
            new_data = data_def(alert['config'])
            check_alert(alert['name'], new_data, alert.get('warn_contacts', []), alert.get('fail_contacts', []), alert.get('warn_delay', 0), alert.get('fail_delay', 0))
            state = {'state': 'OK', 'message': 'ran successfully'}
            log.info('Checked %s', alert['name'])
        except Exception:
            state = {'state': 'FAIL', 'message': 'an exception was thrown, check sentinel logs for details'}
            log.exception('Check of %s failed', alert['name'])
        overall_data['%s monitoring plugin' % alert['name']] = state
    check_alert('monitoring', overall_data, [], config['monitoring_fail_contacts'], 0, 14*60)

    metadata['last_check_finished'] = time.time()
    set_metadata(metadata)

    log.info('Checked alerts')


if __name__ == '__main__':
    while True:
        check_alerts()
        time.sleep(5*60)
