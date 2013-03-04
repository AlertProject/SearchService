# -*- coding: utf8 -*-
#
# Hound: Search service
# Copyright (C) 2012  GSyC/LibreSoft
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Felipe Ortega <jfelipe@libresoft.es>
#          Santiago Dueñas <sduenas@libresoft.es>

from urlparse import urlparse, ParseResult
from datetime import datetime

from entity import Entity
from issueTracker import IssueTracker
from attachment import Attachment
from comment import Comment
from person import Person

class Issue(Entity):
    """
    This class models an issue recorded in ITS
    """
    # Severity values
    BLOCKER = "Blocker"
    CRITICAL = "Critical"
    MAJOR = "Major"
    MINOR = "Minor"
    TRIVIAL = "Trivial"
    FEATURE = "Feature"
    
    # State values
    ASSIGNED = "Assigned"
    OPEN = "Open"
    RESOLVED = "Resolved"
    VERIFIED = "Verified"
    CLOSED = "Closed"
    
    # Resolution values
    DUPLICATED = "Duplicated"
    FIXED = "Fixed"
    INVALID = "Invalid"
    LATER = "Later"
    REMIND = "Remind"
    THIRD_PARTY = "Third Party"
    WONT_FIX = "Wont Fix"
    WORKS_FOR_ME = "Works For Me"

    def __init__(self, issue_id, short_desc, description, opened, reporter):
        self.__issue_tracker = None
        self.__issue_id = issue_id
        self.__issue_url = None
        self.__short_desc = short_desc
        self.__description = description
        self.__date_opened = opened
        self.__last_modified = None
        self.__assigned_to = None
        self.__reporter = reporter
        self.__severity = None
        self.__state = None
        self.__resoultion = None
        self._priority = ''
        self.__comments = []
        self.__attachments = []
        self._product = None
        self._computer_system = None
        self._activities = []
        self._cc_people = []
        self._milestone = None
        
    def get_issue_tracker(self):
        return self.__issue_tracker
        
    def set_issue_tracker(self, value):
        self.__issue_tracker = value
    
    def get_issue_id(self):
        return self.__issue_id
        
    def set_issue_id(self, value):
        self.__issue_id = value
        
    def get_issue_url(self):
        return self.__issue_url
        
    def set_issue_url(self, value):
        self.__issue_url = value
            
    def get_short_desc(self):
        return self.__short_desc
        
    def set_short_desc(self, value):
        self.__short_desc = value
        
    def get_description(self):
        return self.__description
        
    def set_description(self, value):
        self.__description = value
        
    def get_date_opened(self):
        return self.__date_opened
        
    def set_date_opened(self, value):
        self.__date_opened = value
        
    def get_last_modified(self):
        return self.__last_modified
        
    def set_last_modified(self, value):
        self.__last_modified = value
        
    def get_reporter(self):
        return self.__reporter
        
    def set_reporter(self, value):
        self.__reporter = value
    
    def is_enhancement(self):
        return self.__severity is Issue.FEATURE
        
    def is_bug(self):
        return not self.is_enhancement()
        
    def get_assigned_to(self):
        return self.__assigned_to
        
    def set_assigned_to(self, value):
        self.__assigned_to = value
        
    def get_severity(self):
        return self.__severity
        
    def set_severity(self, value):
        self.__severity = value
        
    def get_state(self):
        """Status of this issue"""
        return self.__state
        
    def set_state(self, value):
        self.__state = value
        
    def get_resolution(self):
        return self.__resolution
    
    def set_resolution(self, value):
        self.__resolution = value
    
    def get_comments(self):
        return self.__comments
        
    def add_comment(self, value):
        self.__comments.append(value)
            
    def get_attachments(self):
        return self.__attachments
        
    def add_attachment(self, value):
        self.__attachments.append(value)
        
    @property
    def priority(self):
        """Return Issue priority."""
        return self._priority
        
    @priority.setter
    def priority(self, priority):
        """Modify Issue priority."""
        self._priority = priority
        
    @property
    def product(self):
        """Return Product associated to this Issue."""
        return self._product
        
    @product.setter
    def product(self, product):
        """Modify  Product associated to this Issue."""
        self._product = product
        
    @property
    def activities(self):
        """Return list of Activities for this Issue"""
        return self._activities
        
    def add_activity(self, activity):
        """Add a new activity to this issue."""
        self._activities.append(activity)
        
    @property
    def cc_people(self):
        """Return list of people in CC for updates on this Issue."""
        return self._cc_people
        
    def add_cc_person(self, person):
        """Add new Person in CC for updates on this Issue."""
        self._cc_people.append(person)
        
    @property
    def milestone(self):
        """Return milestone associated to this Issue."""
        return self._milestone
        
    @milestone.setter
    def milestone(self, milestone):
        """Set milestone associated to this Issue."""
        self._milestone = milestone
        
    @property
    def computer_system(self):
        return self._computer_system
        
    @computer_system.setter
    def computer_system(self, computer_system):
        self._computer_system = computer_system
        
    