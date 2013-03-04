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

from datetime import datetime

from entity import Entity
from person import Person

class Commit(Entity):
    
    def __init__(self, commitMessage, commitDate, revisionTag, author,
                 committer):
        
        self.__commitMessage = commitMessage
        self.__commitDate = commitDate
        self.__revisionTag = revisionTag
        self.__author = author
        self.__committer = committer
        self.__repository = None
        self.__actions = []
        self.files = []
        self.repository_uri = ''
        
    def get_commitMessage(self):
        return self.__commitMessage
        
    def set_commitMessage(self, value):
        self.__commitMessage = value
        
    def get_commitDate(self):
        return self.__commitDate
        
    def set_commitDate(self, value):
        self.__commitDate = value
        
    def get_revisionTag(self):
        return self.__revisionTag
        
    def set_revisionTag(self, value):
        self.__revisionTag = value
        
    def get_author(self):
        return self.__author
        
    def set_author(self, value):
        self.__author = value
        
    def get_committer(self):
        return self.__committer
        
    def set_committer(self, value):
        self.__committer = value
        
    def get_repository(self):
        return self.__repository
        
    def set_repository(self, value):
        self.__repository = value
        
    def get_actions(self):
        return self.__actions
        
    def add_action(self, value):
        self.__actions.append(value)
                    