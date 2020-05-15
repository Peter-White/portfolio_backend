from flask_mail import Message
from app import app, mail
from flask import render_template

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_confirm_email(user, code):

    send_email(
        'Confirm Account',
        sender = app.config['ADMINS'][0],
        recipients = [user.email],
        text_body = render_template('email/confirm_account.txt', user=user, code=code),
        html_body = render_template('email/confirm_account.html', user=user, code=code)
    )

def send_test(email):

    send_email(
        'Test',
        sender = app.config["ADMINS"][0],
        recipients = [email],
        text_body = render_template('email/test.txt'),
        html_body = render_template('email/test.html')
    )
