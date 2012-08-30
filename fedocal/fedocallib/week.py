# -*- coding: utf-8 -*-

"""
fedocallib - Back-end library for the fedocal project.

Copyright (C) 2012 Pierre-Yves Chibon
Author: Pierre-Yves Chibon <pingou@pingoured.fr>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or (at
your option) any later version.
See http://www.gnu.org/copyleft/gpl.html  for the full text of the
license.
"""

from datetime import datetime
from datetime import date
from datetime import timedelta

from model import Calendar, Meeting


class Week(object):
    """ This class represents a week for in a specific calendar with
    all its meetings.
    """

    def __init__(self, calendar, start_date=None):
        """ Constructor, instanciate a week object for a given calendar.
        :arg calendar, the name of the calendar to use.
        :kwarg start_date, the starting date of the week.
        """
        self.calendar = Calender.by_id(calendar)
        self.start_date = start_date
        self.stop_date = start_date + timedelta(days=7)
        self.meetings = self.get_meetings()

    def get_meetings(self):
        """ Retrieves the list of this week meeting from the database.
        """
        self.meetings = Meeting.get_by_date(self.start_date,
            self.stop_date)

