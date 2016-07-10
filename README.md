sentinel
========

Sentinel is a light weight monitoring alerts tool.

Installation
------------

Create a folder to store state and config e.g. `/etc/sentinel` and a `config.json` inside it e.g.

```
{
  "smtp": {
    "authentication": {
      "username": "xxx",
      "password": "yyy"
    },
    "host": "email-smtp.us-east-1.amazonaws.com",
    "from_address": "sentinel@example.com"
  },
  "monitoring_fail_contacts": [
    {"type": "email", "address": "ops@example.com"}
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
      "plugin": "disk_space",
      "config": {
        "graphite_used_space_key": "servers.*.diskspace.*.gigabyte_used",
        "graphite_avail_space_key": "servers.*.diskspace.*.gigabyte_avail"
      },
      "fail_contacts": [
        {"type": "email", "address": "team_two@example.com"}
      ]
    },
    {
      "name": "my_sentry_alert",
      "plugin": "sentry",
      "config": {
        "graphite_errors_key": "stats.sentry.errors"
      },
      "fail_contacts": [
        {"type": "email", "address": "team_three@example.com"}
      ]
    }
  ]
}
```

Run with docker

```
sudo docker run -t -i --rm -p 8000:8000 -v /etc/sentinel:/app/state kierenbeckett/sentinel
```

To view alerts HUD visit `http://localhost:8000/`.
