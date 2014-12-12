#!/usr/bin/python
# Copyright 2014 Andrew Chang
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

"""Unit tests for filecmp.py"""

import unittest
from emailer import SMTPEmailer


class TestHashDiff(unittest.TestCase):
    """Unit tests for filecmp.py"""
    
    def setUp(self):
        passwd = ""
        self.emailer = SMTPEmailer("smtp.live.com", 587, "andrew_chang1@hotmail.com", passwd)
        
    def tearDown(self):
        pass
        
    def test_send_two_emails(self):
        """send two emails using same SMTPEmailer instance"""
        sub1 = "testsub1"
        msg1 = "testmsg1"
        sub2 = "testsub2"
        msg2 = "testmsg2"
        self.emailer.send_email("andrew_chang1@hotmail.com", sub1, msg1)
        self.emailer.send_email("andrew_chang1@hotmail.com", sub2, msg2)
    
        #read emails out other end
        #sleep?
        
if __name__ == '__main__':
    unittest.main()
    