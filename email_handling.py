import smtplib
import imaplib
import email
import ssl
import re
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

dic = {"HSHLOIMIE@vtext.com":"3472150400@vzwpix.com","@vtext.com": "@vzwpix.com ",}
username = "autointernet910@gmail.com"
password = "12345qwertY"

connection = ""


def start_send():
    global connection
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=username, password=password)


def send_main(send_to, message, subject="", ):
    global connection
    connection.sendmail(from_addr=username, to_addrs=send_to, msg="Subject:" + subject + "\n\n" + message)


def end_send():
    global connection
    connection.close()


def confirm_email(inp):
    for t in dic:
        inp = re.sub(t,dic[t],inp)
    return inp


def send_email(send_to, message, subject="", ):
    global connection
    try:
        start_send()
        send_main(send_to, message, subject)
        end_send()
        print(f"email send to {send_to}")
    except:
        print(f"sending email did not work because of error ")

import re
def strip(par):
    x = re.split("\s", par)
    x = x[-1]
    x = x.replace("<", "")
    x = x.replace(">", "")
    return x


def get_inbox():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select("inbox")
    _, search_data = mail.search(None, 'UNSEEN')
    my_message = []
    for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')
        # print(data[0])
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        for header in ['subject', 'to', 'from', 'date']:
            # print("{}: {}".format(header, email_message[header]))
            email_data[header] = email_message[header]

        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                email_data['body'] = body.decode()
            # elif part.get_content_type() == "text/html":
            #     html_body = part.get_payload(decode=True)
                # email_data['html_body'] = html_body.decode()
        my_message.append(email_data)

    return my_message





def sendPic(to, attachmentPath, sub="", name="responder"):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    gmail = username

    message = MIMEMultipart('mixed')
    message['From'] = f"{name} <{gmail}>"
    message['To'] = confirm_email(to)
    # message['To'] = to
    message['Subject'] = sub

    # if you ever want html
    # from email.mime.text import MIMEText
    # body = MIMEText('<h4>Hi There,<br> This is a testing message.</h4>\n', 'html')
    # message.attach(body)

    try:
        with open(attachmentPath, "rb") as attachment:
            p = MIMEApplication(attachment.read(), _subtype="png")
            p.add_header('Content-Disposition', "attachment; filename= %s" % attachmentPath.split("\\")[-1])
            message.attach(p)
    except Exception as e:
        print(str(e))

    msg_full = message.as_string()

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(gmail, password)
        server.sendmail(gmail,
                        message["To"].split(";") + (message["cc"].split(";") if message["cc"] else []),
                        msg_full)
        server.quit()

    print("email sent out successfully")
