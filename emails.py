from flask_mail import Mail, Message

mail = Mail()

def sendemail():
    msg = Message()
    msg.subject = "Email Subject"
    msg.recipients = ['bluefloyd12321@icloud.com']
    msg.sender = 'username@gmail.com'
    msg.body = 'Email body'
    mail.send(msg)

sendemail