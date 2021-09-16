from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body, attachments=None, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:  # allows adding attachments for example json file
        for attachment in attachments:
            msg.attach(*attachment)  # without * there would be single argument-list
    if sync:  # send email in the foreground
        mail.send(msg)
    else:
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
        # _get_current_object() extracts the actual application instacje from isinde the proxy object
