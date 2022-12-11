from flask_mail import Mail, Message
from flask import render_template

mail = Mail()

def sendemail(otc):
    with open('message-body-format.txt', 'r') as file:
        email_body = file.read()
        file.close()
    msg = Message()
    msg.subject = "Email Subject"
    msg.recipients = ['bluefloyd12321@icloud.com']
    msg.sender = 'username@gmail.com'
    print(type(otc))
    msg.html = render_template('email.html', otc=otc)
    mail.send(msg)
