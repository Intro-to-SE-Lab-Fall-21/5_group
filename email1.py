def sendMail(sender, password, recipient, subject, message):

    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender, password)
    server.send_message(msg)
    server.quit()
    
    print("email sent from ", sender, "to", recipient)

email = input("Your email address: ")
password = input("Password: ")
recipient = input("Recipient email address: ")
subject = input("Subject: ")
message = input("Message: ")

sendMail(email, password, recipient, subject, message)
input("Press enter to close...")