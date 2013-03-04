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

class Metrics(Entity):
    
    def __init__(self):
        self.__lang = None
        self.__sloc = -1
        self.__loc = -1
        self.__ncomment = -1
        self.__lcomment = -1
        self.__lblank = -1
        
    def get_lang(self):
        """Programming language concerning this metric"""
        return self.__lang
        
    def set_lang(self, value):
        self.__lang = value
            
    def get_sloc(self):
        return self.__sloc
        
    def set_sloc(self, value):
        self.__sloc = value
            
    def get_loc(self):
        return self.__loc
        
    def set_loc(self, value):
        self.__loc = value
            
    def get_num_comments(self):
        return self.__ncomment
        
    def set_num_comments(self, value):
        self.__ncomment = value
    
    def get_comments_lines(self):
        return self.__lcomment
        
    def set_comments_lines(self, value):
        self.__lcomment = value
    
    def get_blank_lines(self):
        return self.__lblank
        
    def set_blank_lines(self, value):
        self.__lblank = value
        