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
# 

from django.db import models
import datetime

from search.model.issue import Issue
from search.model.commit import Commit
from search.model.person import Person

# Auxiliary model classes can be found in the 'model' module
class Person(models.Model):
    name = models.CharField(max_length=40, default='alias')
    email = models.EmailField(default='alias@foo.bar')
    user_id = models.IntegerField(default=1)
    
    def __unicode__(self):
        return self.name

class Commit(models.Model):
    commitMessage = models.CharField(max_length=40, default='AnotherCommit')
    commitDate = models.DateField(default=datetime.date.today())
    revisionTag = models.CharField(max_length=40, default='Main')
    author = models.ForeignKey(Person, related_name = "authors")
    committer = models.ForeignKey(Person, related_name = "committers")
    repository = models.CharField(max_length=40, default="MyIssueTracker")
    #actions = []
    
    def __unicode__(self):
        return self.commit_id

class Issue(models.Model):
    issue_tracker = models.CharField(max_length=40, default="MyIssueTracker")
    issue_id = models.CharField(max_length=40)
    issue_url = models.URLField(default="http://exampleITS/issue/")
    short_desc = models.CharField(max_length=40, default='Short desc')
    description = models.CharField(max_length=40, default='Full desc')
    date_opened = models.DateField(max_length=40, 
                                   default=datetime.date.today())
    last_modified = models.DateField(default=datetime.date.today())
    assigned_to = models.ManyToManyField(Person, related_name = "assignees")
    reporter = models.ForeignKey(Person, related_name = "reporters")
    severity = models.CharField(max_length=40, default=Issue.MINOR)
    state = models.CharField(max_length=40, default=Issue.OPEN)
    resoultion = models.CharField(max_length=40, default=Issue.LATER)
    comments = models.CharField(max_length=40, default='A comment')
    
    rel_commits = models.ManyToManyField(Commit)
    
    #attachments = [] 
    
    def __unicode__(self):
        return self.issue_id

class SearchResult(object):
    """This class models a search result"""
    def __init__(self, uuid = None, desc = None):
        self.uuid = uuid
        self.desc = desc
        #self.__results = {}
    
    # Dummy implementation to test REST API functionality
    #def retrieve_results(self):
        #issue = Issue(id = 1, short_desc = "First issue" , 
                      #description = "This is a very, very bad issue",
                      #opened = datetime.date.today(), 
                      #reporter = Person (name = "John Smith",
                                         #email = "jsmith@foo.bar",
                                         #user_id = 007) )
        
        #commit = Commit(commitMessage = "Hi", 
                          #commitDate = datetime.date.today(),
                          #revisionTag = 'main',
                          #author = Person (name = "John Smith",
                                         #email = "jsmith@foo.bar",
                                         #user_id = 007),
                          #committer = Person (name = "John Smith",
                                         #email = "jsmith@foo.bar",
                                         #user_id = 007))
        
        #self.__results[1] = issue
        #self.__results[2] = commit
        #return len(self.__results)