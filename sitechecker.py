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

from filecmp import FileCmp

#set up logger
#TODO: I don't like this here...
logger = logging.getLogger('sitechecker') # pylint: disable=C0103
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
modpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # pylint: disable=C0103
fh = logging.FileHandler(modpath + '\\sitechecker.log') # pylint: disable=C0103
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler() # pylint: disable=C0103
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') # pylint: disable=C0103
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
    def email_myself():
        """send email to myself from my hotmail address"""
        pass
    
    @staticmethod
    def dl_and_cmp(url, savedir=None):
        """downloads file from url, and saves if newer version of page"""
        if savedir is None:
            savedir = modpath + "\\hist"
            
        savedir += "\\" + str(FileCmp.get_string_hash(url))
        logger.debug("savedir is: " + savedir)
            
        #check for savedir
        if not os.path.exists(savedir):
            try:
                os.makedirs(savedir)
            except OSError as err:
                logger.error("OS error {%s}: %s", err.errno, err.strerror)
            #save file under savedir with url name
            #just to make it easier for me to figure out what original url was
            try:
                urlfilename = savedir + "\\url"
                urlfile = open(urlfilename, "w")
                urlfile.write(url)
                urlfile.close()
            except IOError as err:
                logger.error("IOError {%s}: %s", err.errno, err.strerror)
        
        #download file
        try:
            request.urlretrieve(url, savedir + "\\" +SiteChecker.tmpfilename)
        except IOError:
            logger.error("Could not download file: " + url)
            return
        
        logger.debug("File downloaded: " + url)

        #if no local, or diff
        #save and rotate
        if not os.path.exists(savedir + "\\1") or \
            not FileCmp.file_cmp_by_hash(savedir + "\\" +SiteChecker.tmpfilename, \
            savedir + "\\1"):
            logger.debug("File at url has changed.  Saving.")
            SiteChecker.save_and_rotate(savedir, SiteChecker.tmpfilename)
            SiteChecker.email_myself()
        #else clean up
        else:
            logger.debug("File has not changed.  Cleaning up.")
            try:
                os.remove(savedir + "\\" + SiteChecker.tmpfilename)
            except OSError:
                pass
            
        return

def usage():
    """print usage"""
    print('usage: --url url ')
    sys.exit(1)
    
def main():
    """script main method"""
    
    #configloader tests
    args = sys.argv[1:]

    if not args:
        usage()
        
    if args[0] == '--url':
        url = args[1]
        del args[0:2]
    else:
        usage()

    SiteChecker.dl_and_cmp(url)
    #SiteChecker.dl_and_cmp("http://www.crawfordnotchcamping.com/vacancies.php")
    #SiteChecker.dl_and_cmp("http://stackoverflow.com/questions/2759067/rename-files-in-python")
        
    sys.exit(0)    
        
if __name__ == '__main__':
    main()
