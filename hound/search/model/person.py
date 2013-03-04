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
from entity import Entity

class Person(Entity):
    
    def __init__(self, name, email, user_id):
        self.__name = name
        self.__email = email
        self.__user_id = user_id
            
    def get_name(self):
        """Name of this Person"""
        return self.__name
        
    def set_name(self, value):
        self.__name = value
            
    def get_email(self):
        """Email of this Person"""
        return self.__email
        
    def set_email(self, value):
        self.__email = value
            
    def get_user_id(self):
        """ID for this user in the system"""
        return self.__user_id
        
    def set_user_id(self, value):
        self.__user_id = value
            