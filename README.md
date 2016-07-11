sentinel
========

Sentinel is a light weight monitoring alerts tool.

Installation
------------

Create a config file e.g. `/etc/sentinel`

```
{
  "monitoring_fail_contacts": [
    {"type": "email", "address": "ops@example.com"}
  ],
  "contacts": [
    {
      "name": "email",
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
  ],
  "alerts": [
    {
      "name": "my_http_alert",
      "plugin": "http",
      "config": {
        "endpoints": {
          "example.com": "http://httpstat.us/200"
        }
      },
      "fail_contacts": [
        {"type": "email", "address": "team_one@example.com"}
      ]
    },
    {
      "name": "my_disk_space_alert",
      "plugin": "graphite_disk_space",
      "config": {
        "graphite": {
          "host": "http://graphite.example.com"
        },
        "graphite_used_space_key": "servers.*.diskspace.*.gigabyte_used",
        "graphite_avail_space_key": "servers.*.diskspace.*.gigabyte_avail"
      },
      "fail_contacts": [
        {"type": "email", "address": "team_two@example.com"}
      ]
    },
    {
      "name": "my_sentry_alert",
      "plugin": "graphite_sentry",
      "config": {
        "graphite": {
          "host": "http://graphite.example.com"
        },
        "graphite_errors_key": "stats.sentry.errors"
      },
      "fail_contacts": [
        {"type": "email", "address": "team_three@example.com"}
      ]
    }
  ]
}
```

Run with docker, be sure to configure the correct path of the config file and also a suitable folder for storing working state

```
sudo docker run -t -i --rm -p 8000:80 -v /etc/sentinel.conf:/sentinel.conf -v /var/sentinel:/state kierenbeckett/sentinel
```

To view alerts HUD visit `http://localhost:8000/`.
