#!/usr/bin/python
# Copyright 2014 Andrew Chang
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

"""Downloads a url, compares against saved page history, emails admin if a change detected."""

import sys
from urllib import request
import os
import logging
import inspect
import json
from emailer import SMTPEmailer

from filecmp import FileCmp

#set up logger
#TODO: I don't like this here...
logger = logging.getLogger('sitechecker') # pylint: disable=C0103
logger.setLevel(logging.INFO)
# create file handler which logs even info messages
modpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # pylint: disable=C0103
fh = logging.FileHandler(modpath + '\\sitechecker.log') # pylint: disable=C0103
fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler() # pylint: disable=C0103
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(levelname)s - %(funcName)s - %(message)s') # pylint: disable=C0103
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

class SiteChecker:
    """Downloads a url, compares against saved, emails admin if a change detected."""
    tmpfilename = "tmp"

    @staticmethod
    def print_and_rename(src, dst):
        """print to output before renaming"""
        logger.debug("renaming " + src + " to " + dst)
        os.rename(src, dst)
                    
    
    @staticmethod
    def save_and_rotate(savedir, filetosave):
        """saves last 10 files under savedir, under a subfolder named by hash of url, named 1-10"""
        maxsavefiles = 10
        
        try:
            os.remove(savedir + "\\" + str(maxsavefiles))
        except OSError:
            pass
            
        for i in reversed(range(1, maxsavefiles)):
            try:
                SiteChecker.print_and_rename(savedir + "\\" + str(i), savedir + "\\" + str(i + 1))
            except OSError as err:
                #we are expecting this exception, if fewer than 10 history files exist
                logger.debug("OS error {%s}: %s", err.errno, err.strerror)
    
        #save tmpfile
        SiteChecker.print_and_rename(savedir + "\\" +filetosave, savedir + "\\1")
        
    @staticmethod
    def email_myself(email, password, sub, msg):
        """send email to myself from my hotmail address"""
        try:
            SMTPEmailer("smtp.live.com", 587, email, password).send_email(email, sub, msg)
        except ConnectionRefusedError as err:
            logger.error("Error sending email.  Connection error {%s}: %s", err.errno, err.strerror)
    
    @staticmethod
    def create_dir_if_not_exist(dirname):
        """creates directory if not found"""
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except OSError as err:
                logger.error("OS error {%s}: %s", err.errno, err.strerror)
                raise err
    
    @staticmethod
    def save_urls_file(path, url, hashstring):
        """saves human readable dict of url->hashtring mappings under dir path"""
        
        dictfilename = path + '\\urls' 
        #load dict
        try:
            with open(dictfilename, 'r') as urlsfp:
                url2md5dict = json.load(urlsfp)
        except (IOError, ValueError):
            #no dict file found
            logger.info("no or empty dict file found: " + dictfilename)
            url2md5dict = {} 
        
        #save if key:val doesn't already exist
        if url not in url2md5dict.keys():
            url2md5dict[url] = hashstring
            with open(dictfilename, 'w') as urlsfp:
                json.dump(url2md5dict, urlsfp)
            

    @staticmethod
    def dl_and_cmp(url, email, password):
        """downloads file from url, and saves if newer version of page"""
        histpath = modpath + "\\hist"
        urlhashstring = FileCmp.get_string_md5hash(url)
        urlsavepath = histpath + "\\" + urlhashstring
        logger.info("urlsavepath is: " + urlsavepath)
            
        #create working directories if necessary
        SiteChecker.create_dir_if_not_exist(histpath)
        SiteChecker.create_dir_if_not_exist(urlsavepath)
        
        #save url->subdir(hash of url) mapping
        #just to make it easier for me to figure out what original url was
        SiteChecker.save_urls_file(histpath, url, urlhashstring)
        
        #download url
        try:
            request.urlretrieve(url, urlsavepath + "\\" + SiteChecker.tmpfilename)
        except IOError:
            logger.error("Could not download file: " + url)
            return
        
        logger.info("File downloaded: " + url)

        #if no local, or diff
        #save and rotate
        if not os.path.exists(urlsavepath + "\\1") or \
            not FileCmp.file_cmp_by_hash(urlsavepath + "\\" +SiteChecker.tmpfilename, \
            urlsavepath + "\\1"):
            logger.info("File at url has changed.  Saving.")
            SiteChecker.save_and_rotate(urlsavepath, SiteChecker.tmpfilename)
            
            #send notification email
            sub = "Sitechecker.py: url changed: " + url 
            msg = "Link: " + url
            SiteChecker.email_myself(email, password, sub, msg)
        #else clean up
        else:
            logger.info("File has not changed.  Cleaning up.")
            try:
                os.remove(urlsavepath + "\\" + SiteChecker.tmpfilename)
            except OSError:
                pass
            
        return

def usage():
    """print usage"""
    print('usage: -url url -email email -password password')
    sys.exit(1)
    
def main():
    """script main method"""
    
    #configloader tests
    args = sys.argv[1:]

    if not args:
        usage()
        
    if args[0] == '-url':
        url = args[1]
        del args[0:2]
    else:
        usage()
        
    if args[0] == '-email':
        email = args[1]
        del args[0:2]
    else:
        usage()
        
    if args[0] == '-password':
        password = args[1]
        del args[0:2]
    else:
        usage()

    SiteChecker.dl_and_cmp(url, email, password)
    #static url (for testing)
    #SiteChecker.dl_and_cmp("http://www.crawfordnotchcamping.com/vacancies.php")
    #changing url (for testing)
    #SiteChecker.dl_and_cmp("http://stackoverflow.com/questions/2759067/rename-files-in-python")
        
    sys.exit(0)    
        
if __name__ == '__main__':
    main()
