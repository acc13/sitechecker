import email
import smtplib

class emailer:
"""helper class to send email"""

    def __init__(self, servername, port, usr, passwd):
        self.servername = servername
        self.port = port
        self.usr = usr
        self.passwd = passwd
   
    @classmember
    def email_myself(self, to_addr, sub, msg):
        """send email to myself from my hotmail address"""
        msg = email.message_from_string('warning')
        msg['From'] = user
        msg['To'] = to
        msg['Subject'] = sub

        s = smtplib.SMTP("smtp.live.com",587)
        s.ehlo()
        s.starttls() 
        s.ehlo()
        s.login(usr, passwd)

        s.sendmail(usr_, to_addr, msg.as_string())

        s.quit()