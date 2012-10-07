#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
 (c) 2012 - Copyright Pierre-Yves Chibon
 Author: Pierre-Yves Chibon <pingou@pingoured.fr>

 Distributed under License GPLv3 or later
 You can find a copy of this license on the website
 http://www.gnu.org/licenses/gpl.html

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 MA 02110-1301, USA.

 fedocal.model test script
"""

__requires__ = ['SQLAlchemy >= 0.7']
import pkg_resources

import unittest
import sys
import os

from datetime import date
from datetime import time
from datetime import timedelta

from sqlalchemy.exc import IntegrityError

sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..'))

from fedocallib import model
from fedocallib import week

from tests import Modeltests
from test_meeting import Meetingtests


class Weektests(Modeltests):
    """ Week tests. """

    def __init__(self, method_name='runTest'):
        """ Constructor. """
        unittest.TestCase.__init__(self, method_name)
        self.session = None

    def setUp(self):
        """ Set up the environnment, ran before every tests. """
        self.session = model.create_tables('sqlite:///:memory:')
        # Fills some data in the database in memory
        modeltest = Meetingtests(method_name='test_init_meeting')
        modeltest.session = self.session
        modeltest.test_init_meeting()

    def test_init_week(self):
        """ Test the Week init function. """
        calendar = model.Calendar.by_id(self.session, 'test_calendar')
        today = date.today()
        end_date = today + timedelta(days=7)
        weekobj = week.Week(self.session, calendar, today)

        self.assertNotEqual(weekobj, None)
        self.assertEqual(weekobj.start_date, today)
        self.assertEqual(weekobj.stop_date, end_date)
        self.assertEqual(len(weekobj.meetings), 2)

    def test_repr_week(self):
        """ Test if the week string representation is correct. """
        calendar = model.Calendar.by_id(self.session, 'test_calendar')
        today = date.today()
        end_date = today + timedelta(days=7)
        weekobj = week.Week(self.session, calendar, today)

        self.assertNotEqual(weekobj, None)
        self.assertEqual(str(weekobj), "<Week('%s' from '%s' to '%s')>" % (
            calendar.calendar_name, today, end_date))

    def test_meeting_in_week(self):
        """ Test that the meetings in the week are correct function. """
        calendar = model.Calendar.by_id(self.session, 'test_calendar')
        today = date.today()
        end_date = today + timedelta(days=7)
        weekobj = week.Week(self.session, calendar, today)

        # Test the meeting in the week
        self.assertNotEqual(weekobj, None)
        self.assertNotEqual(weekobj.meetings[0], None)
        self.assertEqual(weekobj.meetings[1].meeting_name,
            'Fedora-fr-test-meeting')
        self.assertEqual(weekobj.meetings[1].meeting_manager,
            'pingou, shaiton')
        self.assertEqual(weekobj.meetings[1].calendar.calendar_name,
            'test_calendar')
        self.assertEqual(weekobj.meetings[1].calendar.calendar_description,
            'This is a test calendar')
        self.assertEqual(weekobj.meetings[1].meeting_information,
            'This is a test meeting')
        self.assertEqual(weekobj.meetings[1].reminder, None)

        self.assertEqual(weekobj.meetings[0].meeting_name,
            'Another test meeting2')
        self.assertEqual(weekobj.meetings[0].meeting_manager,
            'pingou')
        self.assertEqual(weekobj.meetings[0].meeting_information,
            'This is a test meeting with recursion2')
        

   

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(Weektests)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
