#!/usr/bin/env python
import smtplib
from email.mime.text import MIMEText
from email.header    import Header
import sys

receiverName = sys.argv[1]
smtp_host = 'smtp-mail.outlook.com'
login = 'EMAIL
password = 'PASSWORD'
recipients_emails = [receiverName]

msg = MIMEText('A class you requested has opened up', 'plain', 'utf-8')
msg['Subject'] = Header('Class Alert', 'utf-8')
msg['From'] = login
msg['To'] = ", ".join(recipients_emails)

s = smtplib.SMTP(smtp_host, 587, timeout=10)
try:
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(login, password)
    s.sendmail(msg['From'], recipients_emails, msg.as_string())
finally:
    s.quit()
