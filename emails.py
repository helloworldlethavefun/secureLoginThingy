from flask_mail import Mail, Message
from flask import render_template

mail = Mail()

# Sends the user password reset
def sendemail(user):
    token = user.get_user_reset_token()
    msg = Message()
    msg.subject = "Email Subject"
    msg.recipients = [user.email]
    msg.sender = 'username@gmail.com'
    msg.html = render_template('email.html', token=token)
    mail.send(msg)
