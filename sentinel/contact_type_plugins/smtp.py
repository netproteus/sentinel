from email.mime.text import MIMEText
import smtplib


def send_message(config, key, message, contact):
    msg = MIMEText(message)
    msg['Subject'] = message
    msg['From'] = config['from_address']
    msg['To'] = contact['address']
    s = smtplib.SMTP(config['host'])
    s.starttls()
    if 'authentication' in config:
        s.login(config['authentication']['username'], config['authentication']['password'])
    s.sendmail(config['from_address'], [contact['address']], msg.as_string())
    s.quit()
