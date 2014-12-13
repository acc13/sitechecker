#!/usr/bin/python
# Copyright 2014 Andrew Chang
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

"""Utility methods for comparing files."""

import hashlib
import logging
import codecs

class FileCmp:
    """Utility methods for comparing files."""
    
    @staticmethod
    def get_string_md5hash(strtohash):
        """returns md5 has of string foo"""
        md5 = hashlib.md5()
        md5.update(strtohash.encode('utf-8'))
        return str(md5.hexdigest())

    
    @staticmethod
    def get_file_hash(filename):
        """Returns md5 hash of a file.
        
        Args:
            filename (str):
            
        Returns:
            bool: True
        
        Raises:
            
        """
        file = codecs.open(filename, "r", encoding='utf-8')
        md5 = hashlib.md5()
        while True:
            data = file.read(128).encode('utf-8')
            if not data:
                break
            md5.update(data)

        file.close()
        return md5.digest()

    @staticmethod
    def file_cmp_by_hash(fn1, fn2):
        """Returns true if the file hashes of both files match.
        
        Args:
            fn1 (str): filename
            fn2 (str): filename
            
        Returns:
            bool: True if file hashes match
            
        Raises:
            
        """
        
        return FileCmp.get_file_hash(fn1) == FileCmp.get_file_hash(fn2)

    @staticmethod
    def file_cmp_by_area(fn1, fn2, startpatt, endpatt):
        """given two filenames, compares the contents of both files starting\
        with the match for re startpatt, and stopping with the match for re\
        endpatt"""
        raise 
        