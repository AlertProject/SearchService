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

class StructuredKnowledgeSource(Entity):
    
    def __init__(self, uri, _type):
        self.__uri = uri
        self.__type = _type
            
    def get_uri(self):
        """URI for this StructuredKnowledgeSource"""
        return self.__uri
        
    def set_uri(self, value):
        self.__uri = value
            
    def get_type(self):
        return self.__type
        
    def set_type(self, value):
        self.__type = value
            