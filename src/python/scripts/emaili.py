
    
    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(USERNAME, PASSWORD)

    fromaddr = SENDER 
    toaddr = RECEIVER 
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Tämä on testi!"

    #tää pitäis toimia loppuversiossa
    #body = get_data()
    body = 'Hello World!'
    
    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)


