#!/usr/bin/python

import urllib

try:
    import sendgrid
    from sendgrid.helpers.mail import *
except ImportError:
    module_fail.json(msg='Sendgrid python not found, install by: pip install sendgrid')


def post_sendgrid_api(from_address, reply_to, to_addresses,
                      subject, body, api_key=None, cc=None, bcc=None,
                      html_body=False, from_name=None, headers=None):
    # Create the api client
    sg = sendgrid.SendGridAPIClient(apikey=api_key)

    mail = Mail()

    if from_name:
        mail.from_email = Email(from_address, from_name)
    else:
        mail.from_email = Email(from_address)

    mail.subject = subject

    if reply_to:
        mail.reply_to = Email(reply_to)

    if html_body:
        content_type = 'text/html'
    else:
        content_type = 'text/plain'

    mail.add_content(Content(content_type, body))

    personalization = Personalization()

    for address in to_addresses:
        personalization.add_to(Email(address))

    if cc:
        for address in cc:
            personalization.add_cc(Email(address))
    if bcc:
        for address in bcc:
            personalization.add_bcc(Email(address))
    if headers:
        for header in headers:
            personalization.add_header(Header(header))

    mail.add_personalization(personalization)

    data = mail.get()
    return sg.client.mail.send.post(request_body=data)

# Main


def main():
    module = AnsibleModule(
        argument_spec=dict(
            api_key=dict(required=True, no_log=True),
            bcc=dict(required=False, type='list'),
            cc=dict(required=False, type='list'),
            headers=dict(required=False, type='list'),
            from_address=dict(required=True),
            from_name=dict(required=False),
            reply_to=dict(required=False),
            to_addresses=dict(required=True, type='list'),
            subject=dict(required=True),
            body=dict(required=True, type='str'),
            html_body=dict(required=False, default=False, type='bool')
        )
    )

    api_key = module.params['api_key']
    bcc = module.params['bcc']
    cc = module.params['cc']
    headers = module.params['headers']
    from_name = module.params['from_name']
    from_address = module.params['from_address']
    reply_to = module.params['reply_to']
    to_addresses = module.params['to_addresses']
    subject = module.params['subject']
    body = module.params['body']
    html_body = module.params['html_body']

    try:
        response = post_sendgrid_api(from_address, reply_to, to_addresses,
                                     subject, body, api_key, cc, bcc,
                                     html_body, from_name, headers)
    except Exception as e:
        module.fail_json(msg=str(e), changed=False)

    if response.status_code != 202:
        module.fail_json(msg="Unable to send email through SendGrid API: %s" %
                         response.body, changed=False)

    module.exit_json(msg=subject, changed=True)

# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
if __name__ == '__main__':
    main()