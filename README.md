Role Name
=========

Role to send emails through sendgrid api or username / password.

Requirements
------------
Install sendgrid python library:


`pip install sendgrid`

Role Variables
--------------

```yaml
sendgrid_notifier_api_key         : "api key"
sendgrid_notifier_bcc             : ["bcc list"]
sendgrid_notifier_cc              : ["cc list"]
sendgrid_notifier_headers         : [{"key": "value"}]
sendgrid_notifier_from_address    : "from@example.com"
sendgrid_notifier_from_name       : "From sender"
sendgrid_notifier_reply_to        : "reply@example.com"
sendgrid_notifier_to_addresses    : ["user1@example.com"]
sendgrid_notifier_subject         : "Subject"
sendgrid_notifier_body            : "Hi there"
sendgrid_notifier_html_body       : "<b>Hi there</b>"
```

License
-------

BSD

Author Information
------------------

* [Ali Rizwan](github.com/aleerizw)