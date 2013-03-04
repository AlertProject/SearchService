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

class Comment(Entity):
    """Models comments submitted to a root entity (Issue, Commit)"""
    
    def __init__(self, uid, comment, commentor, date):
        self._uid = uid
        self.__comment = comment
        self.__commentor = commentor
        """Poster of the comment"""
        self.__date = date
        
            
    def get_comment(self):
        """Text of this Comment"""
        return self.__comment
        
    def set_comment(self, value):
        self.__comment = value
            
    def get_commentor(self):
        """Person who made this Comment"""
        return self.__commentor
        
    def set_commentor(self, value):
        self.__commentor = value
        
    def get_date(self):
        """Date of the Comment"""
        return self.__date
        
    def set_date(self, value):
        self.__date = value
    
    @property
    def id(self):
        """Id of this comment"""
        return self._uid
        
    @id.setter
    def id(self, value):
        """Assign nev id to this comment"""
        self._uid = value