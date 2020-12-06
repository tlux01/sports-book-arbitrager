import smtplib, ssl

port = 465
smtp_server = "smtp.gmail.com"
with open('email_auth.txt', 'r') as f:
    credentials = f.readlines()
    sender_email = credentials[0].strip('\n')
    sender_pass = credentials[1].strip('\n')
with open('subscribers.txt', 'r') as f:
    subs = f.readlines()
    subs = map(lambda x : x.strip('\n'), subs)
message = """\
Subject: SportsPlays


Testing email service"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, sender_pass)
    for sub in subs:
        s = server.sendmail(sender_email, sub, message)
        print(s)
