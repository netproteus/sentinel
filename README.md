sentinel
========

Sentinel is a light weight monitoring alerts tool.  It does not directly store any monitoring data, but is designed to provide alerting on top of existing tools such as [graphite](http://graphiteapp.org/).

Installation
------------

The sentinel web UI is read-only, all configuration is done via a file.  Start by creating the config file e.g. `/etc/sentinel.conf`

```
{
  "alerts": {
    "team_one_api": {
      "plugin": "http",
      "config": {
        "friendly_name": "Team One API",
        "url": "http://httpstat.us/200"
      }
    }
  }
}
```

Run with docker, be sure to configure the correct path of the config file and also a suitable folder for storing working state

```
sudo docker run -t -i --rm -p 8000:80 -v /etc/sentinel.conf:/sentinel.conf -v /var/sentinel:/state kierenbeckett/sentinel
```

You should see your example HTTP alert being run in the logs.  To view the alerts HUD visit `http://localhost:8000/`.  Change the url to `http://httpstat.us/404`, after a few minutes when the alert is next run you should see it get marked as failing.

Alerts
------

Add alerts to your config as follows

```
{
  ...,
  "alerts": {
    "my_alert": {
      "plugin": "http",
      "config": {
        "friendly_name": "Team One API",
        "url": "http://httpstat.us/200"
      }
      "warn_delay": 60,
      "warn_contacts": [
        {"type": "email", "address": "team_one@example.com"},
        ...
      ],
      "fail_delay": 60,
      "fail_contacts": [
        {"type": "email", "address": "team_one@example.com"},
        ...
      ],
    },
    ...
  },
  ...
}
```

* plugin - This is the type of alert, see below for applicable values.
* config - Plugin specific config.
* warn_delay - Optional, rather than notifying contacts immediately after an alert moves to the warn state wait the given number of seconds.
* warn_contacts - Optional, contacts to notify when the alert moves into the warn state.
* fail_delay - Optional, rather than notifying contacts immediately after an alert moves to the fail state wait the given number of seconds.
* fail_contacts - Optional, contacts to notify when the alert moves into the fail state.

Note that for contacts the contact type must also be setup, see below.

### Plugins

#### http

Check a HTTP endpoint and fail if a 200 isn't returned.

```
  ...
  "my_http_alert": {
    "plugin": "http",
    "config": {
      "friendly_name": "My endpoint name",
      "url": "http://httpstat.us/200"
    },
    ...
  },
  ...
```

#### graphite_disk_space

Check for low disk space across servers using graphite data.

```
  ...
  "my_disk_space_alert": {
    "plugin": "graphite_disk_space",
    "config": {
      "used_space_key": "servers.*.diskspace.*.gigabyte_used",
      "avail_space_key": "servers.*.diskspace.*.gigabyte_avail",
    },
    ...
  },
  ...
```

This assumes disk usage stats are emitted to graphite using keys such as `servers.<hostname>.diskspace.<drivename>.gigabyte_{used,avail}.`

#### rabbit_queues

Check for large RabbitMQ queues.

```
  ...
  "my_rabbit_queues_alert": {
    "plugin": "rabbit_queues",
    "config": {
      "authentication": {
        "username": "rabbit_user",
        "password": "rabbit_pass"
      }
      "host": "http://rabbit.example.com",
      "queue_sizes": {
        "queue_name_prefix_": [50, 5000, 1]
      }
    },
    ...
  },
  ...
```

Contact Types
-------------

For alerts to send notifications one or more contact types must be setup

```
  ...
  "contact_types": {
    "my_contact_type": {
      "plugin": "smtp",
      "config": {
        "authentication": {
          "username": "xxx",
          "password": "yyy"
        },
        "host": "email-smtp.us-east-1.amazonaws.com",
        "from_address": "sentinel@example.com"
      }
    },
    ...
  },
  ...
```

* plugin - This is the type of contact type, see below for applicable values.
* config - Plugin specific config.

### Plugins

#### smtp

Send an alert via email using SMTP.

```
  ...
  "my_smtp_contact_type": {
    "plugin": "smtp",
    "config": {
      "authentication": {
        "username": "xxx",
        "password": "yyy"
      },
      "host": "email-smtp.us-east-1.amazonaws.com",
      "from_address": "sentinel@example.com"
    }
  },
  ...
```

Then to define a contact

```
  ...
  fail_contacts: [
    {"type": "my_smtp_contact_type", "address": "to_be_alerted@example.com"}
  ],
  ...
```

#### pagerduty

Send an alert via PagerDuty.

```
  ...
  "my_pagerduty_contact_type": {
    "plugin": "pagerduty",
    "config": {
      "service_key": "xxx",
    }
  },
  ...
```

Then to define a contact

```
  ...
  fail_contacts: [
    {"type": "my_pagerduty_contact_type"}
  ],
  ...
```

Persisting State
----------------

To keep track of alerts Sentinel requires a certain amount of internal state.  By default this is persisted to local disk, a better option for production is to persist to a remote data store.  For example to persist to DynamoDB add to your `sentinel.conf`

```
{
  ...
  "state": {
    plugin": "dynamodb",
    "config": {
      "table": "sentinel",
      "aws_access_key_id": "xxx",
      "aws_secret_access_key": "yyy",
      "aws_region": "eu-west-1"
    }
  },
  ...
}
```

You will need to create a DynamoDB table with a non-ranged primary key named `name`, a read/write thoughput of 5 will suffice.

Custom Plugins
--------------

You can write additional alert, contact type and state plugins.  Use the existing plugins as examples, the easiest way to then integrate them is to make your own extension of the Sentinel Docker image

```
FROM kierenbeckett/sentinel

ADD my_alert_plugin.py /app/sentinel/alert_plugins/
ADD my_contact_type_plugin.py /app/sentinel/contact_type_plugins/
ADD my_state_plugin.py /app/sentinel/state_plugins/
```

If you think your plugin might be useful to other people please consider opening a pull request.
