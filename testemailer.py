#!/usr/bin/python
# Copyright 2014 Andrew Chang
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

"""Unit tests for filecmp.py"""

import unittest
import sys
from emailer import SMTPEmailer


class TestEmailer(unittest.TestCase):
    """Unit tests for filecmp.py"""
    USERNAME = ""
    PASSWORD = ""
    
    def setUp(self):
        print(TestEmailer.USERNAME)
        print(TestEmailer.PASSWORD[0:3])
        self.emailer = SMTPEmailer("smtp.live.com", 587, TestEmailer.USERNAME, TestEmailer.PASSWORD)
        
    def tearDown(self):
        pass
        
    def test_send_two_emails(self):
        """send two emails using same SMTPEmailer instance"""
        sub1 = "testsub1"
        msg1 = "testmsg1"
        sub2 = "testsub2"
        msg2 = "testmsg2"
        self.emailer.send_email(TestEmailer.USERNAME, sub1, msg1)
        self.emailer.send_email(TestEmailer.USERNAME, sub2, msg2)
        
        #sleep & read emails out other end?
        
        
if __name__ == "__main__":
    if len(sys.argv) > 1:
        TestEmailer.PASSWORD = sys.argv.pop()
        TestEmailer.USERNAME = sys.argv.pop()
        unittest.main()
    