sentinel
========

Sentinel is a light weight monitoring alerts tool.  It does not directly store any monitoring data, but is designed to provide alerting on top of existing tools such as [graphite](http://graphiteapp.org/).

Installation
------------

Create a config file e.g. `/etc/sentinel.conf`

```
{
  "contact_types": {
    "email": {
      "plugin": "smtp",
      "config": {
        "authentication": {
          "username": "xxx",
          "password": "yyy"
        },
        "host": "email-smtp.us-east-1.amazonaws.com",
        "from_address": "sentinel@example.com"
      }
    }
  },
  "monitoring_fail_contacts": [
    {"type": "email", "address": "ops@example.com"}
  ],
  "alerts": {
    "team_one_api": {
      "plugin": "http",
      "config": {
        "friendly_name": "Team One API",
        "url": "http://httpstat.us/200"
      },
      "fail_contacts": [
        {"type": "email", "address": "team_one@example.com"}
      ]
    }
  }
}
```

Run with docker, be sure to configure the correct path of the config file and also a suitable folder for storing working state

```
sudo docker run -t -i --rm -p 8000:80 -v /etc/sentinel.conf:/sentinel.conf -v /var/sentinel:/state kierenbeckett/sentinel
```

To view alerts HUD visit `http://localhost:8000/`.

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

Alert Plugins
-------------

### http

Check a HTTP endpoint and fail if a 200 isn't returned.

```
  ...
  "alerts": {
    "my_http_alert": {
      "plugin": "http",
      "config": {
        "friendly_name": "My endpoint name",
        "url": "http://httpstat.us/200"
      },
      ...
    },
    ...
  },
  ...
```

### graphite_disk_space

Check for low disk space across servers using graphite data.

```
  ...
  "alerts": {
    "my_disk_space_alert": {
      "plugin": "graphite_disk_space",
      "config": {
        "used_space_key": "servers.*.diskspace.*.gigabyte_used",
        "avail_space_key": "servers.*.diskspace.*.gigabyte_avail",
      },
      ...
    },
    ...
  },
  ...
```

This assumes disk usage stats are emitted to graphite using keys such as `servers.<hostname>.diskspace.<drivename>.gigabyte_{used,avail}.`

Contact Type Plugins
--------------------

### smtp

Send an alert via email using SMTP.

```
  ...
  "contact_types": {
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
  },
  ...
```
