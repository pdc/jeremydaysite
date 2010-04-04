"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
import os
from datetime import datetime
from jeremyday.livejournal import *
from jeremyday.context_processors import *

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

        
    def test_entries(self):
        print os.getcwd()
        with open('frontpage/lj-test.html', 'rb') as input:
            html = input.read()
            
        entries = entries_from_livejournal_html(html)
        self.assertEqual(14, len(entries)) # 20 entries of which one is friends-locked.
        for i, entry in enumerate(entries):
            self.assert_(entry['title'], 'expected title for entry #%d' % i)
            self.assert_(entry['href'], 'expected href for entry #%d' % i)
            self.assert_(entry['content'], 'expected content for entry #%d' % i)
            self.assert_(entry['userpic']['src'], 'expected userpic.src for entry #%d' % i)
            self.assertEqual(100, entry['userpic']['width'], 'expected userpic.src for entry #%d' % i)
            self.assert_(entry['content'])
            self.assert_('class="user-icon"' not in entry['content'])
            
        self.assertEqual(datetime(2010, 3, 17, 23, 21, 0), entries[0]['published'])
        self.assertEqual(datetime(2010, 3, 16, 21, 41, 0), entries[1]['published'])
        self.assertEqual(datetime(2010, 3, 16, 0, 1, 0), entries[2]['published'])
        self.assertEqual(datetime(2010, 3, 11, 8, 35, 0), entries[4]['published'])
        
        self.assertEqual(8, entries[0]['comment_count'])        
        self.assertEqual(9, entries[1]['comment_count'])
        self.assertEqual(0, entries[5]['comment_count']) # Had to search for a post with no comments...!
        
    def test_date_coverage(self):
        self.assertEqual(True, is_date_covered(datetime(2010, 4, 7), datetime(2010, 4, 7)))
        self.assertEqual(False, is_date_covered(datetime(2010, 4, 7), datetime(2010, 4, 6)))
        self.assertEqual(False, is_date_covered(datetime(2010, 4, 7), datetime(2010, 4, 9)))
        self.assertEqual(True, is_date_covered(datetime(2010, 4, 7), datetime(2010, 4, 8, 10, 0, 0)))
        self.assertEqual(False, is_date_covered(datetime(2010, 4, 7), datetime(2010, 4, 8, 13, 0, 0)))
        self.assertEqual(True, is_date_covered(datetime(2010, 4, 7), datetime(2010, 4, 6, 13, 0, 0)))
        self.assertEqual(False, is_date_covered(datetime(2010, 4, 7), datetime(2010, 4, 6, 10, 0, 0)))
        
    def test_cass_naked_date(self):
        self.assertEqual(datetime(2010, 4, 7), css_naked_date(2010))
        
    def test_cass_naked_date_default(self):
        self.assertEqual(css_naked_date(datetime.now().year), css_naked_date())
        