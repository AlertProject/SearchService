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

from entity import Entity

class File(Entity):
    
    def __init__(self, fileID, commitID):
        self.__file_id = fileID
        self.__filePath = None
        #self.__commitID = commitID
        self.__metrics = None
        self.__modules = []
        self._branch = ''
        self._action = None
        self._simple_action = ''
    
    def get_fileID(self):
        return self.__file_id
        
    def set_fileID(self, value):
        self.__file_id = value
    
    def get_filePath(self):
        return self.__filePath
        
    def set_filePath(self, value):
        self.__filePath = value
            
    def get_commitID(self):
        return self.__commitID
        
    def set_commitID(self, value):
        self.__commitID = value
    
    def get_metrics(self):
        return self.__metrics
        
    def set_metrics(self, value):
        self.__metrics = value
            
    def get_modules(self):
        return self.__modules
        
    def add_module(self, value):
        self.__modules.append(value)
        
    @property
    def branch(self):
        """Return branch of this file."""
        return self._branch
        
    @branch.setter
    def branch(self, branch):
        """Set new branch for this File."""
        self._branch = branch
        
    @property
    def action(self):
        """Return action for this File."""
        return self._action
        
    @action.setter
    def action(self, action):
        """Set new action for this File."""
        self._action = action
        
    @property
    def simple_action(self):
        """Return simple_action associated to this File."""
        return self._simple_action
        
    @simple_action.setter
    def simple_action(self, sa):
        """Set new simple action associated to this File"""
        self._simple_action = sa
        
        
        
        
        
        
        
        
        
        
        
        