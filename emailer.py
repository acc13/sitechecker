#!/usr/bin/python
# Copyright 2014 Andrew Chang
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

"""helper class to send email"""

import email
import smtplib

class SMTPEmailer:
    """helper class to send email"""

    def __init__(self, servername, port, usr, passwd):
        self.servername = servername
        self.port = port
        self.usr = usr
        self.passwd = passwd
   
    def send_email(self, to_addr, sub, msg):
        """send email to to_addr, with subject sub and body msg"""
        msg = email.message_from_string('warning')
        msg['From'] = self.usr
        msg['To'] = to_addr
        msg['Subject'] = sub

        #smtpconn = smtplib.SMTP("smtp.live.com", 587)
        smtpconn = smtplib.SMTP(self.servername, self.port)
        smtpconn.ehlo()
        smtpconn.starttls() 
        smtpconn.ehlo()
        smtpconn.login(self.usr, self.passwd)

        smtpconn.sendmail(self.usr, to_addr, msg.as_string())

        smtpconn.quit()
        
        return True
        