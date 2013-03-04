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
from person import Person

class Attachment(Entity):
    """
    This class models Attachments associated with a root Entity (Issue, Commit)
    """
    
    def __init__(self, filename, description, creator, date, url):
        self.__filename = filename
        self.__description = description
        self.__creator = creator
        self.__date = date
        self.__url = url
            
    def get_filename(self):
        """Name of attached file"""
        return self.__filename
        
    def set_filename(self, value):
        self.__filename = value
            
    def get_description(self):
        """Attachment description"""
        return self.__description
        
    def set_description(self, value):
        self.__description = value
            
    def get_creator(self):
        """Person who submitted this attachment"""
        return self.__creator
        
    def set_creator(self, value):
        self.__creator = value
            
    def get_date(self):
        """Date on which the attachment was submitted"""
        return self.__date
        
    def set_date(self, value):
        self.__date = value
            
    def get_url(self):
        """URL of this attachment"""
        return self.__url
        
    def set_url(self, value):
        self.__url = value
            