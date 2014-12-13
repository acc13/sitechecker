#!/usr/bin/python
# Copyright 2014 Andrew Chang
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

"""Unit tests for filecmp.py"""

import unittest
from filecmp import FileCmp
import os
import inspect

class TestHashDiff(unittest.TestCase):
    """Unit tests for FileCmp"""
    modpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    file1name = modpath + "/file1.test"
    file1copyname = modpath + "/file1copy.test"
    notsamefilename = modpath + "/notsame.test"
    
    @classmethod
    def setUpClass(cls):
        file1 = open(cls.file1name, "w")
        file1copy = open(cls.file1copyname, "w")
        notsamefile = open(cls.notsamefilename, "w")
        
        mb1 = """To-morrow, and to-morrow, and to-morrow,
Creeps in this petty pace from day to day
To the last syllable of recorded time,
And all our yesterdays have lighted fools
The way to dusty death. Out, out, brief candle!
Life's but a walking shadow, a poor player
That struts and frets his hour upon the stage
And then is heard no more: it is a tale
Told by an idiot, full of sound and fury,
Signifying nothing."""
        
        mb2 = """Is this a dagger which I see before me,
The handle toward my hand? Come, let me clutch thee.
I have thee not, and yet I see thee still.
Art thou not, fatal vision, sensible
To feeling as to sight? or art thou but
A dagger of the mind, a false creation,
Proceeding from the heat-oppressed brain?
I see thee yet, in form as palpable
As this which now I draw.
Thou marshall'st me the way that I was going;
And such an instrument I was to use.
Mine eyes are made the fools o' the other senses,
Or else worth all the rest; I see thee still,
And on thy blade and dudgeon gouts of blood,
Which was not so before. There's no such thing:
It is the bloody business which informs
Thus to mine eyes. Now o'er the one halfworld
Nature seems dead, and wicked dreams abuse
The curtain'd sleep; witchcraft celebrates
Pale Hecate's offerings, and wither'd murder,
Alarum'd by his sentinel, the wolf,
Whose howl's his watch, thus with his stealthy pace.
With Tarquin's ravishing strides, towards his design
Moves like a ghost. Thou sure and firm-set earth,
Hear not my steps, which way they walk, for fear
Thy very stones prate of my whereabout,
And take the present horror from the time,
Which now suits with it. Whiles I threat, he lives:
Words to the heat of deeds too cold breath gives."""
        
        file1.write(mb1)
        file1copy.write(mb1)
        notsamefile.write(mb2)
        
        file1.close()
        file1copy.close()
        notsamefile.close()
 
 
 
    @classmethod    
    def tearDownClass(cls):
        #delete test files
        try: 
            os.remove(cls.file1name)
        except OSError:
            pass
        try: 
            os.remove(cls.file1copyname)
        except OSError:
            pass
        try: 
            os.remove(cls.notsamefilename)
        except OSError:
            pass
        return

    def test_files_same_hash(self):
        """Assert that files w/ identical contents have same file hash"""
        self.assertTrue(FileCmp.file_cmp_by_hash(self.file1name, self.file1copyname))
        
    def test_files_notsame_hash(self):
        """Assert that files w/ diff contents do not have matching hashes"""
        self.assertFalse(FileCmp.file_cmp_by_hash(self.file1name, self.notsamefilename))
    
if __name__ == '__main__':
    unittest.main()
