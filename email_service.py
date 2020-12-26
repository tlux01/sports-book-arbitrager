import smtplib, ssl
from datetime import timedelta, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_message(subject, html):
    port = 465
    smtp_server = "smtp.gmail.com"
    with open('email_auth.txt', 'r') as f:
        credentials = f.readlines()
        sender_email = credentials[0].strip('\n')
        sender_pass = credentials[1].strip('\n')
    with open('subscribers.txt', 'r') as f:
        subs = f.readlines()
        subs = map(lambda x : x.strip('\n'), subs)
    
    email = MIMEMultipart("alternative")
    email["Subject"] = subject
    email.attach(MIMEText(html, 'html'))
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, sender_pass)
        for sub in subs:
            s = server.sendmail(sender_email, sub, email.as_string())

def generate_message_for_profitable_bets(profitable_bets):
    # logical partition of bets in hours, keep any partitions over 24 to a multiple of 24
    partitions = [2,6,12,24,"Other"]
    n = len(partitions)

    # exclude "Other" partition, this case will be considered later
    hour_partitions = [timedelta(hours=partitions[i]) for i in range(n-1)]
    buckets = [[] for i in range(n)]
    for bet in profitable_bets:
        time_diff = bet['Date'] - datetime.now()
        for i in range(n-1):
            if time_diff < hour_partitions[i]:
                buckets[i].append(bet)
                break
        # Other case
        if time_diff > hour_partitions[-1]:
            buckets[-1].append(bet)
    
    number_bets_kept = 3
    for i in range(n):
        buckets[i].sort(key=lambda x : x['Juice'], reverse=True)
        bets_in_bucket = len(buckets[i])
        # c
        buckets[i] = buckets[i][:min(bets_in_bucket, number_bets_kept)]
      

    labeled_buckets = [{
        "Time Period": partitions[i],
        "Bets" : buckets[i]
    } for i in range(len(partitions))]
    html = generate_html_body_from_labeled_buckets(labeled_buckets)
    return html

def generate_html_body_from_labeled_buckets(labeled_buckets):
    html = """\
        <html>
        <head></head>
        <body>
        {}
        </body>
        </html>
    """  
    table_name_format = "<h2>Top Bets within {}</h2>\n"
    body = ""
    for labeled_bucket in labeled_buckets:
        time = labeled_bucket["Time Period"]
        bets = labeled_bucket["Bets"]
        if time == "Other":
             table_name = "<h2>Top Bets Anytime After</h2>\n"
        elif time < 24:
            table_name = table_name_format.format(str(time) + " Hours")
        else:
            table_name = table_name_format.format(str(time//24) + " Day(s)")

        table = """\
            <table style="width:100%">
            {header}
            {table_body}
            </table>
        """
        table_body = ""
        header = ""
        if bets:
            header = ["<th>{}</th>".format(k) for k in bets[0]]
            header = "<tr>" + "\n".join(header) + "</tr>\n"
            
            for bet in bets:
                tds = ["<td>{}</td>".format(bet[k]) for k in bet]
                table_body += "<tr>" + "\n".join(tds) + "</tr>\n"
        body += table_name + table.format(header=header, table_body=table_body)
    return html.format(body)
#send_email_message("TESSSTTTT", "MAKE THIS BET")
